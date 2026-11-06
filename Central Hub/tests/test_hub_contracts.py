"""Static checks and test-only inventory/approval oracles; never model/tool execution."""
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / 'tool_pipelines/ImageT'

# Explicit historical mapping for archive verification only; never runtime fallback.
LEGACY_ARCHIVE = ROOT / 'Source_archive/Central Hub legacy v1.0'
LEGACY_PATHS = frozenset(['HUB_CI_v1.0.md', 'HUB_ROUTER_v1.0.yaml', 'domains/technical/TECHNICAL_v1.0.md', 'domains/creative/CREATIVE_v1.0.md', 'capabilities/BRAINSTORM_v1.0.md'])

AIS_ARCHIVE = ROOT / 'Source_archive/AIS research-core promotion 2026-10-21'
AIS_PREDECESSORS = frozenset(['tool_pipelines/AIS/AIS_PIPELINE_v1.0.md', 'tool_pipelines/AIS/AIS_ROUTER_v1.1.yaml'])

CONCEPT_ARCHIVE = ROOT / 'Source_archive/Concept development migration 2026-10-26'
CONCEPT_PREDECESSORS = frozenset(['HUB_ARCHITECTURE_v1.0.md', 'HUB_PACKAGE_CATALOG_v1.0.yaml',
    'HUB_ROUTER_v1.1.yaml', 'HUB_LIBRARY_SINGLETON_MIGRATION.md',
    'library_modules/HUB-DOM-CREATIVE_v1.0.md', 'library_modules/HUB-CAP-BRAINSTORM_v1.0.md'])

SHOPPING_PREDECESSOR = ROOT / 'Source_archive/Shopping 1.0 promotion 2026-11-06'


def historical_source(path):
    if path == 'tests/HUB_ROUTE_TEST_CASES.md':
        return ROOT / 'Source_archive/Concept explicit leaf controls 2026-11-02' / path
    if path in {'tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md', 'tool_pipelines/ImageT/manifest.yaml'}:
        return ROOT / 'Source_archive/ImageT Open Gate promotion 2026-10-29' / path
    if path in CONCEPT_PREDECESSORS:
        return CONCEPT_ARCHIVE / path  # Historical assertions only, never active resolution.
    if path in AIS_PREDECESSORS:
        return AIS_ARCHIVE / path  # Explicit history checks only, never runtime fallback.
    return LEGACY_ARCHIVE / path if path in LEGACY_PATHS else ROOT / path



class Closed(ValueError):
    pass


class StrictLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key == '<<' or key in result:
                raise Closed('duplicate or merge key')
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def parse(text):
    for event in yaml.parse(text):
        if isinstance(event, yaml.AliasEvent) or getattr(event, 'anchor', None):
            raise Closed('anchor/alias')
    for token in yaml.scan(text):
        if isinstance(token, yaml.TagToken):
            raise Closed('explicit tag')
        if isinstance(token, yaml.ScalarToken) and token.plain:
            if token.value.lower() in {'yes', 'no', 'on', 'off', 'false', 'true', 'null', '~'}:
                if token.value not in {'true', 'false', 'null'}:
                    raise Closed('ambiguous scalar')
            if re.match(r'^\d{4}-\d{2}-\d{2}', token.value):
                raise Closed('implicit date')
    return yaml.load(text, Loader=StrictLoader)


def load(path):
    return parse(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_source(entry):
    path = (IMAGE / entry['local_path']).resolve()
    if not path.is_relative_to(IMAGE) or any(p.lower() == 'source_archive' for p in path.parts):
        raise Closed('outside active sources')
    try:
        actual_digest = digest(path) if path.is_file() else None
    except OSError as error:
        raise Closed(f'unreadable source: {entry["file"]}') from error
    if path.name != entry['file'] or actual_digest != entry['sha256']:
        raise Closed('missing/nonexact/corrupt source')
    if path.suffix == '.md':
        text = path.read_text(encoding='utf-8')
        versions = re.findall(r'^(?:IMAGE_CONTROLLER|READY_GATE|ANTI_PRIOR|CONFIG|PREFERENCE)_VERSION: (.+)$', text, re.M)
        if versions != [entry['version']] or f"STATUS: {entry['status'].upper()}" not in text:
            raise Closed('header mismatch')
    return path


def image_oracle(manifest, router, operation='create', selection=None, unexpected_template=False):
    """Acceptance oracle only; does not run the instructional router or ChatGPT."""
    if manifest['format_version'] != router['manifest_contract']['format_version']:
        raise Closed('manifest contract mismatch')
    if operation not in router['operations']:
        raise Closed('unknown operation')
    active = manifest['controllers']['active']
    if selection not in {None, active['id']}:
        raise Closed('no selectable experiment in this release')
    if active['status'] != 'active':
        raise Closed('inactive controller')
    verify_source(active)
    generation = operation in {'create', 'edit', 'variation', 'correct'}
    if generation:
        if 'ready_gate' not in active['compatibility'] or 'ready_gate' not in manifest['artifacts']:
            raise Closed('missing Ready Gate dependency')
        if operation not in router['generation_dependencies']['operations']:
            raise Closed('generation route bypass')
        if router['execution']['ready_gate'] != 'manifest_selected_ready_gate_contract':
            raise Closed('missing Ready Gate delegation')
    for role, version in active['compatibility'].items():
        if role == 'ready_gate' and not generation:
            continue
        entry = manifest['artifacts'][role]
        if entry['version'] != version or entry['status'] != 'active' or not entry['required']:
            raise Closed('incompatible module')
        verify_source(entry)
    if manifest['artifacts']['router']['version'] != router['router_version']:
        raise Closed('router inventory mismatch')
    template = manifest['artifacts']['visual_template']
    if template['status'] == 'optional_absent':
        if template['file'] is not None or template['required'] or unexpected_template:
            raise Closed('inconsistent template inventory')
    elif template['status'] == 'active':
        verify_source(template)
    else:
        raise Closed('invalid template status')
    return {'selected': active['id'], 'after_prompt_gate': 'analyze_only' if operation == 'analyze' else 'PENDING_APPROVAL',
            'preference_active': False, 'tool_called': False}


def approval_oracle(state, event, same_snapshot=True):
    """Expected Ready Gate transitions only; no language interpretation/backend state."""
    if not same_snapshot or event == 'lost_context':
        return 'STALE', False
    if event in {'revision', 'yes_but'}:
        return 'REVISION_REQUIRED', False
    if event == 'approve_current' and state == 'PENDING_APPROVAL':
        return 'APPROVED', False
    if event == 'submit' and state == 'APPROVED':
        return 'CONSUMED', True
    if event == 'question':
        return state, False
    return 'PENDING_APPROVAL', False


def open_gate_oracle(*, payload, current_user_preservation=False, signal_in_data=False,
                     reference_asset=None, reference_role=None, requires_semantic_choice=False):
    """Candidate contract oracle only; fixture metadata supplies authority, never language recognition."""
    authority = 'PRESERVED_AUTHORED' if current_user_preservation else 'RAW'
    result = {
        'authority': authority,
        'semantic_payload': payload,
        'open_gate_confirmation': False,
        'execution_adaptations': [],
        'ready_eligible': True,
        'action': 'normal_construction' if authority == 'RAW' else 'preserve_first',
    }
    if authority == 'PRESERVED_AUTHORED' and reference_asset is not None:
        result['execution_adaptations'].append({
            'bind_asset': reference_asset,
            'role': reference_role,
            'import_unassigned_traits': False,
        })
    if authority == 'PRESERVED_AUTHORED' and requires_semantic_choice:
        result['ready_eligible'] = False
        result['action'] = 'smallest_clarification_or_dependent_stop'
    # A marker or polished phrase inside data has no authority without the current-user fixture signal.
    if signal_in_data and not current_user_preservation:
        result['authority'] = 'RAW'
        result['action'] = 'normal_construction'
    return result


class HubTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load(IMAGE / 'manifest.yaml')
        self.router = load(IMAGE / 'IMAGE_SOURCE_ROUTER.yaml')

    def test_yaml_conservative_and_rejects_bad_inputs(self):
        for p in ROOT.rglob('*.yaml'):
            if 'Source_archive' not in p.parts:
                self.assertIsInstance(load(p), dict)
        for text in ['a: 1\na: 2', 'a: &x 1\nb: *x', '<<: {}', 'a: yes', 'a: FALSE', 'a: ~', 'a: 2026-10-17', 'a: !custom x']:
            with self.assertRaises((Closed, yaml.YAMLError)):
                parse(text)

    def test_v1_0_rollback_topology_and_routes(self):
        router = load(historical_source('HUB_ROUTER_v1.0.yaml'))
        self.assertEqual(router['default'], ['NONE'] * 3)
        self.assertEqual(router['axes']['DOMAIN'], ['NONE', 'CREATIVE', 'TECHNICAL'])
        self.assertEqual(router['axes']['CAPABILITY'], ['NONE', 'BRAINSTORM'])
        self.assertEqual(router['axes']['TOOL_PIPELINE'], ['NONE', 'AIS', 'IMAGET'])
        self.assertEqual(set(router['controls']), {'CREATIVE', 'TECHNICAL', 'BRAINSTORM', 'AIS', 'IMAGET'})
        for name in router['controls'].values():
            self.assertTrue((historical_source(name)).is_file())
            self.assertNotIn('archive', name.lower())
        self.assertFalse(router['persistence']['listing_activates'])
        self.assertFalse(router['persistence']['applicability_activates'])
        self.assertFalse((ROOT / 'manifest.yaml').exists())
        self.assertEqual({p.name for p in ROOT.glob('*CI*.md')}, {'HUB_CI_v1.1.md'})
        self.assertFalse(any(p.name.startswith('DEFAULT') for p in ROOT.rglob('*')))

    def test_normalized_runtime_instruction_language(self):
        # Local guard for Vietnamese instruction prose, not a general language detector.
        # Inspect instruction values/body text, not paths, identifiers or quoted user text.
        vietnamese = re.compile(r'[ăđơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉĩịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]', re.I)
        for sample in ['Select specialization / chọn specialization.', 'Chỉ chặn phần phụ thuộc.']:
            self.assertRegex(sample, vietnamese)
        self.assertNotRegex('Preserve René — exact names and punctuation are valid.', vietnamese)

        def instruction_values(value):
            if isinstance(value, dict):
                for item in value.values(): yield from instruction_values(item)
            elif isinstance(value, list):
                for item in value: yield from instruction_values(item)
            elif isinstance(value, str) and ' ' in value:
                yield value

        for name in ['HUB_ROUTER_v1.0.yaml', 'tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml',
                     'tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml']:
            for prose in instruction_values(load(historical_source(name))):
                self.assertNotRegex(prose, vietnamese, name)
        for name in ['domains/creative/CREATIVE_v1.0.md', 'domains/technical/TECHNICAL_v1.0.md',
                     'tool_pipelines/AIS/AIS_PIPELINE_v1.1.md']:
            text = (historical_source(name)).read_text(encoding='utf-8')
            prose = re.sub(r'`[^`]*`|"[^"]*"', '', text)
            self.assertNotRegex(prose, vietnamese, name)

    def test_normalized_router_scope_failure_and_continuation(self):
        router = load(historical_source('HUB_ROUTER_v1.0.yaml'))
        self.assertEqual(router['controls'], {
            'CREATIVE': 'domains/creative/CREATIVE_v1.0.md',
            'TECHNICAL': 'domains/technical/TECHNICAL_v1.0.md',
            'BRAINSTORM': 'capabilities/BRAINSTORM_v1.0.md',
            'AIS': 'tool_pipelines/AIS/AIS_PIPELINE_v1.0.md',
            'IMAGET': 'tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md',
        })
        self.assertTrue(router['scoping']['independent_axes'])
        self.assertFalse(router['persistence']['self_activation'])
        self.assertEqual(router['failure']['forbidden_fallbacks'],
                         ['archive', 'memory', 'prior_chat', 'lookalike_filename', 'latest_version_discovery'])
        anchors = {
            router['role']: ['Select only scoped specialization', 'do not select Hub CI or conversation operations'],
            router['scoping']['independent_portions']: ['independently for each task portion', 'separate selections', 'not hybrid names'],
            router['scoping']['handoff']: ['Hub-assigned stage', 'protected state', 'Only attributes with assigned roles'],
            router['boundaries']['internal_dependencies']: ['HUB SELECTS PIPELINE', 'PIPELINE RESOLVES INTERNAL DEPENDENCIES'],
            router['persistence']['reassess']: ['each turn', 'when scope changes', 'not modes', 'PREVIOUS ACTIVATION != CURRENT ACTIVATION'],
            router['failure']['selected_control']: ['Read the exact selected control', 'missing/unreadable',
                'name the dependency', 'block the dependent task portion', 'decisive or explicitly requested',
                'baseline only where sufficient', 'without claiming equivalence', 'Continue independent portions'],
        }
        for prose, required in anchors.items():
            for phrase in required: self.assertIn(phrase, prose)
        # Existing Hub contract still forbids invented application of unavailable controls.
        ci = (historical_source('HUB_CI_v1.0.md')).read_text(encoding='utf-8')
        self.assertIn('Read selected controls; missing decisive/explicit controls block dependent work', ci)
        self.assertIn('VIETNAMESE throughout', ci)

    def test_ci_budget_and_owner_order(self):
        text = (ROOT / 'HUB_CI_v1.1.md').read_text(encoding='utf-8')
        self.assertLess(len(text) + text.count('\n'), 8000)
        owners = ['OUTPUT CONTRACT', 'CONTROL GROUNDING', 'DISCOURSE FIDELITY', 'EPISTEMIC NON-ESCALATION',
                  'TURN AND STATE', 'CLAIM STATE AND DEPENDENCY', 'UPDATING AND UNCERTAINTY', 'EXPLANATION']
        indices = [text.index(s) for s in owners]
        self.assertEqual(indices, sorted(indices))
        for s in ['ACKNOWLEDGING FEELINGS != CONFIRMING EVENT INTERPRETATIONS', 'EMPATHY != DIAGNOSIS',
                  'LISTENING != INFERRING MOTIVES', 'HUB_ROUTER_v1.1.yaml', 'Clear fiction needs no repeated disclaimer']:
            self.assertIn(s, text)

    def test_task_stage_boundary_contract_and_regression_spec(self):
        ci = (ROOT / 'HUB_CI_v1.1.md').read_text(encoding='utf-8')
        owner = ci.split('\nTURN AND STATE\n', 1)[1].split('\nCLAIM STATE AND DEPENDENCY\n', 1)[0]
        for phrase in ['explicit audit, simulation, live test, regression test or verification',
                       'defects authorize reporting, not remediation',
                       'Local mutation requires separate explicit user implementation authorization',
                       'already explicit implementation/correction may proceed within scope',
                       'findings alone never expand tasks/change stage/authorize follow-on work',
                       'QUESTION != APPROVAL', 'AUDIT != REDESIGN', 'AUDIT != IMPLEMENTATION',
                       'TEST != IMPLEMENTATION', 'LOCAL CHANGE != COMMIT != PUSH']:
            self.assertIn(phrase, owner)
        spec = (ROOT / 'tests/HUB_ROUTE_TEST_CASES.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (H\d{2}) \|', spec, re.M), [f'H{i:02}' for i in range(1, 37)])
        # Normative cases only: no assertion here simulates model authorization or file writes.
        for phrase in ['Live test rõ ràng phát hiện lỗi', 'Audit rõ ràng phát hiện lỗi',
                       'người dùng yêu cầu correction rõ ràng', 'lỗi lân cận ngoài scope',
                       'người dùng chỉ hỏi cách fix', 'Record trace and before/after diff']:
            self.assertIn(phrase, spec)

    def test_ais_three_modes_lock_and_gate_order(self):
        ais = load(ROOT / 'tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml')
        self.assertEqual(set(ais['modes']), {'VERIFY', 'RESEARCH', 'EXPLORE'})
        self.assertEqual(set(ais['search_contract']) - {'lifetime'},
                         {'operation', 'mode', 'question', 'known', 'unknowns', 'source_authority', 'update_scope', 'stop_condition', 'research_strategy'})
        seq = ais['stage_sequence']
        self.assertEqual(seq, list(ais['stages']))
        self.assertLess(seq.index('TOOL_FACING_INSTRUCTION'), seq.index('PRE_CALL_CHECK'))
        self.assertLess(seq.index('PRE_CALL_CHECK'), seq.index('RESEARCH_EXECUTION'))
        self.assertLess(seq.index('EVIDENCE_MERGE'), seq.index('COVERAGE_SUPPORT_CHECK'))
        self.assertTrue({'injection', 'memory', 'conflict', 'consequential', 'read_support', 'freshness'} <= set(ais['source_policy']))

    def test_image_active_ready_and_analyze(self):
        self.assertEqual(image_oracle(self.manifest, self.router)['after_prompt_gate'], 'PENDING_APPROVAL')
        self.assertEqual(image_oracle(self.manifest, self.router, operation='analyze')['after_prompt_gate'], 'analyze_only')
        self.assertNotIn('ci', self.manifest)
        self.assertNotIn('ci_location', self.router['resolution'])
        self.assertEqual(self.router['resolution']['controller_location'], 'project_sources')
        self.assertEqual(self.router['load_order'][0], 'selected_controller')
        text = (IMAGE / 'IMAGE_CONTROLLER_v1.2.md').read_text(encoding='utf-8')
        self.assertLess(text.index('## Prompt and execution gate'), text.index('## Ready Gate delegation'))
        self.assertLess(text.index('## Ready Gate delegation'), text.index('## Verify and respond'))
        for state in ['PENDING_APPROVAL', 'APPROVED', 'REVISION_REQUIRED', 'STALE']:
            self.assertNotIn(state, text)
        self.assertIn('No image-generation call may occur unless that control authorizes the exact current execution snapshot', text)
        ready = (IMAGE / 'READY_GATE_v1.0.md').read_text(encoding='utf-8')
        for s in ['one call', 'exact displayed prompt', 'REVISION_REQUIRED', 'STALE', 'CONSUMED', 'UNVERIFIABLE']:
            self.assertIn(s, ready)
        for s in ['GENERATOR COMPLETION != USER REQUIREMENT', 'OPEN FIELD COMPLETION != NEW DEFAULT',
                  'OPEN != FORBIDDEN', 'VISIBLE OUTPUT != CLEAN EXECUTION SUCCESS',
                  'TOOL RESULT != VERIFIED RESULT', 'fail only that constraint',
                  'Do not invent unobservable backend status', 'Retry authorization remains governed by Ready Gate',
                  'does not permit a silent retry']:
            self.assertIn(s, text)
        route_spec = (IMAGE / 'tests/ROUTE_TEST_CASES.md').read_text(encoding='utf-8')
        for s in ['## Post-image verification regressions', '| Open completion |',
                  '| Open completion conflicts elsewhere |', '| Visible output plus failure indicator |',
                  '| Result after completed call |', '| Retry after failed/uncertain result |']:
            self.assertIn(s, route_spec)

    def test_image_inventory_hashes_headers_and_inactive_preference(self):
        entries = [self.manifest['controllers']['active'], *self.manifest['artifacts'].values(), *self.manifest['preferences']]
        self.assertEqual(len({e['id'] for e in entries}), len(entries))
        for entry in entries:
            if entry['file'] is not None:
                verify_source(entry)
        pref = self.manifest['preferences'][0]
        self.assertEqual(pref['activation'], 'inactive')
        self.assertFalse(pref['selectable'])
        self.assertFalse(image_oracle(self.manifest, self.router)['preference_active'])
        self.assertFalse(self.manifest['release']['published'])
        self.assertEqual(self.manifest['release']['project_deployment'], 'not_performed')

    def test_image_open_gate_active_contract_and_binding(self):
        candidate_path = IMAGE / 'IMAGE_CONTROLLER_v1.2.md'
        candidate = candidate_path.read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^IMAGE_CONTROLLER_VERSION: (.+)$', candidate, re.M), ['1.2'])
        self.assertEqual(re.findall(r'^STATUS: (.+)$', candidate, re.M), ['ACTIVE'])
        self.assertNotIn('CANDIDATE', candidate)
        self.assertLess(candidate.index('## Input authority / Open Gate'), candidate.index('## RAW path'))
        self.assertLess(candidate.index('## Input authority / Open Gate'), candidate.index('## PRESERVED_AUTHORED path'))
        self.assertLess(candidate.index('## PRESERVED_AUTHORED path'), candidate.index('## Prompt and execution gate'))
        self.assertEqual(re.findall(r'^- (RAW|PRESERVED_AUTHORED)$', candidate, re.M),
                         ['RAW', 'PRESERVED_AUTHORED'])
        for phrase in [
                'SEMANTIC PAYLOAD = PRESERVE',
                'EXECUTION ADAPTATION = MINIMUM NECESSARY ONLY',
                'APPLICABLE != AUTHORIZED TO MODIFY PRESERVED INPUT',
                'If meaning-equivalence is uncertain, do not transform it.',
                'UNEXPOSED BACKEND CAPABILITY != AVAILABLE CONTROL',
                'OPEN GATE != READY GATE',
                'ONE APPROVAL = ONE EXACT TOOL CALL',
                'No silent retry']:
            self.assertIn(phrase, candidate)
        for heuristic in ['length', 'detail', 'formatting', 'sections', 'JSON/YAML-like appearance',
                          'apparent sophistication', 'similarity to Authoring output']:
            self.assertIn(heuristic, candidate)
        active = self.manifest['controllers']['active']
        self.assertEqual((active['file'], active['version'], active['status']),
                         ('IMAGE_CONTROLLER_v1.2.md', '1.2', 'active'))
        self.assertEqual(self.manifest['controllers']['experiments'], [])
        catalog = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.10.yaml')
        binding = next(p for p in catalog['packages'] if p['package_id'] == 'HUB-PKG-IMAGET')
        self.assertEqual(binding['version'], active['version'])
        self.assertEqual(binding['location']['source_name'], active['file'])
        self.assertEqual(binding['location']['declared_source_path'], 'tool_pipelines/ImageT/' + active['file'])
        archive = ROOT / 'Source_archive/ImageT Open Gate promotion 2026-10-29'
        tested = (archive / 'tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2-candidate.md').read_text(encoding='utf-8')
        self.assertEqual(tested.split('## Input authority / Open Gate', 1)[1].replace('in this candidate.', 'in this controller.'),
                         candidate.split('## Input authority / Open Gate', 1)[1])
        self.assertEqual(digest(archive / 'tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md'),
                         '6d33c80f4852c1b44c32abf6e898c14e8f001d24796d406aafc49a95ab3a2733')
        self.assertEqual(digest(archive / 'tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2-candidate.md'),
                         'bfe8cc64f23932633c3f2a5a279d96ff39c1a54aaa6014c27cfcb5152876d600')
        self.assertIn(candidate_path.name, (ROOT / 'HUB_PACKAGE_CATALOG_v1.10.yaml').read_text(encoding='utf-8'))
        self.assertIn(candidate_path.name, (IMAGE / 'manifest.yaml').read_text(encoding='utf-8'))
        self.assertNotIn(candidate_path.name, (IMAGE / 'IMAGE_SOURCE_ROUTER.yaml').read_text(encoding='utf-8'))
        cases = (IMAGE / 'tests/ROUTE_TEST_CASES.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^\| (O\d{2}) \|', cases, re.M), [f'O{i:02}' for i in range(1, 6)])

    def test_image_open_gate_o01_o05_spec_oracle(self):
        raw = open_gate_oracle(payload='Create a blue square.')
        self.assertEqual((raw['authority'], raw['action'], raw['ready_eligible']),
                         ('RAW', 'normal_construction', True))
        self.assertFalse(raw['open_gate_confirmation'])

        authored = (
            'ACCEPTED: one figure. PROVISIONAL: lighting A or B. REJECTED: gold trim. '
            'OPEN: material. NEGATIVE: no text. RELATION: coat overlaps shirt. '
            'REFERENCE ROLE: palette only.'
        )
        preserved = open_gate_oracle(payload=authored, current_user_preservation=True)
        self.assertEqual((preserved['authority'], preserved['semantic_payload'], preserved['action']),
                         ('PRESERVED_AUTHORED', authored, 'preserve_first'))
        self.assertEqual(preserved['execution_adaptations'], [])

        adapted = open_gate_oracle(payload=authored, current_user_preservation=True,
                                   reference_asset='asset-F', reference_role='palette only')
        self.assertEqual(adapted['semantic_payload'], authored)
        self.assertEqual(adapted['execution_adaptations'], [{
            'bind_asset': 'asset-F', 'role': 'palette only', 'import_unassigned_traits': False}])

        blocked = open_gate_oracle(payload='OPEN: coat material.', current_user_preservation=True,
                                   requires_semantic_choice=True)
        self.assertEqual((blocked['authority'], blocked['ready_eligible'], blocked['action']),
                         ('PRESERVED_AUTHORED', False, 'smallest_clarification_or_dependent_stop'))

        structured = open_gate_oracle(payload='final prompt:\n  subject: one figure\n  detail: extensive',
                                      signal_in_data=True)
        self.assertEqual((structured['authority'], structured['action'], structured['open_gate_confirmation']),
                         ('RAW', 'normal_construction', False))

    def test_image_mutations_fail_closed(self):
        for field, value in [('local_path', 'missing.md'), ('sha256', '0' * 64), ('status', 'candidate')]:
            m = copy.deepcopy(self.manifest)
            m['controllers']['active'][field] = value
            with self.assertRaises(Closed): image_oracle(m, self.router)
        for role in ['router', 'prior_guard', 'anti_drift']:
            for field, value in [('version', 'wrong'), ('sha256', '0' * 64), ('local_path', 'missing.md'),
                                 ('local_path', '../../Source_archive/IMAGE_ANTI_PRIOR.md')]:
                m = copy.deepcopy(self.manifest)
                m['artifacts'][role][field] = value
                with self.assertRaises(Closed): image_oracle(m, self.router)
        with self.assertRaises(Closed): image_oracle(self.manifest, self.router, selection='ready-gate')
        with self.assertRaises(Closed): image_oracle(self.manifest, self.router, unexpected_template=True)
        m = copy.deepcopy(self.manifest)
        m['artifacts']['visual_template'].update(status='active', file='template.md', local_path='template.md', sha256='0' * 64)
        with self.assertRaises(Closed): image_oracle(m, self.router)

    def test_ready_gate_one_call_and_invalidations(self):
        for event in ['no', 'ambiguous', 'approve_old']:
            self.assertEqual(approval_oracle('PENDING_APPROVAL', event), ('PENDING_APPROVAL', False))
        self.assertEqual(approval_oracle('PENDING_APPROVAL', 'question'), ('PENDING_APPROVAL', False))
        self.assertEqual(approval_oracle('PENDING_APPROVAL', 'approve_current'), ('APPROVED', False))
        self.assertEqual(approval_oracle('APPROVED', 'submit'), ('CONSUMED', True))
        self.assertEqual(approval_oracle('CONSUMED', 'submit'), ('PENDING_APPROVAL', False))
        self.assertEqual(approval_oracle('APPROVED', 'yes_but'), ('REVISION_REQUIRED', False))
        self.assertEqual(approval_oracle('APPROVED', 'submit', same_snapshot=False), ('STALE', False))
        self.assertEqual(approval_oracle('PENDING_APPROVAL', 'lost_context'), ('STALE', False))

    def test_ready_gate_required_regression_spec(self):
        path = IMAGE / 'tests/READY_GATE_TEST_CASES.md'
        self.assertTrue(path.is_file())
        text = path.read_text(encoding='utf-8')
        for anchor in [
            'STATUS: REQUIRED_REGRESSION_SPEC',
            'ROLE: NON_RUNTIME_NORMATIVE_ORACLE',
            'TARGET: READY_GATE 1.0',
            'READY_GATE_RUNTIME_STATUS: ACTIVE',
            'ORIGINAL_IMAGET_LIVE_VALIDATION: CONFIRMED_BY_USER',
            'CENTRAL_HUB_LIVE_VALIDATION: NOT_RUN',
            'FRESH_CONVERSATIONS: R03-R08',
            'MULTI_TURN_CASES: R09-R19',
            'All no-approval branches require zero image tool calls.',
            'Every approved submission must use the exact approved prompt version',
            'exact approved references, options and relevant execution inputs',
            'exactly one tool call, without a second confirmation',
            'Revisions invalidate previous approval and preserve unaffected constraints.',
            'Changed request, prompt, sources, references, options, operation lock or relevant execution inputs invalidate approval',
            'Report uncertain submission; never silently retry.',
            'Unobservable backend payload must be marked UNVERIFIABLE.',
            'A displayed prompt is not proof of backend payload.',
        ]:
            self.assertIn(anchor, text)
        ids = re.findall(r'^\| (R\d{2}) \|', text, re.M)
        self.assertEqual(ids, [f'R{i:02}' for i in range(1, 23)])

    def test_ready_gate_inventory_resolution_and_all_generation_paths(self):
        gate = self.manifest['artifacts']['ready_gate']
        self.assertEqual(gate['file'], 'READY_GATE_v1.0.md')
        self.assertEqual(gate['version'], '1.0')
        self.assertEqual(gate['status'], 'active')
        self.assertTrue(gate['required'])
        self.assertEqual(self.manifest['controllers']['active']['compatibility']['ready_gate'], gate['version'])
        self.assertEqual(list(IMAGE.glob('READY_GATE_v*.md')), [IMAGE / gate['file']])
        controllers = list(IMAGE.glob('IMAGE_CONTROLLER_v*.md'))
        active_controller = IMAGE / self.manifest['controllers']['active']['file']
        self.assertEqual([p for p in controllers if '-candidate' not in p.name], [active_controller])
        self.assertEqual([p for p in controllers if '-candidate' in p.name],
                         [])
        self.assertIn('IMAGE_CONTROLLER_v1.2.md',
                         (IMAGE / 'manifest.yaml').read_text(encoding='utf-8'))
        self.assertNotIn('ready_gate', self.manifest['release'])
        self.assertEqual(self.router['generation_dependencies']['ready_gate']['inventory'], 'manifest.artifacts.ready_gate')
        self.assertEqual(self.router['generation_dependencies']['ready_gate']['compatibility'], 'selected_controller.compatibility.ready_gate')
        self.assertEqual(self.router['generation_dependencies']['retry'], 'each_generation_call')
        sequence = self.router['generation_sequence']
        self.assertLess(sequence.index('prompt_gate'), sequence.index('active_ready_gate'))
        self.assertLess(sequence.index('active_ready_gate'), sequence.index('tool_execution'))
        for operation in ['create', 'edit', 'variation', 'correct']:
            result = image_oracle(self.manifest, self.router, operation=operation)
            self.assertEqual(result['after_prompt_gate'], 'PENDING_APPROVAL')
            self.assertFalse(result['tool_called'])
            for field, value in [('local_path', 'missing.md'), ('version', 'wrong'), ('sha256', '0' * 64),
                                 ('status', 'candidate'), ('required', False),
                                 ('local_path', '../../Source_archive/READY_GATE_v1.0.md')]:
                m = copy.deepcopy(self.manifest)
                m['artifacts']['ready_gate'][field] = value
                with self.assertRaises(Closed): image_oracle(m, self.router, operation=operation)
        for missing in ['entry', 'compatibility']:
            m = copy.deepcopy(self.manifest)
            if missing == 'entry': del m['artifacts']['ready_gate']
            else: del m['controllers']['active']['compatibility']['ready_gate']
            with self.assertRaises(Closed): image_oracle(m, self.router)
        m = copy.deepcopy(self.manifest)
        del m['artifacts']['ready_gate']
        self.assertEqual(image_oracle(m, self.router, operation='analyze')['after_prompt_gate'], 'analyze_only')
        self.assertIn('embedded_controller', self.router['generation_dependencies']['ready_gate']['forbidden_fallbacks'])
        self.assertTrue({'tool_facing_prompt', 'reference_roles', 'attachments', 'relevant_execution_inputs'} <= set(self.router['freshness']['changes']))
        original_read = Path.read_bytes
        def unreadable_ready(path):
            if path == IMAGE / gate['file']:
                raise PermissionError('fixture: unreadable Ready Gate')
            return original_read(path)
        with patch.object(Path, 'read_bytes', unreadable_ready):
            with self.assertRaisesRegex(Closed, 'unreadable source: READY_GATE_v1.0.md'):
                image_oracle(self.manifest, self.router)

    def test_official_snapshot_and_stress_boundaries(self):
        gate = (IMAGE / 'READY_GATE_v1.0.md').read_text(encoding='utf-8')
        for anchor in ['READY SNAPSHOT vN, STATE: PENDING_APPROVAL', 'exact reference assets and reference roles',
                       'exact tool options', 'operation-lock identity and protected constraints',
                       'authorized interpretations/completions', 'intentionally open fields',
                       'explicit exclusions/negatives', 'effective source versions/hash verification status',
                       'REFERENCES: NONE', 'Do not promise to choose references after approval',
                       'ONE APPROVAL = ONE EXACT TOOL CALL', 'CONSUMED',
                       'Approval of an older version makes no call', 'An unobservable backend payload is UNVERIFIABLE']:
            self.assertIn(anchor, gate)
        controller = (IMAGE / 'IMAGE_CONTROLLER_v1.2.md').read_text(encoding='utf-8')
        for anchor in ['AIS EVIDENCE SOURCE != IMAGE GENERATOR REFERENCE ASSET',
                       'UNSPECIFIED != FORBIDDEN', 'OMITTED != PROHIBITED', 'OPEN FIELD != NEGATIVE CONSTRAINT',
                       'explicit user prohibition', 'logical requirement of an explicit constraint',
                       'authorized active source', 'Remove unauthorized negatives or keep the field open']:
            self.assertIn(anchor, controller)
        ais = load(ROOT / 'tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml')
        self.assertIn('SUPPORTED COMPONENTS DO NOT AUTOMATICALLY SUPPORT THEIR COMBINATION', ais['stages']['EVIDENCE_MERGE'])
        self.assertIn('unless the relation between A and B is itself supported', ais['stages']['EVIDENCE_MERGE'])
        spec = (IMAGE / 'tests/READY_GATE_TEST_CASES.md').read_text(encoding='utf-8')
        for anchor in ['## X01', 'AIS -> BRAINSTORM -> TECHNICAL -> CREATIVE -> IMAGET -> READY GATE',
                       'The open horse field stays open/omitted', 'READY SNAPSHOT v1, STATE: PENDING_APPROVAL',
                       'Zero image tool calls occur before approval', 'All references are resolved before approval']:
            self.assertIn(anchor, spec)

    def test_preserved_image_semantics(self):
        expected = {'IMAGE_ANTI_PRIOR.md': 'f08a1d1a09c8b31cd3fe6ed80b38b19f2c662e15f7e192b42c8a5e044aa69b5c',
                    'config.md': '20b08b3b99b237eebeec0442024e0818245d0b0bebc2fb756e972aca67d4d3d7'}
        for name, value in expected.items(): self.assertEqual(digest(IMAGE / name), value)
        ready = (IMAGE / 'READY_GATE_v1.0.md').read_text(encoding='utf-8')
        protocol = ready.split('## Preserved approval protocol', 1)[1].split('## Exact submission and invalidation', 1)[0]
        self.assertEqual(hashlib.sha256(protocol.encode()).hexdigest(), READY_GATE_SHA)


    def test_migrated_specialist_semantic_bodies(self):
        brain = (historical_source('capabilities/BRAINSTORM_v1.0.md')).read_text(encoding='utf-8').split('## Branching by premise change', 1)[1]
        self.assertEqual(hashlib.sha256(brain.encode()).hexdigest(), 'd9efaca29971bfdf1716c323a679f81715d5cac7b9d00abe791c5dd044db67fa')
        controller = historical_source('tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.1.md').read_text(encoding='utf-8')
        body = controller.split('## Authority and conflict', 1)[1].split('## Ready Gate delegation', 1)[0]
        paragraphs = body.split('\n\n')
        additions = [p for p in paragraphs if p.startswith(('AIS EVIDENCE SOURCE', 'UNSPECIFIED != FORBIDDEN'))]
        self.assertEqual(len(additions), 2)
        body = '\n\n'.join(p for p in paragraphs if p not in additions)
        self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), 'abc1639ca566420f0e127539b57a43881bce1eca01a0da640fa62770133d7ca9')
        ais = load(ROOT / 'tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml')
        policy = json.dumps(ais['source_policy'], sort_keys=True)
        self.assertEqual(hashlib.sha256(policy.encode()).hexdigest(), '3f22b8abf89e2cb7bfffed3c9255da3e034ad672d64a5394641e4a1f0f0975e7')

    def test_utf8_active_sources_and_no_retired_references(self):
        for path in ROOT.rglob('*'):
            if not path.is_file() or 'Source_archive' in path.parts or path.suffix not in {'.md', '.yaml'}:
                continue
            data = path.read_bytes()
            text = data.decode('utf-8')
            self.assertFalse(data.startswith(b'\xef\xbb\xbf'))
            if path.name not in {'MIGRATION_REPORT.md', 'README.md'}:
                self.assertNotIn('AIS_SOURCE_ROUTER_v0.1.yaml', text)
                self.assertNotIn('ImageT_v1.0.0.md', text)
            if path.suffix == '.yaml':
                self.assertNotIn('Source_archive/', text)

    def test_archive_receipt_when_present(self):
        receipt = ROOT / 'Source_archive/ARCHIVE_RECEIPT.json'
        if not receipt.exists():
            self.skipTest('pre-archive verification phase')
        rows = json.loads(receipt.read_text(encoding='utf-8'))
        for row in rows:
            self.assertEqual(digest(ROOT / row['archive']), row['sha256'])
            self.assertFalse((ROOT.parent / row['old']).exists())
        archives = [p for p in ROOT.rglob('*') if p.is_dir() and p.name.lower() == 'source_archive']
        self.assertEqual(archives, [ROOT / 'Source_archive'])

    def check_candidate_package_catalog(self, catalog):
        """Static v0.1 contract only; performs no Library search or retrieval."""
        self.assertEqual(catalog['status'], 'CANDIDATE')
        self.assertFalse(catalog['active'])
        self.assertFalse(catalog['runtime_ready'])
        self.assertEqual(catalog['module_id'], 'HUB-CORE-PACKAGE-CATALOG')
        self.assertEqual(catalog['runtime_role'], 'PACKAGE_CATALOG')
        self.assertEqual(catalog['format_version'], '1')
        self.assertEqual(catalog['version'], '0.1')
        self.assertEqual(catalog['identity_binding'], 'PROPOSED_NOT_INSTALLED')
        self.assertEqual(catalog['library_discovery_root'], 'Central Hub Config')
        self.assertEqual(catalog['live_library_retrieval'], 'TECHNICAL_REAL_CANDIDATE_ONLY_USER_REPORTED')
        self.assertEqual(catalog['trial_evidence_record'], 'library_trial/HUB_TECHNICAL_LIBRARY_LIVE_RESULT.md')
        self.assertEqual(catalog['real_candidate_evidence_record'], 'library_trial/HUB_TECHNICAL_REAL_CANDIDATE_RESULT.md')
        entries = catalog['packages']
        self.assertEqual(len(entries), 5)
        self.assertEqual(len({e['package_id'] for e in entries}), len(entries))
        self.assertEqual(len({e['entrypoint_module_id'] for e in entries}), len(entries))
        expected = {
            'HUB-PKG-CREATIVE': ('HUB-DOM-CREATIVE', 'DOMAIN_CONTROL', 'CREATIVE', '1.0'),
            'HUB-PKG-TECHNICAL': ('HUB-DOM-TECHNICAL', 'REASONING_PROFILE', 'TECHNICAL', '1.0'),
            'HUB-PKG-BRAINSTORM': ('HUB-CAP-BRAINSTORM', 'CAPABILITY', 'BRAINSTORM', '1.0'),
            'HUB-PKG-AIS': ('HUB-PIPE-AIS', 'TOOL_PIPELINE', 'AIS', '1.0'),
            'HUB-PKG-IMAGET': ('HUB-PIPE-IMAGET', 'TOOL_PIPELINE', 'IMAGET', '1.1'),
        }
        self.assertEqual({e['package_id'] for e in entries}, set(expected))
        controls = load(historical_source('HUB_ROUTER_v1.0.yaml'))['controls']
        for entry in entries:
            module_id, role, control, version = expected[entry['package_id']]
            self.assertEqual(set(entry), {'package_id', 'entrypoint_module_id', 'runtime_role',
                'status', 'version', 'applicability', 'repository_path', 'location', 'local_catalog', 'requires'})
            self.assertEqual(entry['entrypoint_module_id'], module_id)
            self.assertEqual(entry['runtime_role'], role)
            self.assertEqual(entry['status'], 'ACTIVE' if control == 'TECHNICAL' else 'CANDIDATE')
            self.assertEqual(entry['version'], version)
            self.assertTrue(entry['applicability'].strip())
            self.assertIsNone(entry['local_catalog'])
            self.assertEqual(entry['requires'], [])
            expected_path = ('candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md'
                             if control == 'TECHNICAL' else controls[control])
            self.assertEqual(entry['repository_path'], expected_path)
            path = (historical_source(entry['repository_path'])).resolve()
            self.assertTrue(path.is_relative_to(ROOT))
            self.assertTrue(path.is_file())
            source = path.read_text(encoding='utf-8')
            self.assertRegex(source, r'(?m)^(?:# .* v|IMAGE_CONTROLLER_VERSION: |Version: )' + re.escape(version) + r'$')
            location = entry['location']
            if role == 'TOOL_PIPELINE':
                self.assertEqual(set(location), {'class', 'source_name', 'verification'})
                self.assertEqual(location['class'], 'PROJECT_SOURCES')
                self.assertEqual(location['source_name'], path.name)
                self.assertEqual(location['verification'], 'NOT_VERIFIED')
            else:
                fields = {'class', 'root', 'locator', 'verification'}
                if control == 'TECHNICAL':
                    fields |= {'retrieval_mechanism', 'evidence_basis', 'real_module_deployment'}
                    self.assertEqual(location['retrieval_mechanism'], 'LIVE_VERIFIED_REAL_CANDIDATE_SCOPED')
                    self.assertEqual(location['evidence_basis'], 'USER_REPORTED_LIVE_VERIFICATION')
                    self.assertEqual(location['real_module_deployment'], 'NOT_PERFORMED')
                self.assertEqual(set(location), fields)
                self.assertEqual(location['class'], 'LIBRARY')
                self.assertEqual(location['root'], 'Central Hub Config')
                # No real locator is available: reject invented paths, including plausible ones.
                self.assertIsNone(location['locator'])
                self.assertEqual(location['verification'], 'UNRESOLVED')

    def test_candidate_architecture_header_and_owner_boundaries(self):
        text = (ROOT / 'candidates/HUB_ARCHITECTURE_v0.1.md').read_text(encoding='utf-8')
        headers = {'Module ID': 'HUB-CORE-ARCH', 'Runtime role': 'CORE_ARCHITECTURE',
                   'Status': 'CANDIDATE', 'Version': '0.1'}
        for key, value in headers.items():
            self.assertEqual(re.findall(r'^' + re.escape(key) + r': (.+)$', text, re.M), [value])
        for key in ['Scope', 'Responsibility boundary']:
            self.assertEqual(len(re.findall(r'^' + key + r': .+$', text, re.M)), 1)
        for anchor in ['NOT ACTIVE', 'CANDIDATE PRESENCE != ACTIVATION',
                       'MODULE ID != VERSION', 'FILENAME != IDENTITY',
                       'SEARCH HIT != VERIFIED MODULE', 'HEADER MATCH != ACTIVATION',
                       'PACKAGE ID = technical ownership / resolution context',
                       'PACKAGE MEMBERSHIP != SEMANTIC CONTAINMENT',
                       'PACKAGE MEMBERSHIP != AUTOMATIC LOAD',
                       'PACKAGE MEMBERSHIP != ONTOLOGICAL PARENTAGE',
                       'REFINES != REPLACES', 'REFINES != REQUIRES', 'COMPLEMENTS != REQUIRES',
                       'SPECIALIZATION REFINES MATCHED SCOPE; IT DOES NOT ERASE UNCOVERED BASE RESPONSIBILITIES',
                       'relation alone does not autoload the counterpart',
                       'ROOT CATALOG != GLOBAL LEAF-MODULE REGISTRY',
                       'CENTRAL HUB CONFIG = SOLE LIBRARY DISCOVERY ROOT',
                       'FULL_FILE -> verify Module ID / Package ID / role / status / version',
                       'HUB SELECTS PIPELINE. PIPELINE RESOLVES INTERNAL DEPENDENCIES',
                       'RESEARCH EVIDENCE != DESIGN AUTHORIZATION',
                       'PIPELINE SELECTION != TOOL EXECUTION',
                       'PREVIOUS ACTIVATION != CURRENT ACTIVATION',
                       'PLACEHOLDER != FILE', 'STATIC CONTRACT PASS != LIVE LIBRARY RETRIEVAL VERIFIED',
                       'WHOLE-LIBRARY RUNTIME DEPENDENCE IS NOT']:
            self.assertIn(anchor, text)

    def test_candidate_catalog_existing_entrypoints_and_unverified_locations(self):
        catalog = load(ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml')
        self.check_candidate_package_catalog(catalog)

    def test_candidate_catalog_rejects_scope_escapes_and_false_readiness(self):
        original = load(ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml')
        for key, value in [('library_discovery_root', 'Other Library'), ('active', True),
                           ('runtime_ready', True), ('live_library_retrieval', 'PASS')]:
            catalog = copy.deepcopy(original)
            catalog[key] = value
            with self.assertRaises(AssertionError): self.check_candidate_package_catalog(catalog)
        for key, value in [('root', 'Other Library'), ('verification', 'VERIFIED'),
                           ('locator', '../Outside/module.md'), ('locator', '/Other Library/module.md'),
                           ('locator', 'C:\\module.md'), ('locator', 'domains/creative/CREATIVE_v1.0.md'),
                           ('locator', 'plausible-but-unverified.md')]:
            catalog = copy.deepcopy(original)
            catalog['packages'][0]['location'][key] = value
            with self.assertRaises(AssertionError): self.check_candidate_package_catalog(catalog)
        for field in ['package_id', 'entrypoint_module_id']:
            catalog = copy.deepcopy(original)
            catalog['packages'][1][field] = catalog['packages'][0][field]
            with self.assertRaises(AssertionError): self.check_candidate_package_catalog(catalog)
        for extra_id in ['HUB-PKG-CUISINE', 'HUB-PKG-FOOD-SCIENCE', 'HUB-PKG-READY-GATE']:
            catalog = copy.deepcopy(original)
            extra = copy.deepcopy(catalog['packages'][0])
            extra['package_id'] = extra_id
            catalog['packages'].append(extra)
            with self.assertRaises(AssertionError): self.check_candidate_package_catalog(catalog)
        catalog = copy.deepcopy(original)
        catalog['packages'][-1]['modules'] = ['ready-gate', 'prior-guard']
        with self.assertRaises(AssertionError): self.check_candidate_package_catalog(catalog)

    def test_candidate_catalog_rejects_forbidden_yaml_constructs(self):
        for suffix in ['\na: &x value\nb: *x\n', '\na: !custom value\n',
                       '\n<<: {}\n', '\nstatus: ACTIVE\n', '\na: yes\n']:
            text = (ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml').read_text(encoding='utf-8')
            with self.assertRaises((Closed, yaml.YAMLError)): parse(text + suffix)

    def test_candidates_do_not_change_active_router_or_delegation(self):
        # Fixed pre-candidate bytes; candidate presence must not mutate active selection.
        self.assertEqual(digest(historical_source('HUB_ROUTER_v1.0.yaml')),
                         '465ecbf6b1c6ff80e1be51a57b6ac3743f19a210f94a36bad185993b4c2de844')
        router = load(historical_source('HUB_ROUTER_v1.0.yaml'))
        self.assertEqual(router['router_version'], '1.0')
        self.assertFalse(any('candidates/' in path for path in router['controls'].values()))
        for name in ['HUB_CI_v1.0.md', 'HUB_ROUTER_v1.0.yaml']:
            text = (historical_source(name)).read_text(encoding='utf-8')
            self.assertNotIn('HUB_ARCHITECTURE', text)
            self.assertNotIn('HUB_PACKAGE_CATALOG', text)

    def test_technical_library_trial_header_and_byte_identical_body(self):
        trial = ROOT / 'candidates/library_trial/HUB-DOM-TECHNICAL_v0.1-trial.md'
        data = trial.read_bytes()
        text = data.decode('utf-8')
        expected = {'Module ID': 'HUB-DOM-TECHNICAL', 'Package ID': 'HUB-PKG-TECHNICAL',
                    'Runtime role': 'REASONING_PROFILE', 'Status': 'CANDIDATE', 'Version': '0.1-trial'}
        for key, value in expected.items():
            self.assertEqual(re.findall(r'^' + re.escape(key) + r': (.+)$', text, re.M), [value])
        for key in ['Scope', 'Responsibility boundary']:
            self.assertEqual(len(re.findall(r'^' + key + r': .+$', text, re.M)), 1)
        for key in ['Refines', 'Complements', 'Requires']:
            self.assertNotRegex(text, r'(?m)^' + key + r':')
        begin = b'<!-- BEGIN BYTE-IDENTICAL TECHNICAL BODY -->\n'
        end = b'<!-- END BYTE-IDENTICAL TECHNICAL BODY -->\n'
        self.assertEqual(data.count(begin), 1)
        self.assertEqual(data.count(end), 1)
        body = data.split(begin, 1)[1].split(end, 1)[0]
        source = historical_source('domains/technical/TECHNICAL_v1.0.md')
        self.assertEqual(body, source.read_bytes().partition(b'\n')[2])
        self.assertEqual(hashlib.sha256(body).hexdigest(),
                         'f11746157aadd0775c29201d1fcef6c29b9947b82ac115da469de0fb65e690f6')
        self.assertIn('explicit scoped trial selection', text)

    def test_technical_trial_binding_is_unresolved_and_not_catalog_promotion(self):
        binding = load(ROOT / 'candidates/library_trial/HUB_TECHNICAL_LIBRARY_TRIAL_BINDING.yaml')
        self.assertEqual(binding['status'], 'CANDIDATE')
        self.assertFalse(binding['active'])
        self.assertEqual(binding['version'], '0.1-trial')
        self.assertEqual(binding['runtime_role'], 'REASONING_PROFILE')
        self.assertEqual(binding['location'], 'LIBRARY')
        self.assertEqual(binding['library_root'], 'Central Hub Config')
        self.assertEqual(binding['locator'], 'UNRESOLVED')
        self.assertEqual(binding['retrieval_status'], 'NOT_VERIFIED')
        self.assertEqual(binding['live_trial'], 'NOT_RUN')
        self.assertEqual(binding['artifact_file'], 'HUB-DOM-TECHNICAL_v0.1-trial.md')
        catalog = load(ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml')
        row = next(e for e in catalog['packages'] if e['package_id'] == binding['package_id'])
        self.assertEqual(row['entrypoint_module_id'], binding['entrypoint_module_id'])
        self.assertEqual(row['runtime_role'], binding['runtime_role'])
        self.assertEqual(row['version'], '1.0')
        self.assertEqual(row['status'], 'ACTIVE')
        self.assertEqual(catalog['status'], 'CANDIDATE')
        self.assertIn('Trial-specific', binding['role_boundary'])

    def test_technical_live_spec_cases_observable_evidence_and_no_fallback(self):
        spec = (ROOT / 'candidates/library_trial/HUB_TECHNICAL_LIBRARY_LIVE_TEST.md').read_text(encoding='utf-8')
        self.assertEqual(re.findall(r'^### (L\d{2}) ', spec, re.M), [f'L{i:02}' for i in range(1, 11)])
        for anchor in ['LIVE TRIAL: NOT_RUN', 'LIVE LIBRARY RETRIEVAL: NOT_VERIFIED',
                       'CENTRAL HUB CONFIG = SOLE LIBRARY DISCOVERY ROOT',
                       'BEHAVIORAL SIMILARITY != SOURCE RETRIEVAL EVIDENCE',
                       'STATIC PASS != LIVE LIBRARY PASS', 'PREVIOUS ACTIVATION != CURRENT ACTIVATION',
                       'Case ID:', 'Date:', 'Surface / Model / Project:', 'Artifact actually retrieved',
                       'Read status: FULL_FILE / PARTIAL / NONE', 'Header verification:',
                       'Selection result and application scope:', 'Observed response behavior:',
                       'Fallback attempted?', 'Result: PASS / FAIL / UNVERIFIABLE', 'Notes / prerequisite',
                       'RETRIEVAL FAILURE', 'ROUTING FAILURE', 'IDENTITY FAILURE', 'SCOPE FAILURE',
                       'PLATFORM LIMITATION', 'LOCAL FAILURE != GLOBAL ARCHITECTURE FAILURE',
                       'Memory', 'prior chat', 'Project Sources', 'lookalike', 'UNVERIFIABLE']:
            self.assertIn(anchor, spec)
        self.assertIn('không search toàn Library', spec)
        self.assertIn('không pre-fill PASS', spec)
        self.assertIn('hidden chain-of-thought', spec)
        self.assertIn('NOT EXERCISED / UNVERIFIABLE', spec)

    def test_technical_trial_does_not_change_active_sources(self):
        self.assertEqual(digest(historical_source('domains/technical/TECHNICAL_v1.0.md')),
                         '008e1be28a32fd956ff4ca4edc64536de4e9e3b3b6b7b124ae4ecebdc60b1894')
        self.assertEqual(digest(historical_source('HUB_ROUTER_v1.0.yaml')),
                         '465ecbf6b1c6ff80e1be51a57b6ac3743f19a210f94a36bad185993b4c2de844')
        for name in ['HUB_CI_v1.0.md', 'HUB_ROUTER_v1.0.yaml', 'domains/technical/TECHNICAL_v1.0.md']:
            self.assertNotIn('0.1-trial', (historical_source(name)).read_text(encoding='utf-8'))

    def test_real_technical_candidate_canonical_identity_and_preserved_body(self):
        path = ROOT / 'candidates/HUB-DOM-TECHNICAL_v1.0-candidate.md'
        data = path.read_bytes()
        text = data.decode('utf-8')
        expected = {'Module ID': 'HUB-DOM-TECHNICAL', 'Package ID': 'HUB-PKG-TECHNICAL',
                    'Runtime role': 'REASONING_PROFILE', 'Status': 'CANDIDATE', 'Version': '1.0-candidate'}
        for field, value in expected.items():
            self.assertEqual(re.findall(r'^' + re.escape(field) + r': (.+)$', text, re.M), [value])
        body = data.split(b'\nResponsibility boundary: ', 1)[1].partition(b'\n')[2]
        self.assertEqual(body, (historical_source('domains/technical/TECHNICAL_v1.0.md')).read_bytes().partition(b'\n')[2])
        self.assertEqual(hashlib.sha256(body).hexdigest(),
                         'f11746157aadd0775c29201d1fcef6c29b9947b82ac115da469de0fb65e690f6')
        for prohibited in ['0.1-trial', 'Trial wrapper', 'L04', 'BYTE-IDENTICAL TECHNICAL BODY']:
            self.assertNotIn(prohibited, text)
        for field in ['Refines', 'Complements', 'Requires']:
            self.assertNotRegex(text, r'(?m)^' + field + r':')
        row = next(e for e in load(ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml')['packages']
                   if e['package_id'] == expected['Package ID'])
        self.assertEqual((row['entrypoint_module_id'], row['runtime_role']),
                         (expected['Module ID'], expected['Runtime role']))
        self.assertEqual((row['status'], row['version']), ('ACTIVE', '1.0'))
        architecture = (ROOT / 'candidates/HUB_ARCHITECTURE_v0.1.md').read_text(encoding='utf-8')
        self.assertIn('| REASONING_PROFILE |', architecture)
        self.assertIn('HOW reasoning proceeds', architecture)
        self.assertIn('CURRENT DIRECTORY != ROLE', architecture)
        router = load(ROOT / 'candidates/HUB_ROUTER_v1.1-candidate.yaml')
        self.assertIn('REASONING_PROFILE', router['eligibility']['technical_reconciliation'])
        self.assertEqual(router['status'], 'CANDIDATE')
        self.assertFalse(router['active'])

    def test_live_trial_result_is_scoped_user_report_not_real_deployment(self):
        path = ROOT / 'candidates/library_trial/HUB_TECHNICAL_LIBRARY_LIVE_RESULT.md'
        text = path.read_text(encoding='utf-8')
        self.assertIn('Classification: LIVE VERIFIED — SINGLE MODULE / SCOPED TRIAL', text)
        self.assertIn('Evidence source: USER_REPORTED_LIVE_TRIAL', text)
        self.assertIn('Independent Codex reproduction: NOT_RUN', text)
        self.assertIn('NOT_PROVIDED', text)
        self.assertIn('30/30', text)
        rows = re.findall(r'^\| ([^|]+) \| (PASS|UNVERIFIABLE) \|', text, re.M)
        self.assertEqual(sum(result == 'PASS' for _, result in rows), 10)
        unverified = [label for label, result in rows if result == 'UNVERIFIABLE']
        self.assertEqual(len(unverified), 2)
        self.assertTrue(any('L08' in label for label in unverified))
        self.assertTrue(any('L09' in label for label in unverified))
        self.assertIn('L10 re-entry: PASS', text)
        self.assertIn('TRIAL RETRIEVAL VERIFIED != REAL MODULE DEPLOYED', text)
        catalog = load(ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml')
        self.assertEqual((ROOT / 'candidates' / catalog['trial_evidence_record']).resolve(), path.resolve())
        self.assertFalse(catalog['active'])
        self.assertFalse(catalog['runtime_ready'])

    def test_historical_technical_trial_preparation_remains_byte_exact(self):
        expected = {
            'HUB-DOM-TECHNICAL_v0.1-trial.md': 'a0d7af2e8df7d019b2dfc198269c52a616db0db7d77c3330bc9cf8f55e5715d3',
            'HUB_TECHNICAL_LIBRARY_TRIAL_BINDING.yaml': '4b7d07909d0359febefddcd8aea7ecf1e2c3c8e33fa10203b9bb511c9c3ae4d9',
            'HUB_TECHNICAL_LIBRARY_LIVE_TEST.md': 'bb14903fd17ff18ad9983f828db95698901a5ed8c19497af66dcd38630957a0d',
        }
        for name, sha in expected.items():
            self.assertEqual(digest(ROOT / 'candidates/library_trial' / name), sha)

    def test_technical_promotion_ready_header_and_exact_body_preservation(self):
        candidate = ROOT / 'candidates/HUB-DOM-TECHNICAL_v1.0-candidate.md'
        promoted = ROOT / 'candidates/promotion/HUB-DOM-TECHNICAL_v1.0.md'
        data = promoted.read_bytes()
        text = data.decode('utf-8')
        expected = {'Module ID': 'HUB-DOM-TECHNICAL', 'Package ID': 'HUB-PKG-TECHNICAL',
                    'Runtime role': 'REASONING_PROFILE', 'Status': 'ACTIVE', 'Version': '1.0'}
        for field, value in expected.items():
            self.assertEqual(re.findall(r'^' + re.escape(field) + r': (.+)$', text, re.M), [value])
        for field in ['Scope', 'Responsibility boundary']:
            self.assertEqual(re.findall(r'^' + field + r': (.+)$', text, re.M),
                             re.findall(r'^' + field + r': (.+)$', candidate.read_text(encoding='utf-8'), re.M))
        body = data.split(b'\nResponsibility boundary: ', 1)[1].partition(b'\n')[2]
        self.assertEqual(body, (historical_source('domains/technical/TECHNICAL_v1.0.md')).read_bytes().partition(b'\n')[2])
        self.assertEqual(hashlib.sha256(body).hexdigest(),
                         'f11746157aadd0775c29201d1fcef6c29b9947b82ac115da469de0fb65e690f6')
        for prohibited in ['0.1-trial', '1.0-candidate', 'Trial wrapper', 'L04']:
            self.assertNotIn(prohibited, text)
        for field in ['Refines', 'Complements', 'Requires']:
            self.assertNotRegex(text, r'(?m)^' + field + r':')
        self.assertEqual(digest(candidate), '3a0658abae4fcf1b60336412cc83fe63c157d62a5d412e1cb85312338959bae1')
        self.assertIn('Status: CANDIDATE', candidate.read_text(encoding='utf-8'))

    def test_real_candidate_live_identity_is_not_promoted_locator(self):
        record = (ROOT / 'candidates/library_trial/HUB_TECHNICAL_REAL_CANDIDATE_RESULT.md').read_text(encoding='utf-8')
        ids = {'Candidate file_id': 'file_00000000d3fc8207970927a462f187e2',
               'Candidate library_file_id': 'libfile_54ae9fe83c688191b5dd0a56f9f2444e',
               'Candidate Library version_id': '1'}
        for field, value in ids.items():
            self.assertEqual(re.findall(r'^' + re.escape(field) + r': (.+)$', record, re.M), [value])
        for anchor in ['LIVE VERIFIED — REAL CANDIDATE / SINGLE MODULE / SCOPED',
                       'Evidence source: USER_REPORTED_LIVE_VERIFICATION',
                       '19/19; has_more=false', 'Library version_id != artifact Version field',
                       'CANDIDATE OBJECT IDENTITY != FUTURE ACTIVE OBJECT IDENTITY',
                       'REAL CANDIDATE VERIFIED != ACTIVE REVISION VERIFIED',
                       'PROMOTION-READY != DEPLOYED', 'ROLLBACK PATH != RUNTIME FALLBACK']:
            self.assertIn(anchor, record)
        for case in ['V01', 'V02 deactivation', 'Overall']:
            self.assertIn('| ' + case + ' | PASS |', record)
        self.assertIn('| Fallback | NONE |', record)
        catalog_path = ROOT / 'candidates/HUB_PACKAGE_CATALOG_v0.1.yaml'
        catalog_text = catalog_path.read_text(encoding='utf-8')
        catalog = load(catalog_path)
        self.assertFalse(catalog['active'])
        self.assertFalse(catalog['runtime_ready'])
        row = next(e for e in catalog['packages'] if e['package_id'] == 'HUB-PKG-TECHNICAL')
        self.assertEqual((row['status'], row['version']), ('ACTIVE', '1.0'))
        self.assertIsInstance(row['version'], str)
        self.assertEqual(row['location']['root'], 'Central Hub Config')
        self.assertIsNone(row['location']['locator'])
        self.assertEqual(row['location']['verification'], 'UNRESOLVED')
        self.assertEqual(row['location']['real_module_deployment'], 'NOT_PERFORMED')
        for field in ['file_id', 'library_file_id', 'version_id']:
            self.assertNotIn(field, row['location'])
        for value in list(ids.values())[:2]:
            self.assertNotIn(value, catalog_text)


# Original embedded protocol hash retained as provenance; checked against the extracted preserved protocol.
READY_GATE_SHA = 'c1360811a98e27b6ddabbf008d9b82ffd54610b0bf5a8948c8f37092340fd322'

if __name__ == '__main__':
    unittest.main()
