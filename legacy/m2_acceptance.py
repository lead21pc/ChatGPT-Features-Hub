"""Observational runner for the two fixed M2 workloads; no retries or payload edits."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import app
import m1
from openai.resources.responses import Responses


PROMPTS = {
    1: '/AUTHOR GENERIC + BRAINSTORM\nCreate a prompt for another model to brainstorm 6 clearly different ways to build a desktop UI for Central Hub after M4. Do not choose a winning option yet. Use Brainstorm as a contributor to expand candidate ideas before writing the final prompt. Do not implement the UI and do not execute any target.\nWithin this Authoring request, apply the following explicit scoped Brainstorm control:\n/BRAINSTORM Expand six materially different candidate approaches for the desktop UI layer, including different integration boundaries, packaging tradeoffs, and failure modes. Keep them as parallel candidates; do not rank or accept one. #\n',
    2: 'Evaluate this proposal for Central Hub after M4: use Tauri as the desktop UI layer while keeping the current Python runtime behind it.\n1) Use Technical to analyze integration boundaries and technical risks of connecting a desktop frontend to the Python runtime.\n2) Use Concept to develop at least 3 architecture candidates using this explicit scoped control: /BRAINSTORM Produce at least three materially different integration architecture variants. Keep them parallel candidates and do not accept or rank a winner. #\n3) Use AIS to verify the current Tauri documentation about sidecars and bundling external binaries or processes, using official Tauri sources only.\n4) Let Hub synthesize the final answer, clearly separating external evidence, Concept candidates, and Technical diagnosis. Do not accept any Concept candidate as a project decision.',
}

OUT = Path(__file__).resolve().parent / "m2_evidence"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def snapshot():
    return {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path('.').rglob('*') if p.is_file()
            and not any(x in p.parts for x in ('.git', '__pycache__', 'm2_evidence'))}


def run(number):
    OUT.mkdir(exist_ok=True)
    target = OUT / f"workload_{number}_corrected_ab.json"
    if target.exists():
        raise SystemExit("Existing evidence: refusing another live execution.")
    config = app.read_config()
    record = dict(workload=number, prompt=PROMPTS[number], model=config['model'],
                  started_utc=datetime.now(timezone.utc).isoformat(), calls=[], trace=None,
                  final_output=None, error=None)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    original = Responses.create

    def observed(client, *args, **kwargs):
        call = dict(number=len(record['calls']) + 1,
                    phase=kwargs.get('text', {}).get('format', {}).get('name', 'text'),
                    tools=kwargs.get('tools', []), tool_choice=kwargs.get('tool_choice'),
                    model=kwargs.get('model'), store=kwargs.get('store'))
        record['calls'].append(call)
        # Capture handoff data without changing instructions or retaining API credentials.
        instructions = kwargs.get('instructions', '')
        marker = '[T8 VERIFIED HANDOFF]\n'
        if marker in instructions:
            call['handoff'] = json.JSONDecoder().raw_decode(instructions.split(marker, 1)[1])[0]
        save(target, record)
        try:
            response = original(client, *args, **kwargs)
        except Exception as exc:
            call['error'] = dict(type=type(exc).__name__, message=str(exc))
            save(target, record)
            raise
        call['response'] = response.model_dump(mode='json')
        save(target, record)
        print(f"workload={number} call={call['number']} phase={call['phase']} status={response.status}", flush=True)
        return response

    try:
        with patch.object(Responses, 'create', observed):
            record['final_output'], record['trace'] = m1.call_runtime(
                config, [dict(role='user', content=PROMPTS[number])])
    except Exception as exc:
        record['error'] = dict(type=type(exc).__name__, message=str(exc))
        record['trace'] = getattr(exc, 'trace', None)
    finally:
        record['responses_api_calls'] = len(record['calls'])
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(target, record)
    print(json.dumps({k: record[k] for k in ('workload', 'responses_api_calls', 'error', 'trace')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('baseline', '1', '2', 'check'))
    action = parser.parse_args().action
    if action == 'baseline':
        OUT.mkdir(exist_ok=True)
        if (OUT / 'baseline.json').exists():
            raise SystemExit('Baseline already exists.')
        save(OUT / 'baseline.json', snapshot())
    elif action == 'check':
        before = json.loads((OUT / 'baseline.json').read_text(encoding='utf-8'))
        after = snapshot()
        print(json.dumps(dict(changed=[p for p in before if before[p] != after.get(p)],
                              added=sorted(set(after) - set(before))), ensure_ascii=False))
    else:
        run(int(action))

