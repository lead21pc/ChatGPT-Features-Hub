"""Static contract checks and declared semantic fixtures, never a runtime AIS executor.

These oracles do not interpret natural language, launch tools, transfer chats,
or establish model compliance. RC fixtures encode already-classified task shapes.
"""
import copy
import hashlib
from pathlib import Path
import re
import unittest

from test_hub_contracts import load, historical_source
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tool_pipelines/AIS'
POLICY = load(BASE / 'AIS_ROUTER_v1.2.yaml')

# Captured before this task's edits, from the clean local 603bd01 working tree.
BASELINE = {
    'HUB_CI_v1.1.md': '7bb946874663627060d28e47674decb07ba99f51acbffb6550db98d65746157b',
    # Refreshed only for the authorized Library identity correction; AIS owners are unchanged.
    'HUB_ROUTER_v1.1.yaml': 'b63baa9a9461b90f12c61b35dbe572270ac16826e38c66f8a95128ad32e705de',
    'HUB_ARCHITECTURE_v1.0.md': 'da62208fd10ed46d2a453fb72c55a0475185583d107edc2196b5b503eae738b5',
    'tool_pipelines/AIS/AIS_PIPELINE_v1.0.md': 'c7f78f10be855d6b77aa3e0bbf67c3856c7fa42f890382752056de71abd10f69',
    'tool_pipelines/AIS/AIS_ROUTER_v1.1.yaml': 'ea5e22648fdcb1da239126ec25220b474444de11521887cd93711f41b4b32901',
    'tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md': '3519fd3f596043e157b987129afbd51872f991faf889fb91162ac754f51529d3',
    # Refreshed for package-local trigger ownership metadata; AIS contracts are unchanged.
    'tests/HUB_ROUTE_TEST_CASES.md': '094966e895ed06406a97cdd66ad1e3d1a473117ef0cb32d3d95b57e6180ff745',
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


def depth_oracle(explicit_depth=False, broad=False, multiple_material_claims=False):
    """Declared semantic depth fixture only; no language parser or product selection."""
    return 'EXTENSIVE' if broad else 'THOROUGH' if explicit_depth or multiple_material_claims else 'NORMAL'


def completion_oracle(required, supported, decisive_gaps=(), limit_reached=False):
    """Expected bounded evidence coverage, never an actual model/search executor."""
    missing = set(required) - set(supported)
    gaps = missing | set(decisive_gaps)
    return dict(return_to_hub=not gaps or limit_reached,
                supported=set(supported), unresolved=gaps,
                sufficient=not gaps)


def supported_claim(decisive_reads=(), supporting_reads=(), label=None):
    """A verified label cannot create the missing decisive read/support relation."""
    return 'SUPPORTED' if set(decisive_reads).intersection(supporting_reads) else 'UNRESOLVED'


def fallback_oracle(branches):
    """Retain supported branches; only unresolved/invalidated branches need work."""
    retained = {k: copy.deepcopy(v) for k, v in branches.items()
                if v['supported'] and not v.get('invalidated')}
    return retained, set(branches) - set(retained)


class AISResearchStaticTests(unittest.TestCase):
    def test_official_pair_stage_order_and_unchanged_owners(self):
        old = load(historical_source('tool_pipelines/AIS/AIS_ROUTER_v1.1.yaml'))
        self.assertEqual(POLICY['status'], 'ACTIVE')
        self.assertTrue(POLICY['active'])
        self.assertEqual(POLICY['router_version'], '1.2')
        self.assertEqual(POLICY['deployment'], 'REPOSITORY_ACTIVE; PROJECT_DEPLOYMENT_NOT_PERFORMED')
        self.assertEqual(POLICY['live_verification'], 'NOT_RUN')
        sequence = POLICY['stage_sequence']
        self.assertEqual(sequence, list(POLICY['stages']))
        self.assertEqual([s for s in sequence if s != 'RESEARCH_STRATEGY'], old['stage_sequence'])
        self.assertEqual(sequence[2:5], ['SOURCE_AUTHORITY_GATE', 'RESEARCH_STRATEGY', 'TOOL_FACING_INSTRUCTION'])
        for key in ['modes', 'mode_resolution', 'source_policy', 'execution_observability']:
            comparison = old if key in old else load(
                ROOT / 'Source_archive/AIS research-core promotion 2026-10-21/candidates/ais_research_core/AIS_ROUTER_v1.2-candidate.yaml')
            self.assertEqual(POLICY[key], comparison[key])
        old_lock = copy.deepcopy(POLICY['search_contract'])
        strategy = old_lock.pop('research_strategy')
        self.assertEqual(old_lock, old['search_contract'])
        self.assertEqual(set(strategy), {'quality_target', 'coverage_expectations'})
        for owner in ['hub', 'hub_router', 'platform', 'evidence']:
            self.assertEqual(POLICY['ownership'][owner], old['ownership'][owner])
        pipeline = (BASE / 'AIS_PIPELINE_v1.1.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'`(AIS_ROUTER_[^`]+\.yaml)`', pipeline), ['AIS_ROUTER_v1.2.yaml'])
        self.assertIn('Status: ACTIVE', pipeline)
        self.assertIn('without reassessing the whole turn', pipeline)
        catalog = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        ais = next(p for p in catalog['packages'] if p['package_id'] == 'HUB-PKG-AIS')
        self.assertEqual(ais['version'], '1.1')
        self.assertEqual(ais['binding_mode'], 'LEGACY_PROJECT_SOURCE')
        self.assertEqual(ais['location']['declared_source_path'], 'tool_pipelines/AIS/AIS_PIPELINE_v1.1.md')
        self.assertEqual(ais['location']['source_name'], 'AIS_PIPELINE_v1.1.md')
        self.assertEqual(ais['project_deployment'], 'NOT_PERFORMED')
        self.assertNotIn('Source_archive', str(ais))
        self.assertEqual(list(BASE.glob('AIS_PIPELINE_v*.md')), [BASE / 'AIS_PIPELINE_v1.1.md'])
        self.assertEqual(list(BASE.glob('AIS_ROUTER_v*.yaml')), [BASE / 'AIS_ROUTER_v1.2.yaml'])
        self.assertFalse((ROOT / 'candidates/ais_research_core/AIS_PIPELINE_v1.1-candidate.md').exists())
        self.assertFalse((ROOT / 'candidates/ais_research_core/AIS_ROUTER_v1.2-candidate.yaml').exists())

    def test_predecessors_archived_exact_and_28_acceptance_criteria_preserved(self):
        for name, sha in BASELINE.items():
            if name == 'tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md':
                continue  # Only AIS-22's exact current router filename changes below.
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256(historical_source(name).read_bytes()).hexdigest(), sha)
        original = (BASE / 'tests/ROUTE_TEST_CASES.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (AIS-\d+) \|', original, re.M),
                         [f'AIS-{n:02}' for n in range(1, 29)])
        old_name = original.replace('AIS_ROUTER_v1.2.yaml', 'AIS_ROUTER_v1.1.yaml')
        self.assertEqual(hashlib.sha256(old_name.encode()).hexdigest(),
                         BASELINE['tool_pipelines/AIS/tests/ROUTE_TEST_CASES.md'])
        receipt = json.loads((ROOT / 'Source_archive/AIS_PROMOTION_ARCHIVE_RECEIPT_2026-10-21.json').read_text(encoding='utf-8'))
        self.assertEqual(len(receipt), 7)
        for row in receipt:
            self.assertFalse((ROOT / row['old']).exists())
            self.assertEqual(hashlib.sha256((ROOT / row['archive']).read_bytes()).hexdigest(), row['sha256'])

    def test_contract_gates_loop_return_and_evidence_limits(self):
        p = POLICY['research_policy']
        self.assertEqual(set(p['quality_targets']), {'NORMAL', 'THOROUGH', 'EXTENSIVE'})
        # The rejected orchestrator is removed, not relocated to another policy field.
        for field in ['lane_selection', 'resource_states', 'availability_states', 'work_transition',
                      'bounded_handoff', 'launch_required', 'chat_guided_loop']:
            self.assertNotIn(field, p)
        for field in ['preferred_executor', 'selected_executor', 'observed_executor_state',
                      'resource_state', 'work_transition', 'task_shape', 'fallback']:
            self.assertNotIn(field, POLICY['search_contract']['research_strategy'])
        for field in ['quality target', 'coverage expectations', 'tool availability/access',
                      'protected state', 'stop_condition', 'authorization']:
            self.assertIn(field, POLICY['stages']['PRE_CALL_CHECK'])
        self.assertIn('No executor selection', POLICY['stages']['RESEARCH_STRATEGY'])
        self.assertIn('without literal trigger matching', p['depth_request'])
        loop = ' '.join(p['guided_research_loop'])
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
        self.assertIn('tool/access limits materially changing coverage', POLICY['return_contract'])
        self.assertIn('Never promote unresolved to verified', POLICY['stages']['COVERAGE_SUPPORT_CHECK'])
        self.assertNotIn('executor_failure', POLICY['failures'])
        self.assertIn('tool_failure', POLICY['failures'])

    def test_case_inventory_utf8_and_official_whitespace(self):
        spec = (BASE / 'tests/RESEARCH_CORE_TEST_CASES.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (RC\d+) \|', spec, re.M), [f'RC{n:02}' for n in range(1, 27)])
        self.assertTrue((BASE / 'tests/ROUTE_TEST_CASES.md').is_file())
        for path in [*BASE.glob('AIS_*.*'), BASE / 'tests/RESEARCH_CORE_TEST_CASES.md', Path(__file__)]:
            if not path.is_file():
                continue
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b'\xef\xbb\xbf'))
            text = raw.decode('utf-8')
            self.assertNotIn('\r', text)
            self.assertTrue(text.endswith('\n'))
            self.assertTrue(all(line == line.rstrip() for line in text.splitlines()))


class AISResearchSpecFixtures(unittest.TestCase):
    def test_RC01_direct_trace_outranks_retrospective_denial(self):
        self.assertEqual(execution_oracle([('search', 1, 'DIRECT_EXECUTION_TRACE')],
                                         retrospective='NOT_EXECUTED'), 'EXECUTED')

    def test_RC02_missing_trace_is_unknown(self):
        for report in ['EXECUTED', 'NOT_EXECUTED', None]:
            self.assertEqual(execution_oracle(retrospective=report), 'UNKNOWN')

    def test_RC03_execution_read_and_support_are_distinct(self):
        trace = [('search', 1, 'DIRECT_EXECUTION_TRACE')]
        self.assertEqual(execution_oracle(trace), 'EXECUTED')
        self.assertEqual(execution_oracle(trace, action='read'), 'UNKNOWN')
        self.assertEqual(supported_claim(), 'UNRESOLVED')
        self.assertEqual(supported_claim(['A'], ['B']), 'UNRESOLVED')
        self.assertEqual(supported_claim(['A'], ['A']), 'SUPPORTED')

    def test_RC04_normal_guided_research_loop(self):
        self.assertEqual(depth_oracle(), 'NORMAL')
        self.assertIn('native Chat search/read tools', POLICY['stages']['RESEARCH_EXECUTION'])
        self.assertIn('guided_research_loop', POLICY['stages']['RESEARCH_EXECUTION'])

    def test_RC05_thorough_uses_normal_chat_search_read(self):
        self.assertEqual(depth_oracle(explicit_depth=True), 'THOROUGH')
        self.assertIn('Ordinary Chat search/read can meet any of these depth targets',
                      POLICY['research_policy']['depth_request'])
        self.assertIn('source comparison', POLICY['research_policy']['quality_targets']['THOROUGH'])

    def test_RC06_extensive_uses_normal_chat_search_read(self):
        self.assertEqual(depth_oracle(broad=True), 'EXTENSIVE')
        self.assertIn('repeated guided search/read',
                      POLICY['research_policy']['quality_targets']['EXTENSIVE'])

    def test_RC07_semantic_depth_influences_evidence_not_answer_length(self):
        # Semantic intent is supplied as a fixture, never interpreted by a string matcher.
        self.assertEqual(depth_oracle(explicit_depth=True), 'THOROUGH')
        self.assertEqual(depth_oracle(multiple_material_claims=True), 'THOROUGH')
        p = POLICY['research_policy']['depth_request']
        self.assertIn('without literal trigger matching', p)
        self.assertIn('evidence collection, support checks and stopping expectations', p)
        self.assertIn('not merely answer length', p)

    def test_RC08_broad_research_does_not_launch_deep_research(self):
        self.assertEqual(depth_oracle(explicit_depth=True, broad=True), 'EXTENSIVE')
        self.assertNotIn('lane_selection', POLICY['research_policy'])
        self.assertIn('does not automatically select, launch or transfer',
                      POLICY['research_policy']['explicit_product_request'])

    def test_RC09_multistep_work_does_not_launch_work(self):
        self.assertNotIn('work_transition', POLICY['research_policy'])
        self.assertNotIn('selected_executor', POLICY['search_contract']['research_strategy'])
        self.assertIn('No executor selection', POLICY['stages']['RESEARCH_STRATEGY'])

    def test_RC10_sufficient_evidence_returns_to_hub(self):
        result = completion_oracle({'A', 'B'}, {'A', 'B'})
        self.assertTrue(result['sufficient'])
        self.assertTrue(result['return_to_hub'])
        self.assertFalse(result['unresolved'])
        self.assertIn('Stop when scoped evidence is sufficient', POLICY['stages']['RESEARCH_EXECUTION'])

    def test_RC11_limit_with_gaps_returns_honest_partial_output(self):
        result = completion_oracle({'A', 'B'}, {'A'}, limit_reached=True)
        self.assertTrue(result['return_to_hub'])
        self.assertFalse(result['sufficient'])
        self.assertEqual(result['unresolved'], {'B'})
        self.assertIn('exhausting a limit does not prove sufficiency',
                      POLICY['stages']['COVERAGE_SUPPORT_CHECK'])

    def test_RC12_decisive_gaps_do_not_erase_supported_independent_work(self):
        result = completion_oracle({'A'}, {'A'}, decisive_gaps={'B'}, limit_reached=True)
        self.assertEqual(result['supported'], {'A'})
        self.assertEqual(result['unresolved'], {'B'})
        self.assertIn('block dependent conclusions only', POLICY['failures']['decisive_gap'])

    def test_RC13_unavailable_tool_is_not_fabricated_execution(self):
        self.assertIn('actual tool availability/access', POLICY['stages']['PRE_CALL_CHECK'])
        self.assertEqual(execution_oracle([('search', 1, 'UNAVAILABLE_EXECUTOR')]), 'NOT_EXECUTED')
        self.assertIn('otherwise stop and return gaps', POLICY['failures']['tool_failure'])

    def test_RC14_post_submission_timeout_does_not_prove_nonexecution(self):
        self.assertEqual(execution_oracle([('search', 1, 'SUBMITTED'), ('search', 1, 'TIMEOUT')]), 'UNKNOWN')
        self.assertIn('failure/timeout after submission leaves execution UNKNOWN',
                      POLICY['execution_observability']['trace_limits'])

    def test_RC15_conflicting_direct_traces_remain_conflicted_per_attempt(self):
        trace = [('search', 1, 'DIRECT_EXECUTION_TRACE'), ('search', 1, 'PRE_SUBMISSION_BLOCK')]
        self.assertEqual(execution_oracle(trace), 'CONFLICTED')
        trace[1] = ('search', 2, 'PRE_SUBMISSION_BLOCK')
        self.assertEqual(execution_oracle(trace), 'EXECUTED')
        self.assertEqual(execution_oracle(trace, attempt=2), 'NOT_EXECUTED')

    def test_RC16_nonexecution_requires_positive_evidence(self):
        for kind in ['DIRECT_NON_EXECUTION_TRACE', 'PRE_SUBMISSION_BLOCK', 'UNAVAILABLE_EXECUTOR']:
            self.assertEqual(execution_oracle([('search', 1, kind)]), 'NOT_EXECUTED')

    def test_RC17_explicit_product_requests_do_not_grant_imaginary_launches(self):
        p = POLICY['research_policy']['explicit_product_request']
        self.assertIn('may be explicitly requested', p)
        self.assertIn('actually available authorized platform surface', p)
        self.assertIn('do not silently substitute', p)
        self.assertIn('without corresponding direct evidence', p)
        self.assertEqual(execution_oracle([('search', 1, 'REQUESTED')]), 'UNKNOWN')

    def test_RC18_entitlement_or_forum_is_not_observed_tool_capability(self):
        p = POLICY['research_policy']['tool_availability']
        self.assertIn('subscription entitlement or community report proves no actual execution capability', p)
        self.assertIn('no invented search/read', p)

    def test_RC19_tool_failure_preserves_evidence_conditions_and_replans_only_gaps(self):
        branches = {'A': dict(supported=True, reads=['A'], conditions='region/time/version'),
                    'B': dict(supported=True, reads=['B'], invalidated=True),
                    'C': dict(supported=False, reads=['C'])}
        before = copy.deepcopy(branches)
        retained, unresolved = fallback_oracle(branches)
        self.assertEqual(retained, {'A': before['A']})
        self.assertEqual(unresolved, {'B', 'C'})
        self.assertEqual(branches, before)
        self.assertIn('do not restart valid completed research', POLICY['failures']['tool_failure'])
        self.assertIn('retain the quality target and evidence standard', POLICY['failures']['tool_failure'])

    def test_RC20_query_refinement_retains_scope(self):
        self.assertIn('Query refinement for the same target retains scope',
                      POLICY['stages']['TOOL_FACING_INSTRUCTION'])
        self.assertIn('Same-target query refinement retains scope', POLICY['stages']['PRE_CALL_CHECK'])

    def test_RC21_material_scope_change_rebuilds_affected_contract(self):
        self.assertIn('material expansion rebuilds affected contract/strategy',
                      POLICY['stages']['PRE_CALL_CHECK'])
        self.assertIn('INPUT_VALIDATION and Hub authorization', POLICY['stages']['PRE_CALL_CHECK'])
        self.assertIn('rerouting does not self-authorize', POLICY['stages']['SEARCH_SCOPE_LOCK'])

    def test_RC22_components_do_not_automatically_support_combination(self):
        p = POLICY['stages']['EVIDENCE_MERGE']
        self.assertIn('SUPPORTED COMPONENTS DO NOT AUTOMATICALLY SUPPORT THEIR COMBINATION', p)
        self.assertIn('unless the relation between A and B is itself supported', p)

    def test_RC23_protected_state_cannot_be_silently_rewritten(self):
        p = POLICY['stages']['EVIDENCE_MERGE']
        self.assertIn('preserve protected state', p)
        self.assertIn('without silently changing state', p)
        self.assertIn('Update only', p)

    def test_RC24_verified_label_without_decisive_read_stays_unresolved(self):
        for label in ['Work verified', 'Deep Research verified', 'previously verified']:
            self.assertEqual(supported_claim(label=label), 'UNRESOLVED')
        for action in ['search', 'open', 'find']:
            self.assertEqual(execution_oracle([(action, 1, 'DIRECT_EXECUTION_TRACE')], action=action), 'EXECUTED')
        self.assertIn('verified labels cannot replace inaccessible decisive sources',
                      POLICY['stages']['RESEARCH_EXECUTION'])

    def test_RC25_hub_retains_activation_and_original_workflow(self):
        self.assertEqual(POLICY['ownership']['hub_router'], 'Select AIS only for the relevant task portion.')
        self.assertIn('No self-activation, whole-turn reassessment', POLICY['ownership']['router'])
        self.assertIn('so Hub can resume the original work', POLICY['stages']['COVERAGE_SUPPORT_CHECK'])
        self.assertIn('Do not repeat whole-turn', POLICY['stages']['INPUT_VALIDATION'])

    def test_RC26_only_material_unresolved_needs_continue_within_limit(self):
        result = completion_oracle({'A', 'B'}, {'A'})
        self.assertFalse(result['return_to_hub'])
        self.assertEqual(result['unresolved'], {'B'})
        loop = POLICY['research_policy']['guided_research_loop']
        self.assertIn('repeat only for a material unresolved need within stop_condition', loop)
        self.assertIn('reporting any unmet depth', POLICY['stages']['RESEARCH_STRATEGY'])


if __name__ == '__main__':
    unittest.main()
