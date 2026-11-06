"""Exactly one top-level active-runtime sanity attempt after the static gate."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import app
import m1
from openai.resources.responses import Responses

OUT = Path(__file__).resolve().parent
REQUEST = (
    '/AUTHOR GENERIC ISOLATED\n'
    'Create a prompt that compares only the two options supplied in this request: paper notes and plain-text notes. '
    'Treat both as undecided. Do not use earlier chat/project decisions unless I explicitly identify them here. '
    'Do not execute the prompt.'
)


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run():
    gate = json.loads((OUT / 'static_summary.json').read_text(encoding='utf-8'))
    assert gate['passed'], 'Static gate has not passed.'
    for path, expected in gate['source_hashes'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    target = OUT / 'active_runtime.json'
    if target.exists():
        raise SystemExit('Existing evidence: refusing another live attempt.')
    config = app.read_config()
    messages = [
        dict(role='user', content='Earlier project discussion: CANARY_ACTIVE_PRIOR. We accepted cloud notebooks as the only method and rejected paper notes.'),
        dict(role='assistant', content='Accepted decision recorded: use cloud notebooks exclusively; paper notes are rejected. CANARY_ACTIVE_PRIOR.'),
        dict(role='user', content=REQUEST),
    ]
    control_paths = [app.HUB_CI_PATH, app.HUB_ROUTER_PATH, app.HUB_ARCHITECTURE_PATH,
                     app.HUB_CATALOG_PATH, ROOT / 'runtime/HUB_LOCAL_BINDINGS_v0.3.json',
                     ROOT / 'runtime/packages/authoring/HUB-CAP-AUTHORING_v0.7.md']
    record = dict(evidence_class='ACTIVE LOCAL RUNTIME LIVE', top_level_attempts=1,
                  model=config['model'], messages=messages, calls=[], trace=None, result='NOT_EVALUATED',
                  started_utc=datetime.now(timezone.utc).isoformat(),
                  versions=gate['versions'], static_gate_sha256=hashlib.sha256((OUT / 'static_summary.json').read_bytes()).hexdigest(),
                  controls={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in control_paths})
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    original = Responses.create

    def observed(client, *args, **kwargs):
        assert not args
        call = dict(number=len(record['calls']) + 1, payload=kwargs,
                    payload_sha256=hashlib.sha256(json.dumps(kwargs, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
                    max_retries=client._client.max_retries)
        record['calls'].append(call)
        save(target, record)
        assert call['max_retries'] == 0
        try:
            response = original(client, **kwargs)
        except Exception as exc:
            call['error'] = dict(type=type(exc).__name__, message=str(exc))
            save(target, record)
            raise
        call['response'] = response.model_dump(mode='json')
        call['output'] = response.output_text
        call['output_sha256'] = hashlib.sha256(response.output_text.encode()).hexdigest()
        save(target, record)
        print(f"call={call['number']} phase={kwargs.get('text', {}).get('format', {}).get('name', 'text')} status={response.status}", flush=True)
        return response

    try:
        with patch.object(Responses, 'create', observed):
            record['output'], record['trace'] = m1.call_runtime(config, messages)
        record['output_sha256'] = hashlib.sha256(record['output'].encode()).hexdigest()
        print(record['output'], flush=True)
        print(json.dumps(record['trace'], ensure_ascii=False), flush=True)
    except Exception as exc:
        record['error'] = dict(type=type(exc).__name__, message=str(exc))
        record['trace'] = getattr(exc, 'trace', None)
        print(json.dumps(record['error'], ensure_ascii=False), flush=True)
    finally:
        record['responses_api_calls'] = len(record['calls'])
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(target, record)


if __name__ == '__main__':
    run()
