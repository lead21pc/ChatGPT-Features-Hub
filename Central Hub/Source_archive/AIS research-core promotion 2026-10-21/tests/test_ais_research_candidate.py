"""Static contract checks and declared semantic fixtures, never a runtime AIS executor.

These oracles do not interpret natural language, launch tools, transfer chats,
or establish model compliance. RC fixtures encode already-classified task shapes.
"""
import copy
import hashlib
from pathlib import Path
import re
import unittest

from test_hub_contracts import load

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'candidates/ais_research_core'
BASE = ROOT / 'tool_pipelines/AIS'
POLICY = load(CANDIDATE / 'AIS_ROUTER_v1.2-candidate.yaml')

# Captured before this task's edits, from the clean local 603bd01 working tree.
BASELINE = {
    'HUB_CI_v1.1.md': '7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b',
    'HUB_ROUTER_v1.1.yaml': 'ab7c67ae3ad97e7131db7e282b53c5540c11cd4249994f8f87cac0fb8a3462e6',
    'HUB_ARCHITECTURE_v1.0.md': '6c7d6663afa9bd17c2eb80a8036f52f5f70ab32237fcaba65358cabc21787b7e',
    'HUB_PACKAGE_CATALOG_v1.0.yaml': 'ccfe5f0fa109646abe6e76398c7235c4915ca1777501c1a71c1f694401d290a3',
    'tool_pipelines/AIS/AIS_PIPELINE_v1.0.md': 'c7f78f10be855d6b77aa3e0bbf67c3856c7fa42f890382752056de71abd10f69',
    'tool_pipelines/AIS/AIS_ROUTER_v1.1.yaml': 'ea5e22648fdcb1da239126ec25220b474444de11521887cd93711f41b4b32901',
    'tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md': '3519fd3f596043e157b987129afbd51872f991faf889fb91162ac754f51529d3',
    'tests/HUB_ROUTE_TEST_CASES.md': 'db3903d41a1ad72014ca940c6fb129a07ede3d87f1861781b94ddc2213d176d9',
    'tests/test_hub_contracts.py': 'e954c342edcacace93d3df4d7fc97e8eddf0f0fc296f6b92c611ea0a5991cf22',
}


def execution_oracle(traces=(), action='search', attempt=1, retrospective=None):
    """Expected classification of declared direct traces, not trace discovery.

retrospective is deliberately insufficient to establish either execution state.
All supplied direct traces in a fixture share target/time/surface.
"""
    rules = POLICY['execution_observability']['status_rules']
    kinds = {kind for a, n, kind in traces if (a, n) == (action, attempt)}
    executed = bool(kinds.intersection(rules['EXECUTED']))
    not_executed = bool(kinds.intersection(rules['NOT_EXECUTED']))
    if executed and not_executed:
        return 'CONFLICTED'
    if executed:
        return 'EXECUTED'
    return 'NOT_EXECUTED' if not_executed else 'UNKNOWN'


def lane_state(availability='AVAILABLE', resource='AVAILABLE', launch=True,
               basis='DIRECT_PLATFORM_TOOL_STATE', transition='DIRECT_OBSERVED'):
    return dict(availability=availability, resource=resource, launch=launch,
                basis=basis, transition=transition)


def strategy_oracle(shape='bounded', depth=False, conserve=False, named=None,
                    lanes=None, fallback_allowed=True, authorized=True,
                    material_benefit=True, low_bounded=False):
    """SPEC only: supplied shape means material task needs already established.

No capability discovery. A feasible selection still makes zero actual calls.
"""
    p = POLICY['research_policy']
    lanes = lanes or {}
    quality = 'EXTENSIVE' if shape == 'broad_synthesis' else (
        'THOROUGH' if depth or shape == 'workflow' else 'NORMAL')
    preferred = named or (p['lane_selection']['conserve_quota'] if conserve else
                         'WORK' if shape == 'workflow' else
                         'DEEP_RESEARCH' if shape == 'broad_synthesis' else
                         p['lane_selection']['default'])

    def feasible(lane):
        state = lanes.get(lane, {})
        if not authorized or state.get('availability') != 'AVAILABLE':
            return False
        if state.get('basis') not in p['availability_evidence']:
            return False
        if p['launch_required'] and not state.get('launch'):
            return False
        resource = state.get('resource', 'UNKNOWN')
        if resource not in p['resource_states'] or resource == 'EXHAUSTED':
            return False
        if lane == 'WORK' and state.get('transition') not in {
                'DIRECT_OBSERVED', 'PROJECT_CONTEXT_AVAILABLE'}:
            return False
        if lane != 'CHAT_GUIDED':
            if not (material_benefit or named):
                return False
            if resource == 'LOW' and not low_bounded:
                return False
        return True

    selected = preferred if feasible(preferred) else (
        'CHAT_GUIDED' if fallback_allowed and feasible('CHAT_GUIDED') else 'UNRESOLVED')
    return dict(quality=quality, preferred=preferred, selected=selected,
                resource=lanes.get(selected, {}).get('resource', 'UNKNOWN'),
                needs_handoff=(selected == 'WORK' and
                               lanes[selected]['transition'] == 'PROJECT_CONTEXT_AVAILABLE'),
                observed_used='UNKNOWN', actual_calls=0)


def supported_claim(decisive_reads=(), supporting_reads=(), label=None):
    """A verified label cannot create the missing decisive read/support relation."""
    return 'SUPPORTED' if set(decisive_reads).intersection(supporting_reads) else 'UNRESOLVED'


def fallback_oracle(branches):
    """Retain supported branches; only unresolved/invalidated branches need work."""
    retained = {k: copy.deepcopy(v) for k, v in branches.items()
                if v['supported'] and not v.get('invalidated')}
    return retained, set(branches) - set(retained)


class AISResearchStaticTests(unittest.TestCase):
    def test_candidate_pair_stage_order_and_unchanged_owners(self):
        active = load(BASE / 'AIS_ROUTER_v1.1.yaml')
        self.assertEqual(POLICY['status'], 'CANDIDATE')
        self.assertFalse(POLICY['active'])
        self.assertEqual(POLICY['live_verification'], 'NOT_RUN')
        sequence = POLICY['stage_sequence']
        self.assertEqual(sequence, list(POLICY['stages']))
        self.assertEqual([s for s in sequence if s != 'RESEARCH_STRATEGY'], active['stage_sequence'])
        self.assertEqual(sequence[2:5], ['SOURCE_AUTHORITY_GATE', 'RESEARCH_STRATEGY', 'TOOL_FACING_INSTRUCTION'])
        for key in ['modes', 'mode_resolution', 'source_policy']:
            self.assertEqual(POLICY[key], active[key])
        old_lock = copy.deepcopy(POLICY['search_contract'])
        strategy = old_lock.pop('research_strategy')
        self.assertEqual(old_lock, active['search_contract'])
        self.assertEqual(set(strategy), {'quality_target', 'task_shape', 'preferred_executor',
                         'observed_executor_state', 'resource_state', 'work_transition', 'selected_executor', 'fallback'})
        for owner in ['hub', 'hub_router', 'platform', 'evidence']:
            self.assertEqual(POLICY['ownership'][owner], active['ownership'][owner])
        pipeline = (CANDIDATE / 'AIS_PIPELINE_v1.1-candidate.md').read_text(encoding='utf-8')
        refs = re.findall(r'`(AIS_ROUTER_[^`]+\.yaml)`', pipeline)
        self.assertEqual(refs, ['AIS_ROUTER_v1.2-candidate.yaml'])
        self.assertTrue((CANDIDATE / refs[0]).is_file())
        self.assertIn('not admitted by the active Hub Catalog', pipeline)
        self.assertIn('without reassessing the whole turn', pipeline)

    def test_active_baselines_and_28_cases_byte_exact(self):
        for name, sha in BASELINE.items():
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), sha)
        original = (BASE / 'tests/ROUTE_TEST_CASES.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (AIS-\d+) \|', original, re.M),
                         [f'AIS-{n:02}' for n in range(1, 29)])
        catalog = (ROOT / 'HUB_PACKAGE_CATALOG_v1.0.yaml').read_text(encoding='utf-8')
        self.assertNotIn('ais_research_core', catalog)

    def test_contract_gates_loop_return_and_evidence_limits(self):
        p = POLICY['research_policy']
        self.assertEqual(set(p['quality_targets']), {'NORMAL', 'THOROUGH', 'EXTENSIVE'})
        self.assertEqual(set(p['resource_states']), {'AVAILABLE', 'LOW', 'EXHAUSTED', 'UNKNOWN'})
        self.assertFalse(p['forum_proves_runtime'])
        self.assertFalse(p['plan_proves_resource'])
        self.assertTrue(p['launch_required'])
        for field in ['quality target', 'selected executor', 'resource/availability', 'fallback',
                      'protected state', 'stop condition', 'executor transition']:
            self.assertIn(field, POLICY['stages']['PRE_CALL_CHECK'])
        loop = ' '.join(p['chat_guided_loop'])
        for concept in ['unresolved', 'search', 'read decisive', 'inspect', 'terminology',
                        'original/primary/direct', 'corroboration/counterevidence', 'coverage', 'stop_condition']:
            self.assertIn(concept, loop)
        obs = POLICY['execution_observability']
        self.assertIn('outranks contradictory retrospective model self-report', obs['precedence'])
        self.assertIn('USER_REPORTED', obs['precedence'])
        for value in ['INTENDED ACTION != ACTUAL EXECUTION', 'ACTUAL EXECUTION != SOURCE READ',
                      'SOURCE READ != CLAIM SUPPORT']:
            self.assertIn(value, obs['invariants'])
        self.assertIn('per-action execution status and evidence basis', POLICY['return_contract'])
        self.assertIn('executor actually observed as used or UNKNOWN', POLICY['return_contract'])
        self.assertIn('resource/fallback effects materially changing coverage', POLICY['return_contract'])
        self.assertIn('Never promote unresolved to verified', POLICY['stages']['COVERAGE_SUPPORT_CHECK'])

    def test_case_inventory_utf8_and_candidate_whitespace(self):
        spec = (CANDIDATE / 'RESEARCH_CORE_TEST_CASES.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (RC\d+) \|', spec, re.M), [f'RC{n:02}' for n in range(1, 27)])
        self.assertTrue((CANDIDATE / '../../tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md').resolve().is_file())
        for path in [*CANDIDATE.iterdir(), Path(__file__)]:
            if not path.is_file():
                continue
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b'\xef\xbb\xbf'))
            text = raw.decode('utf-8')
            self.assertNotIn('\r', text)
            self.assertTrue(text.endswith('\n'))
            self.assertTrue(all(line == line.rstrip() for line in text.splitlines()))


class AISResearchSpecFixtures(unittest.TestCase):
    def setUp(self):
        self.lanes = {lane: lane_state() for lane in ['CHAT_GUIDED', 'DEEP_RESEARCH', 'WORK']}

    def test_RC01_direct_search_outranks_retrospective_denial(self):
        self.assertEqual(execution_oracle([('search', 1, 'DIRECT_EXECUTION_TRACE')],
                                         retrospective='NOT_EXECUTED'), 'EXECUTED')

    def test_RC02_unobserved_is_unknown(self):
        for report in ['EXECUTED', 'NOT_EXECUTED', None]:
            self.assertEqual(execution_oracle(retrospective=report), 'UNKNOWN')

    def test_RC03_search_execution_is_not_source_read(self):
        trace = [('search', 1, 'DIRECT_EXECUTION_TRACE')]
        self.assertEqual(execution_oracle(trace), 'EXECUTED')
        self.assertEqual(execution_oracle(trace, action='read'), 'UNKNOWN')
        self.assertEqual(supported_claim(), 'UNRESOLVED')

    def test_RC04_bounded_baseline(self):
        result = strategy_oracle(lanes=self.lanes)
        self.assertEqual((result['quality'], result['selected']), ('NORMAL', 'CHAT_GUIDED'))

    def test_RC05_broad_deep_synthesis(self):
        result = strategy_oracle(shape='broad_synthesis', depth=True, lanes=self.lanes)
        self.assertEqual((result['quality'], result['selected']), ('EXTENSIVE', 'DEEP_RESEARCH'))
        self.assertEqual((result['observed_used'], result['actual_calls']), ('UNKNOWN', 0))

    def test_RC06_workflow_deliverable(self):
        self.assertEqual(strategy_oracle(shape='workflow', lanes=self.lanes)['selected'], 'WORK')

    def test_RC07_unknown_quota_bounded(self):
        self.lanes['CHAT_GUIDED']['resource'] = 'UNKNOWN'
        result = strategy_oracle(lanes=self.lanes)
        self.assertEqual((result['selected'], result['resource']), ('CHAT_GUIDED', 'UNKNOWN'))

    def test_RC08_explicit_depth_and_usable_capacity(self):
        result = strategy_oracle(depth=True, named='DEEP_RESEARCH', lanes=self.lanes)
        self.assertEqual((result['quality'], result['selected']), ('THOROUGH', 'DEEP_RESEARCH'))
        self.assertEqual(strategy_oracle(depth=True, lanes=self.lanes)['quality'], 'THOROUGH')

    def test_RC09_selected_without_launch_is_not_execution(self):
        self.lanes['DEEP_RESEARCH']['launch'] = False
        result = strategy_oracle(shape='broad_synthesis', lanes=self.lanes)
        self.assertEqual((result['preferred'], result['selected']), ('DEEP_RESEARCH', 'CHAT_GUIDED'))
        self.assertEqual(result['actual_calls'], 0)
        self.assertEqual(execution_oracle([('search', 1, 'SELECTED_EXECUTOR')]), 'UNKNOWN')

    def test_RC10_fallback_retains_supported_branches_and_reads(self):
        branches = {'A': dict(supported=True, reads=['source-A'], finding='bounded-A'),
                    'B': dict(supported=False, reads=[])}
        before = copy.deepcopy(branches)
        retained, unresolved = fallback_oracle(branches)
        self.assertEqual(retained, {'A': branches['A']})
        self.assertEqual(unresolved, {'B'})
        self.assertEqual(branches, before)
        self.assertIn('re-plan unresolved needs', POLICY['failures']['executor_failure'])

    def test_RC11_project_context_requires_bounded_handoff(self):
        self.lanes['WORK']['transition'] = 'PROJECT_CONTEXT_AVAILABLE'
        result = strategy_oracle(shape='workflow', lanes=self.lanes)
        self.assertTrue(result['needs_handoff'])
        self.assertEqual(set(POLICY['research_policy']['bounded_handoff']), {
            'research objective', 'protected state', 'completed evidence', 'sources actually read',
            'unresolved evidence tasks', 'source roles/authority requirements', 'completion criteria', 'fallback'})
        rule = POLICY['research_policy']['work_transition']['PROJECT_CONTEXT_AVAILABLE']
        self.assertIn('direct same-thread transfer is not established', rule)
        self.assertIn('not proof of task creation or history transfer', rule)

    def test_RC12_direct_transition_is_runtime_scoped(self):
        result = strategy_oracle(shape='workflow', lanes=self.lanes)
        self.assertEqual(result['selected'], 'WORK')
        self.assertFalse(result['needs_handoff'])
        rule = POLICY['research_policy']['work_transition']['DIRECT_OBSERVED']
        self.assertIn('on that runtime/surface', rule)
        self.assertIn('Do not generalize', rule)
        self.lanes['WORK']['transition'] = 'UNKNOWN'
        self.assertEqual(strategy_oracle(shape='workflow', lanes=self.lanes)['selected'], 'CHAT_GUIDED')

    def test_RC13_forum_alone_is_not_capability(self):
        for lane, shape in [('WORK', 'workflow'), ('DEEP_RESEARCH', 'broad_synthesis')]:
            self.lanes[lane]['basis'] = 'COMMUNITY_REPORT'
            self.assertEqual(strategy_oracle(shape=shape, lanes=self.lanes)['selected'], 'CHAT_GUIDED')

    def test_RC14_conserve_quota_keeps_quality_target(self):
        result = strategy_oracle(shape='broad_synthesis', depth=True, conserve=True, lanes=self.lanes)
        self.assertEqual((result['quality'], result['selected']), ('EXTENSIVE', 'CHAT_GUIDED'))

    def test_RC15_verified_labels_cannot_replace_decisive_reads(self):
        for label in ['WORK_VERIFIED', 'DEEP_RESEARCH_VERIFIED']:
            self.assertEqual(supported_claim(label=label), 'UNRESOLVED')
            self.assertEqual(supported_claim(['A'], ['B'], label), 'UNRESOLVED')
        self.assertEqual(supported_claim(['A'], ['A']), 'SUPPORTED')
        self.assertIn('verified labels cannot replace inaccessible', POLICY['stages']['RESEARCH_EXECUTION'])

    def test_RC16_pure_broad_research_does_not_prefer_work(self):
        self.assertEqual(strategy_oracle(shape='broad_synthesis', lanes=self.lanes)['preferred'], 'DEEP_RESEARCH')

    def test_RC17_workflow_does_not_prefer_deep_research(self):
        self.assertEqual(strategy_oracle(shape='workflow', depth=True, lanes=self.lanes)['preferred'], 'WORK')

    def test_RC18_exhaustion_reduces_breadth_not_evidence_standard(self):
        self.lanes['DEEP_RESEARCH']['resource'] = 'EXHAUSTED'
        result = strategy_oracle(shape='broad_synthesis', lanes=self.lanes)
        self.assertEqual((result['quality'], result['selected']), ('EXTENSIVE', 'CHAT_GUIDED'))
        self.assertEqual(supported_claim(label='FALLBACK_COMPLETE'), 'UNRESOLVED')
        self.assertIn('EXECUTOR DOWNGRADE != EVIDENCE-DISCIPLINE DOWNGRADE',
                      POLICY['research_policy']['fallback_invariants'])
        self.test_RC10_fallback_retains_supported_branches_and_reads()

    def test_RC19_query_refinement_retains_scope(self):
        self.assertIn('Query refinement for same target retains', POLICY['stages']['TOOL_FACING_INSTRUCTION'])
        self.assertIn('Same-target query refinement retains scope', POLICY['stages']['PRE_CALL_CHECK'])

    def test_RC20_material_expansion_rebuilds_affected_lock_and_strategy(self):
        stage = POLICY['stages']['PRE_CALL_CHECK']
        self.assertIn('material expansion rebuilds affected contract/strategy', stage)
        self.assertIn('INPUT_VALIDATION and Hub authorization', stage)
        self.assertIn('rerouting does not self-authorize', POLICY['stages']['SEARCH_SCOPE_LOCK'])

    def test_RC21_conflicting_direct_traces_unresolved_per_attempt(self):
        traces = [('search', 1, 'DIRECT_EXECUTION_TRACE'), ('search', 1, 'PRE_SUBMISSION_BLOCK')]
        self.assertEqual(execution_oracle(traces), 'CONFLICTED')
        traces[1] = ('search', 2, 'PRE_SUBMISSION_BLOCK')
        self.assertEqual(execution_oracle(traces), 'EXECUTED')
        self.assertEqual(execution_oracle(traces, attempt=2), 'NOT_EXECUTED')

    def test_RC22_non_execution_requires_positive_direct_evidence(self):
        for kind in ['DIRECT_NON_EXECUTION_TRACE', 'PRE_SUBMISSION_BLOCK', 'UNAVAILABLE_EXECUTOR']:
            self.assertEqual(execution_oracle([('search', 1, kind)]), 'NOT_EXECUTED')

    def test_RC23_post_submission_timeout_is_unknown(self):
        self.assertEqual(execution_oracle([('search', 1, 'SUBMITTED'), ('search', 1, 'TIMEOUT')]), 'UNKNOWN')
        self.assertIn('failure/timeout after submission leaves execution UNKNOWN',
                      POLICY['execution_observability']['trace_limits'])

    def test_RC24_named_executor_failure_without_fallback(self):
        self.lanes['WORK']['availability'] = 'UNAVAILABLE'
        result = strategy_oracle(named='WORK', lanes=self.lanes, fallback_allowed=False)
        self.assertEqual((result['preferred'], result['selected']), ('WORK', 'UNRESOLVED'))
        self.assertIn('If fallback is forbidden, stop dependent work',
                      POLICY['research_policy']['lane_selection']['named_executor'])

    def test_RC25_unknown_low_resources_and_no_authorization(self):
        self.lanes['DEEP_RESEARCH']['resource'] = 'UNKNOWN'
        result = strategy_oracle(shape='broad_synthesis', depth=True, lanes=self.lanes)
        self.assertEqual((result['selected'], result['resource']), ('DEEP_RESEARCH', 'UNKNOWN'))
        self.lanes['DEEP_RESEARCH']['resource'] = 'LOW'
        self.assertEqual(strategy_oracle(shape='broad_synthesis', lanes=self.lanes)['selected'], 'CHAT_GUIDED')
        self.assertEqual(strategy_oracle(shape='broad_synthesis', lanes=self.lanes,
                                        low_bounded=True)['selected'], 'DEEP_RESEARCH')
        self.assertEqual(strategy_oracle(lanes=self.lanes, authorized=False)['selected'], 'UNRESOLVED')
        self.assertEqual(strategy_oracle(shape='broad_synthesis', lanes=self.lanes,
                                        material_benefit=False, low_bounded=True)['selected'], 'CHAT_GUIDED')

    def test_RC26_no_remaining_executor_means_no_fabricated_fallback(self):
        self.lanes['DEEP_RESEARCH']['availability'] = 'UNKNOWN'
        self.lanes['CHAT_GUIDED']['availability'] = 'UNAVAILABLE'
        result = strategy_oracle(shape='broad_synthesis', lanes=self.lanes)
        self.assertEqual((result['selected'], result['actual_calls']), ('UNRESOLVED', 0))


if __name__ == '__main__':
    unittest.main()
