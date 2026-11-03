"""STATIC/SPEC only: declared semantic matches and synthetic Library reads, no model execution."""
import copy
import re
import subprocess
import unittest
import yaml

from test_hub_contracts import ROOT, load
from test_concept_development import current_fixture, PACKAGE
from test_hub_router_candidate import simulate


AP = 'HUB-DOM-ANTI-PRIOR'
MCA = 'HUB-DOM-MODULAR-CONCEPT-ARCHITECTURE'
WIL = 'HUB-DOM-WORLDBUILDING-INTERNAL-LOGIC'
IDS = (AP, MCA, WIL)
FILES = dict(zip(IDS, ('CH_Anti_Drift_Anti_Prior_01.md',
                       'CH_Anti_Drift_Modular_Concept_Architecture_02.md',
                       'CH_Anti_Drift_Worldbuilding_Internal_Logic_03.md')))
SCOPES = {AP: {'ANTI_PRIOR'}, MCA: {'SYSTEMIC'}, WIL: set()}
BASELINE = '6770d9e632951ac767371b6f42567e4b9299c140'


def configured(active=()):
    local = copy.deepcopy(load(ROOT / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml'))
    for row in local['entries']:
        if row['module_id'] in IDS:
            row['status'] = 'ACTIVE' if row['module_id'] in active else 'INACTIVE'
    return local


def portion_spec(local, scopes, alter=None):
    """Independent acceptance oracle, NOT a runtime selector. Scopes are supplied by fixtures."""
    rows = {identity: [r for r in local['entries'] if r['module_id'] == identity] for identity in IDS}
    states = tuple(rows[k][0]['status'] if len(rows[k]) == 1 else None for k in IDS)
    valid = states in {('INACTIVE', 'INACTIVE', 'INACTIVE'),
                       ('ACTIVE', 'INACTIVE', 'INACTIVE'), ('INACTIVE', 'ACTIVE', 'ACTIVE')}
    fixture = current_fixture()
    projected = fixture['local_catalogs'][PACKAGE]
    for module in projected:
        identity = module['module_id']
        if identity not in IDS:
            continue
        if len(rows[identity]) == 1:
            row = rows[identity][0]
            module.update(status=row['status'], requires=copy.deepcopy(row['requires']),
                          location=copy.deepcopy(row['location']), version=row['version'])
        module['scopes'] = SCOPES[identity] if valid else set()
        # Artifact eligibility is ACTIVE; catalog INACTIVE prevents selection before any read.
        record = dict(copy.deepcopy(module), status='ACTIVE', read_kind='FULL_FILE')
        fixture['artifacts'][identity] = [record]
    if alter:
        alter(fixture)
    result = simulate(fixture, scopes)
    result['configuration_error'] = not valid
    result['blocked_anti_drift_portion'] = not valid and bool(set(scopes) & {'ANTI_PRIOR', 'SYSTEMIC'})
    return result


def verified(result):
    return {identity for _, identity in result['spec_verified']}


class AntiDriftSpecTests(unittest.TestCase):
    def test_C0_baseline_all_inactive_preserves_existing_selections(self):
        local = configured()
        for scopes in (set(), {'CORE'}, {'CREATIVE'}, {'BRAINSTORM'}, {'CREATIVE', 'BRAINSTORM'}):
            expected = simulate(current_fixture(), scopes)
            actual = portion_spec(local, scopes)
            for field in ('planned', 'spec_verified', 'blocked', 'artifact_requests', 'module_scopes'):
                self.assertEqual(actual[field], expected[field])
            self.assertFalse(set(IDS) & set(actual['artifact_requests']))
        result = portion_spec(local, {'CREATIVE', 'ANTI_PRIOR', 'SYSTEMIC'})
        self.assertEqual(verified(result), {'HUB-DOM-CREATIVE'})
        self.assertFalse(result['configuration_error'])

    def test_A1_A2_A3_scoped_selection_and_no_mode(self):
        local = configured([AP])
        snapshot = copy.deepcopy(local)
        results = [portion_spec(local, scopes) for scopes in
                   ({'CREATIVE'}, {'CREATIVE', 'ANTI_PRIOR'}, {'CREATIVE'})]
        self.assertEqual([AP in verified(r) for r in results], [False, True, False])
        self.assertEqual(results[1]['module_scopes'][(PACKAGE, AP)], {'ANTI_PRIOR'})
        for result in results:
            self.assertFalse({MCA, WIL} & set(result['artifact_requests']))
        self.assertEqual(local, snapshot)

    def test_B1_B2_both_verified_on_same_portion_only_through_one_way_requires(self):
        local = configured([MCA, WIL])
        self.assertFalse(set(IDS) & verified(portion_spec(local, {'CREATIVE'})))
        result = portion_spec(local, {'CREATIVE', 'SYSTEMIC'})
        self.assertTrue({MCA, WIL} <= verified(result))
        self.assertIn((PACKAGE, MCA), result['planned'])
        self.assertNotIn((PACKAGE, WIL), result['planned'])
        self.assertEqual(result['direct_dependencies'], [((PACKAGE, MCA), (PACKAGE, WIL))])
        self.assertEqual(result['module_scopes'][(PACKAGE, MCA)], {'SYSTEMIC'})
        self.assertEqual(result['module_scopes'][(PACKAGE, MCA)], result['module_scopes'][(PACKAGE, WIL)])
        self.assertNotIn(AP, result['artifact_requests'])
        self.assertFalse(result['runtime_ready'])

    def test_B3_failed_companion_blocks_entire_pair_and_preserves_independent_work(self):
        def missing(f):
            f['artifacts'].pop(WIL)

        def unresolved(f):
            f['artifacts'][WIL][0]['read_kind'] = 'UNRESOLVED'

        def wrong_header(f):
            f['artifacts'][WIL][0]['version'] = 'wrong'

        def wrong_body(f):
            f['artifacts'][WIL][0]['requires'] = [{'module_id': MCA}]

        def duplicate(f):
            f['artifacts'][WIL] *= 2

        def wrong_root(f):
            row = next(m for m in f['local_catalogs'][PACKAGE] if m['module_id'] == WIL)
            row['location']['root'] = 'Other Root'

        def inactive(f):
            f['artifacts'][WIL][0]['status'] = 'INACTIVE'

        for failure in (missing, unresolved, wrong_header, wrong_body, duplicate, wrong_root, inactive):
            with self.subTest(failure=failure.__name__):
                result = portion_spec(configured([MCA, WIL]), {'CREATIVE', 'SYSTEMIC'}, failure)
                self.assertFalse({MCA, WIL} & verified(result))
                self.assertIn((PACKAGE, MCA), result['blocked'])
                self.assertIn('HUB-DOM-CREATIVE', verified(result))
                self.assertNotIn(AP, result['artifact_requests'])
        result = portion_spec(configured([MCA]), {'SYSTEMIC'})  # catalog-inactive WIL
        self.assertTrue(result['blocked_anti_drift_portion'])
        self.assertFalse(set(IDS) & verified(result))

    def test_X1_all_status_combinations_no_winner_and_malformed_inventory(self):
        for mask in range(8):
            active = [identity for bit, identity in enumerate(IDS) if mask & (1 << bit)]
            result = portion_spec(configured(active), {'CREATIVE', 'ANTI_PRIOR', 'SYSTEMIC'})
            valid = mask in {0, 1, 6}
            self.assertEqual(result['configuration_error'], not valid)
            if not valid:
                self.assertTrue(result['blocked_anti_drift_portion'])
                self.assertFalse(set(IDS) & verified(result))
                self.assertFalse(set(IDS) & set(result['artifact_requests']))
                self.assertIn('HUB-DOM-CREATIVE', verified(result))
        for malformed in ('missing', 'duplicate', 'status'):
            local = configured([MCA, WIL])
            row = next(r for r in local['entries'] if r['module_id'] == WIL)
            if malformed == 'missing':
                local['entries'].remove(row)
            elif malformed == 'duplicate':
                local['entries'].append(copy.deepcopy(row))
            else:
                row['status'] = 'CANDIDATE'
            self.assertTrue(portion_spec(local, {'SYSTEMIC'})['blocked_anti_drift_portion'])

    def test_R1_R4_declared_negative_controls_and_scoped_hypothetical(self):
        # Declared semantic classifications; tests do not interpret prose or produce fictional outcomes.
        cases = {
            'R1 complete-premise dialogue realization': {'CREATIVE'},
            'R2 explicit conventional Earth-feudal trope': {'CREATIVE'},
            'R3 blank-slate imagery freely invented': {'BRAINSTORM'},
            'R4 openly invented branch with no system/architecture need': {'BRAINSTORM'},
        }
        for label, scopes in cases.items():
            for enabled in ([AP], [MCA, WIL]):
                with self.subTest(case=label, enabled=enabled):
                    self.assertFalse(set(IDS) & verified(portion_spec(configured(enabled), scopes)))
        # A systemic hypothetical is allowed; B may help develop it without accepting it as canon.
        branch = portion_spec(configured([MCA, WIL]), {'BRAINSTORM', 'SYSTEMIC'})
        self.assertTrue({MCA, WIL, 'HUB-CAP-BRAINSTORM'} <= verified(branch))

    def test_R5_generic_regression_fixture_and_actor_path_unknowns(self):
        fixture = {
            'surface': ('castle', 'sword', 'horse', 'magic'),
            'established': ('independent magic-technology integration', 'digital-like payment terminals',
                            'complex institutions', 'non-Earth development path'),
            'visitor': ('modern human', 'cellphone', 'Jeep'),
            'unsupported': ('castle -> Earth feudalism', 'sword/horse -> low overall technology',
                            'magic -> technology substitute', 'cellphone/Jeep -> automatic superiority',
                            'modern human -> civilization/knowledge advantage',
                            'nobility -> confiscation/patronage authority',
                            'visual medievality -> institutional medievality'),
            'protected_unknowns': ('who receives the signal', 'who understands it',
                                   'who may seize the object', 'who can act'),
        }
        self.assertEqual(len(fixture['unsupported']), 7)
        self.assertEqual(len(fixture['protected_unknowns']), 4)
        # Supported current state plus material unknowns establish declared AP/systemic matches.
        for enabled, expected in (([AP], {AP}), ([MCA, WIL], {MCA, WIL})):
            result = portion_spec(configured(enabled), {'CREATIVE', 'BRAINSTORM', 'ANTI_PRIOR', 'SYSTEMIC'})
            self.assertEqual(verified(result) & set(IDS), expected)
            self.assertFalse(result['runtime_ready'])
        self.assertFalse(set(IDS) & verified(portion_spec(configured(), {'ANTI_PRIOR', 'SYSTEMIC'})))


class AntiDriftStaticTests(unittest.TestCase):
    def test_headers_bindings_requires_and_baseline_configuration(self):
        local = configured()
        for identity in IDS:
            row = next(r for r in local['entries'] if r['module_id'] == identity)
            text = (ROOT / 'library_modules' / FILES[identity]).read_text(encoding='utf-8')
            for key, value in (('Module ID', identity), ('Package ID', PACKAGE),
                               ('Runtime role', 'DOMAIN_CONTROL'), ('Status', 'ACTIVE'), ('Version', '1.0')):
                self.assertEqual(re.findall('^' + key + r': (.+)$', text, re.M), [value])
            self.assertEqual(row['status'], 'INACTIVE')
            self.assertEqual(row['location']['class'], 'LIBRARY')
            self.assertEqual(row['location']['root'], 'Central Hub Config')
            for key in ('locator', 'library_file_id', 'library_version_id'):
                self.assertIsNone(row['location'][key])
            self.assertEqual(row['requires'], [{'module_id': WIL}] if identity == MCA else [])
            self.assertEqual(re.findall(r'^Requires: (.+)$', text, re.M), [WIL] if identity == MCA else [])
            self.assertEqual(row['refines'], [])
            self.assertEqual(row['complements'], [])
        self.assertIn('Dependency-only', next(r for r in local['entries'] if r['module_id'] == WIL)['applicability'])

    def test_preserved_creative_brainstorm_and_upstream_files(self):
        def original(relative):
            return subprocess.check_output(['git', 'show', BASELINE + ':Central Hub/' + relative], cwd=ROOT)
        old_catalog = yaml.safe_load(original('library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.0.yaml'))
        archive = ROOT / 'Source_archive/Concept explicit leaf controls 2026-11-02'
        current = load(archive / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.0.yaml')
        for row in old_catalog['entries']:
            self.assertEqual(row, next(r for r in current['entries'] if r['module_id'] == row['module_id']))
        self.assertEqual({k: v for k, v in current.items() if k not in {'entries', 'anti_drift_configuration'}},
                         {k: v for k, v in old_catalog.items() if k != 'entries'})
        core = (archive / 'library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.0.md').read_text(encoding='utf-8')
        before, added = core.split('### Optional anti-drift experiment\n\n', 1)
        tail = added[added.index('This package and its leaves select no other package'):]
        self.assertEqual(before + tail, original('library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.0.md').decode('utf-8'))
        successor = (ROOT / 'library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md').read_text(encoding='utf-8')
        expected = core.split('### Optional anti-drift experiment', 1)[1].replace(
            'their existing zero/one/both selection remains independent', 'their explicit span selection remains independent')
        self.assertEqual(successor.split('### Optional anti-drift experiment', 1)[1], expected)
        for relative in ('HUB_CI_v1.1.md', 'HUB_ROUTER_v1.1.yaml', 'HUB_ARCHITECTURE_v1.3.md',
                         'HUB_PACKAGE_CATALOG_v1.3.yaml', 'library_modules/HUB-DOM-CREATIVE_v1.1.md',
                         'library_modules/HUB-CAP-BRAINSTORM_v1.1.md'):
            path = ROOT / relative
            if relative in {'HUB_ROUTER_v1.1.yaml', 'HUB_ARCHITECTURE_v1.3.md', 'HUB_PACKAGE_CATALOG_v1.3.yaml'}:
                path = ROOT / 'Source_archive/Authoring 0.4 promotion 2026-11-01' / relative
            self.assertEqual(path.read_bytes(), original(relative))

    def test_port_fidelity_all_sections_retained_and_unaffected_sections_exact(self):
        source_root = ROOT.parent / 'Project Feather Core/Anti-Drift Source'
        cases = ((MCA, 'Modular_Concept_Architecture', {4, 13, 14, 15, 18, 20, 21}),
                 (WIL, 'Worldbuilding_Internal_Logic', {2, 15, 20, 21}))
        for identity, name, changed in cases:
            source = (source_root / f'FTH_Anti_Drift_{name}_v1.2.md').read_text(encoding='utf-8')
            port = (ROOT / 'library_modules' / FILES[identity]).read_text(encoding='utf-8')
            source_sections = re.split(r'(?m)^# (\d+)\. ', source)[1:]
            port_sections = re.split(r'(?m)^# (\d+)\. ', port)[1:]
            old = dict(zip(map(int, source_sections[::2]), source_sections[1::2]))
            new = dict(zip(map(int, port_sections[::2]), port_sections[1::2]))
            self.assertEqual(set(old), set(range(1, 22)))
            self.assertEqual(set(new), set(old))
            for section in old:
                self.assertEqual(old[section].splitlines()[0], new[section].splitlines()[0])
                if section not in changed:
                    self.assertEqual(new[section], old[section], (identity, section))
            self.assertNotRegex(port, r'FTH_Anti_Drift_|PROMPT_ROUTE_ONLY|PROMPT_EXECUTION|active Source Router')
            self.assertIn('UNKNOWN', port)
            self.assertIn('Hub CI', port)
            self.assertIn('Stop Rule', port)
        # Lifecycle substantive text is preserved except the two required authority/owner adaptations.
        old_lifecycle = (source_root / 'FTH_Anti_Drift_Modular_Concept_Architecture_v1.2.md').read_text(encoding='utf-8').split('## Conditional Response Lifecycle\n')[1].split('\n---')[0]
        new_lifecycle = (ROOT / 'library_modules' / FILES[MCA]).read_text(encoding='utf-8').split('## Conditional Response Lifecycle\n')[1].split('\n---')[0]
        old_lifecycle = old_lifecycle.replace('under the CI/Router.', 'under Hub CI and the task-declared source/admission process.')
        old_lifecycle = re.sub(r'This subsection owns branch distinctions only\..*?\n\n', '', old_lifecycle, flags=re.S)
        new_lifecycle = re.sub(r'This subsection owns branch distinctions only\..*?\n\n', '', new_lifecycle, flags=re.S)
        self.assertEqual(new_lifecycle, old_lifecycle)

    def test_reviewed_failure_guards_not_model_behavior_proof(self):
        ap = (ROOT / 'library_modules' / FILES[AP]).read_text(encoding='utf-8')
        for distinction in ('SURFACE / LABEL / AESTHETIC / ANALOGY != SYSTEM PREMISE',
                            'CREATIVE GAP != MATERIAL / PROTECTED UNKNOWN',
                            'SEES != UNDERSTANDS != BELIEVES != VALUES != HAS AUTHORITY != HAS CAPABILITY != ACTS',
                            'DIFFERENT IMPLEMENTATION != LOWER / HIGHER CIVILIZATION',
                            'ONE CAPABILITY != SYSTEM-WIDE DEVELOPMENT LEVEL'):
            self.assertIn(distinction, ap)
        for phrase in ('Use a supported premise normally', 'branch assumption/proposal',
                       'if unnecessary, do not introduce it', 'Do not validate the full output',
                       'explicitly permitted blank-slate invention', 'requested conventional trope',
                       'no mandatory checklist', 'never a persistent anti-drift mode'):
            self.assertIn(phrase, ap)
        core = (ROOT / 'library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md').read_text(encoding='utf-8')
        for phrase in ('CONTROL AVAILABLE != CONTROL SELECTED FOR CURRENT TASK',
                       'PREVIOUS SELECTION != CURRENT SELECTION', 'never execute MCA alone',
                       'WIL is never an independent selection', 'select no winner/fallback'):
            self.assertIn(phrase, core)

    def test_utf8_no_bom_lf_and_exact_library_hints(self):
        for identity, filename in FILES.items():
            data = (ROOT / 'library_modules' / filename).read_bytes()
            self.assertFalse(data.startswith(b'\xef\xbb\xbf'))
            text = data.decode('utf-8', errors='strict')
            self.assertNotIn('\r', text)
            self.assertTrue(text.endswith('\n'))
            self.assertFalse(any(line.rstrip() != line for line in text.splitlines()))
            self.assertIn(identity, text)


if __name__ == '__main__':
    unittest.main()
