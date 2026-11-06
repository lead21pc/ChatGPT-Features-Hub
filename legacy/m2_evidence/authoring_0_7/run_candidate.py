"""Two supplied-candidate live cases; one no-tool Responses call per case, no retries."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import app
import openai
from openai import OpenAI

OUT = Path(__file__).resolve().parent
HUB = ROOT / 'upstream/Central Hub'
CANDIDATE = HUB / 'candidates/authoring_v0_7'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run(case_id):
    path = OUT / f'candidate_{case_id}.json'
    if path.exists():
        raise SystemExit('Existing evidence: refusing another live attempt.')
    case = next(c for c in json.loads((CANDIDATE / 'ISOLATION_TEST_CASES.json').read_text(
        encoding='utf-8'))['cases'] if c['id'] == case_id)
    config = app.read_config()
    paths = [HUB / 'HUB_CI_v1.1.md', CANDIDATE / 'HUB_PACKAGE_CATALOG_v1.9-candidate.yaml',
             CANDIDATE / 'HUB-CAP-AUTHORING_v0.7-candidate.md']
    binding = (
        '[M2 SUPPLIED-CANDIDATE BINDING]\n'
        'This is an explicitly authorized supplied-candidate Authoring turn. The complete '
        'candidate Catalog 1.9-candidate and Authoring 0.7-candidate below are supplied controls '
        'for this test only, under Hub CI 1.1. They are not installed production bindings. '
        'Apply the candidate Authoring entrypoint to the current user turn under these controls. '
        'Earlier conversation and project context remain visible ambient context, with their '
        'ordinary provenance. No target execution is authorized. Return the Authoring result.'
    )
    bodies = [p.read_text(encoding='utf-8') for p in paths]
    messages = []
    if case.get('project_context'):
        messages.append(dict(role='user', content=case['project_context']))
    messages.append(dict(role='assistant', content=case['prior_chat']))
    messages.append(dict(role='user', content=case['request']))
    payload = dict(model=config['model'], input=messages,
                   instructions='\n\n'.join([bodies[0], binding, *bodies[1:]]), store=False)
    record = dict(case_id=case_id, evidence_class='CANDIDATE LIVE',
                  baseline_commit='c619a5a6895cf0d9aa67a92ebb46f36a8bb9e228',
                  started_utc=datetime.now(timezone.utc).isoformat(),
                  sdk_version=openai.__version__, max_retries=0, tools=[],
                  versions=dict(ci='1.1', catalog='1.9-candidate', authoring='0.7-candidate'),
                  controls=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p.read_bytes()))
                            for p in paths], payload=payload,
                  payload_sha256=sha(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()),
                  api_calls=0, result='NOT_EVALUATED')
    with path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    try:
        with OpenAI(api_key=config['openai_api_key'], base_url='https://api.openai.com/v1',
                    timeout=120.0, max_retries=0) as client:
            record['api_calls'] = 1
            save(path, record)
            response = client.responses.create(**payload)
        record['response'] = response.model_dump(mode='json')
        record['output'] = response.output_text
        record['output_sha256'] = sha(response.output_text.encode())
        print(response.output_text, flush=True)
    except Exception as exc:
        record['error'] = dict(type=type(exc).__name__, message=str(exc))
        print(json.dumps(record['error']), flush=True)
    finally:
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save(path, record)


if __name__ == '__main__':
    case_id = sys.argv[1]
    if case_id not in ('I1', 'I3'):
        raise SystemExit('Only I1 and I3 are authorized.')
    run(case_id)
