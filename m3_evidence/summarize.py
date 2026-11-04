"""Offline usage accounting; no API access, no runtime controls."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def summarize(record):
    calls = []
    for c in record['calls']:
        phase = c['phase']
        instructions = c['request'].get('instructions', '')
        if phase == 'text':
            if 'Execute only this verified scoped Authoring contribution' in instructions:
                phase = 'contribution_execution'
            elif 'Return scoped results FOR HUB' in instructions:
                phase = 'independent_scope_execution'
            else:
                phase = 'final_authoring' if (c.get('handoff', {}).get('authoring_active')) else 'final_hub'
        u = c.get('usage') or {}
        details = u.get('input_tokens_details') or {}
        # Preserve missing-provider-field uncertainty rather than treating it as zero.
        cached = details.get('cached_tokens')
        write = details.get('cache_write_tokens')
        ordinary = u['input_tokens'] - cached - write if cached is not None and write is not None else None
        web = sum(item.get('type') == 'web_search_call' for item in c.get('response', {}).get('output', []))
        cost = ((ordinary * 4 + cached * .4 + write * 5 + u['output_tokens'] * 20) / 1e6
                if ordinary is not None else None)
        calls.append(dict(number=c['number'], phase=phase, input=u.get('input_tokens'),
                          ordinary=ordinary, cached=cached, cache_write=write,
                          output=u.get('output_tokens'), total=u.get('total_tokens'),
                          token_cost_usd=cost, web_search_calls=web,
                          web_search_cost_usd=web * .01))
    fields = ['input', 'ordinary', 'cached', 'cache_write', 'output', 'total',
              'token_cost_usd', 'web_search_calls', 'web_search_cost_usd']
    totals = {k: sum(c[k] for c in calls) if all(c[k] is not None for c in calls) else None for k in fields}
    return dict(calls=calls, totals=totals, responses_api_calls=len(calls), error=record['error'])


if __name__ == '__main__':
    result = {p.stem: summarize(json.loads(p.read_text(encoding='utf-8')))
              for p in sorted(OUT.glob('*_workload_*.json'))}
    for checkpoint in ('baseline_current', 'post'):
        pair = [result.get(f'{checkpoint}_workload_{n}') for n in (1, 2)]
        if all(pair):
            result[checkpoint + '_pair'] = {
                **{k: sum(r['totals'][k] for r in pair) for k in pair[0]['totals']},
                'responses_api_calls': sum(r['responses_api_calls'] for r in pair)}
    if 'post_pair' in result and 'baseline_current_pair' in result:
        before, after = result['baseline_current_pair'], result['post_pair']
        result['pair_delta_post_minus_baseline'] = {k: after[k] - before[k] for k in before}
        result['observed_token_cost_savings_percent'] = 100 * (1 - after['token_cost_usd'] / before['token_cost_usd'])
        result['phase_deltas'] = {}
        for number in (1, 2):
            b = result[f'baseline_current_workload_{number}']['calls']
            p = result[f'post_workload_{number}']['calls']
            assert [c['phase'] for c in b] == [c['phase'] for c in p], 'Changed phase/call sequence'
            result['phase_deltas'][f'workload_{number}'] = [
                dict(phase=x['phase'], **{k: y[k] - x[k] for k in
                    ('input', 'ordinary', 'cached', 'cache_write', 'output', 'token_cost_usd', 'web_search_calls')})
                for x, y in zip(b, p)]
    path = OUT / 'metrics.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
