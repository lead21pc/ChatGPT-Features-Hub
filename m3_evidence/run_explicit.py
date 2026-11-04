"""Evidence-only M3 observer. Each checkpoint/workload is exclusive, never retried."""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import httpx
import app
import m1
from m2_acceptance import PROMPTS
from openai.resources.responses import Responses

OUT = ROOT / 'm3_evidence'
PRICES = dict(model='gpt-5.6-sol', ordinary_input_per_million=4,
              cached_input_per_million=0.40, cache_write_30m_per_million=5,
              output_per_million=20, web_search_per_call=0.01,
              provenance='User-supplied official-doc snapshot; evidence only',
              search_content='Included in provider input usage where reported; no separate estimate')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def now():
    return datetime.now(timezone.utc).isoformat()


def snapshot():
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths
            if p and (ROOT / p).is_file()}


def run(checkpoint, number):
    target = OUT / f'{checkpoint}_workload_{number}.json'
    checks = json.loads((OUT / 'explicit_static_checks.json').read_text(encoding='utf-8'))
    assert checks['static_pass'], 'Static gate not passed'
    assert checkpoint == 'explicit'
    if number == 2:
        first = json.loads((OUT / 'explicit_workload_1.json').read_text(encoding='utf-8'))
        assert first['error'] is None and first['responses_api_calls'] == 7
    config = app.read_config()
    record = dict(checkpoint=checkpoint, workload=number, prompt=PROMPTS[number],
                  model=config['model'], started_utc=now(), prices=PRICES,
                  head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
                  source_hashes=snapshot(), calls=[], trace=None, final_output=None, error=None)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    original = Responses.create

    def observed(client, *args, **kwargs):
        instructions = kwargs.get('instructions', '')
        phase = kwargs.get('text', {}).get('format', {}).get('name')
        if not phase:
            phase = 'ais' if kwargs.get('tools') else 'text'
        call = dict(number=len(record['calls']) + 1, phase=phase, started_utc=now(),
                    max_retries=client._client.max_retries, request=kwargs)
        record['calls'].append(call)
        marker = '[T8 VERIFIED HANDOFF]\n'
        if phase == 'hub_t8_concept':
            instructions = kwargs['input'][1]['content'][0]['text']
        if marker in instructions:
            call['handoff'] = json.JSONDecoder().raw_decode(instructions.split(marker, 1)[1])[0]
            call['handoff_field_bytes'] = {k: len(json.dumps(v, ensure_ascii=False).encode())
                                          for k, v in call['handoff'].items()}
        save(target, record)
        try:
            response = original(client, *args, **kwargs)
            call['response'] = response.model_dump(mode='json')
            call['usage'] = call['response'].get('usage')
            print(f'{checkpoint} W{number} call={call["number"]} phase={phase} status={response.status}', flush=True)
            return response
        except Exception as exc:
            call['error'] = dict(type=type(exc).__name__, message=str(exc))
            raise
        finally:
            call['finished_utc'] = now()
            save(target, record)

    original_send = httpx.Client.send

    def observed_send(client, request, *args, **kwargs):
        if request.url.path.endswith('/responses'):
            record['calls'][-1]['serialized_request'] = json.loads(request.content)
            save(target, record)
        return original_send(client, request, *args, **kwargs)

    try:
        with patch.object(Responses, 'create', observed), patch.object(httpx.Client, 'send', observed_send):
            record['final_output'], record['trace'] = m1.call_runtime(
                config, [dict(role='user', content=PROMPTS[number])])
    except Exception as exc:
        record['error'] = dict(type=type(exc).__name__, message=str(exc))
        record['trace'] = getattr(exc, 'trace', None)
    finally:
        record['responses_api_calls'] = len(record['calls'])
        record['finished_utc'] = now()
        record['source_hashes_after'] = snapshot()
        save(target, record)
    print(json.dumps(dict(checkpoint=checkpoint, workload=number,
                          calls=len(record['calls']), error=record['error']), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('checkpoint', choices=['explicit'])
    parser.add_argument('workload', type=int, choices=[1, 2])
    args = parser.parse_args()
    run(args.checkpoint, args.workload)
