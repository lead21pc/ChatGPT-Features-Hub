"""STATIC / declared SPEC fixtures only; no LLM, Library, deployment or canon execution."""
import copy
from pathlib import Path
import re
import subprocess
import unittest

from test_hub_contracts import ROOT, CONCEPT_ARCHIVE, load
from test_hub_router_candidate import synthetic_module, synthetic_fixture, simulate, integration_read_spec
from test_hub_contracts import Closed


PACKAGE = 'HUB-PKG-CONCEPT-DEVELOPMENT'
CORE = 'HUB-DOM-CONCEPT-DEVELOPMENT'
CATALOG = 'HUB-CATALOG-CONCEPT-DEVELOPMENT'
BASELINE = 'ee104645e89939341cd45deba465b5d71da64521'


def current_fixture():
    """Project interfaces into the SPEC oracle; specialized scopes declare already-valid explicit invocations, not semantic auto-selection."""
    core = synthetic_module(CORE, PACKAGE, {'CORE', 'CREATIVE', 'DEBATE', 'BRAINSTORM'}, version='1.1')
    fixture = synthetic_fixture(core)
    catalog = synthetic_module(CATALOG, PACKAGE, set(), role='PACKAGE_CATALOG', version='1.1')
    fixture['packages'][0]['local_catalog'] = catalog
    fixture['artifacts'][CATALOG] = [dict(copy.deepcopy(catalog), read_kind='FULL_FILE')]
    local = load(ROOT / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml')
    leaves = []
    scopes = {'HUB-DOM-CREATIVE': {'CREATIVE'}, 'HUB-CAP-BRAINSTORM': {'BRAINSTORM'}, 'HUB-CAP-DEBATE': {'DEBATE'}}
    for row in local['entries']:
        leaf = synthetic_module(row['module_id'], row['package_id'], scopes.get(row['module_id'], set()),
                                role=row['runtime_role'], version=row['version'],
                                status=row['status'], requires=copy.deepcopy(row['requires']),
                                location=copy.deepcopy(row['location']))
        leaves.append(leaf)
        fixture['artifacts'][leaf['module_id']] = [dict(copy.deepcopy(leaf), read_kind='FULL_FILE')]
    fixture['local_catalogs'][PACKAGE] = leaves
    return fixture


class ConceptDevelopmentTests(unittest.TestCase):
    def setUp(self):
        self.root = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.10.yaml')
        self.local = load(ROOT / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml')
        self.core = (ROOT / 'library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md').read_text(encoding='utf-8')
        self.notes = (ROOT / 'CONCEPT_DEVELOPMENT_MIGRATION.md').read_text(encoding='utf-8')

    def test_six_root_owners_and_package_local_inventory(self):
        self.assertEqual(self.root['version'], '1.10')
        self.assertEqual({p['package_id'] for p in self.root['packages']},
                         {'HUB-PKG-TECHNICAL', PACKAGE, 'HUB-PKG-AUTHORING',
                          'HUB-PKG-AIS', 'HUB-PKG-IMAGET', 'HUB-PKG-SHOPPING'})
        package = next(p for p in self.root['packages'] if p['package_id'] == PACKAGE)
        self.assertEqual((package['entrypoint_module_id'], package['runtime_role'], package['version']),
                         (CORE, 'DOMAIN_CONTROL', '1.1'))
        self.assertEqual(package['binding_mode'], 'LIBRARY_MODULE')
        self.assertEqual(package['requires'], [])
        self.assertEqual(package['local_catalog']['module_id'], CATALOG)
        self.assertEqual(package['local_catalog']['package_id'], PACKAGE)
        self.assertEqual((self.local['module_id'], self.local['package_id'], self.local['runtime_role'],
                          self.local['status'], self.local['version']),
                         (CATALOG, PACKAGE, 'PACKAGE_CATALOG', 'ACTIVE', '1.1'))
        self.assertEqual({p['module_id'] for p in self.local['entries']},
                         {'HUB-DOM-CREATIVE', 'HUB-CAP-DEBATE', 'HUB-CAP-BRAINSTORM', 'HUB-DOM-ANTI-PRIOR',
                          'HUB-DOM-MODULAR-CONCEPT-ARCHITECTURE',
                          'HUB-DOM-WORLDBUILDING-INTERNAL-LOGIC'})
        for leaf_name in ['HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM', 'thử động não', 'brainstorm sâu']:
            self.assertNotIn(leaf_name, str(self.root))  # Root knows only the package interface.

    @unittest.skip("Historical provenance check: run the original suite in ChatGPT-Creative-Workshops")
    def test_router_changes_only_exact_pins_and_global_owners_stay(self):
        previous = load(CONCEPT_ARCHIVE / 'HUB_ROUTER_v1.1.yaml')
        expected = copy.deepcopy(previous)
        for key, name in [('architecture', 'HUB_ARCHITECTURE_v1.10.md'),
                          ('root_catalog', 'HUB_PACKAGE_CATALOG_v1.10.yaml')]:
            expected['contracts'][key]['file'] = name
            expected['contracts'][key]['version'] = '1.10'
        expected['contracts']['binding_scope'] = load(ROOT / 'HUB_ROUTER_v1.1.yaml')['contracts']['binding_scope']
        self.assertEqual(load(ROOT / 'HUB_ROUTER_v1.1.yaml'), expected)
        before = load(CONCEPT_ARCHIVE / 'HUB_PACKAGE_CATALOG_v1.0.yaml')
        for package in ['HUB-PKG-TECHNICAL', 'HUB-PKG-AIS']:
            self.assertEqual(next(p for p in before['packages'] if p['package_id'] == package),
                             next(p for p in self.root['packages'] if p['package_id'] == package))
        image = copy.deepcopy(next(p for p in before['packages'] if p['package_id'] == 'HUB-PKG-IMAGET'))
        image['version'] = '1.2'
        image['location']['declared_source_path'] = 'tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2.md'
        image['location']['source_name'] = 'IMAGE_CONTROLLER_v1.2.md'
        self.assertEqual(image, next(p for p in self.root['packages'] if p['package_id'] == 'HUB-PKG-IMAGET'))
        original = subprocess.check_output(['git', 'show', BASELINE + ':Central Hub/HUB_CI_v1.1.md'], cwd=ROOT)
        self.assertEqual((ROOT / 'HUB_CI_v1.1.md').read_bytes(), original)

    def test_library_headers_ownership_and_exact_leaf_revisions(self):
        for module, version, role in [(CORE, '1.1', 'DOMAIN_CONTROL'),
                                      ('HUB-CAP-DEBATE', '1.0', 'CAPABILITY'),
                                      ('HUB-DOM-CREATIVE', '1.1', 'DOMAIN_CONTROL'),
                                      ('HUB-CAP-BRAINSTORM', '1.1', 'CAPABILITY')]:
            text = (ROOT / f'library_modules/{module}_v{version}.md').read_text(encoding='utf-8')
            for key, value in [('Module ID', module), ('Package ID', PACKAGE), ('Runtime role', role),
                               ('Status', 'ACTIVE'), ('Version', version)]:
                self.assertEqual(re.findall(r'^' + key + r': (.+)$', text, re.M), [value])
        for row in self.local['entries']:
            self.assertEqual(row['package_id'], PACKAGE)
            if row['module_id'] in {'HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM'}:
                self.assertEqual(row['version'], '1.1')
                self.assertEqual(row['requires'], [])
        previous = (CONCEPT_ARCHIVE / 'library_modules/HUB-CAP-BRAINSTORM_v1.0.md').read_bytes()
        current = (ROOT / 'library_modules/HUB-CAP-BRAINSTORM_v1.1.md').read_bytes()
        marker = b'## Branching by premise change'
        self.assertEqual(previous.split(marker, 1)[1], current.split(marker, 1)[1])

    def test_C01_C07_core_only_and_C02_C03_C04_scoped_leaves(self):
        # Declared valid explicit invocations exercise the existing growing-package closure/read oracle.
        cases = [('C01', {'CORE'}, set()), ('C07', {'CORE'}, set()),
                 ('C02', {'CREATIVE'}, {'HUB-DOM-CREATIVE'}),
                 ('C03', {'BRAINSTORM'}, {'HUB-CAP-BRAINSTORM'}),
                 ('C04', {'CREATIVE', 'BRAINSTORM'}, {'HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM'})]
        for case, scopes, leaves in cases:
            with self.subTest(case=case):
                result = simulate(current_fixture(), scopes)
                self.assertEqual({module for _, module in result['planned']}, leaves)
                self.assertEqual(result['spec_reads'][:2], [CORE, CATALOG])
                self.assertEqual(result['local_catalogs_consulted'], [PACKAGE])
                self.assertFalse(result['pipeline_entrypoints'])
                self.assertFalse(result['runtime_ready'])
                self.assertIn('| ' + case + ' |', self.notes)

    def test_C05_C09_baseline_and_no_route_inertia(self):
        fixture = current_fixture()
        original = copy.deepcopy(fixture)
        routes = []
        for scopes in [set(), {'BRAINSTORM'}, set()]:
            result = simulate(fixture, scopes)
            routes.append({module for _, module in result['planned']})
            if not scopes:
                self.assertEqual(result['artifact_requests'], [])
        self.assertEqual(routes, [set(), {'HUB-CAP-BRAINSTORM'}, set()])
        self.assertEqual(fixture, original)
        old = load(CONCEPT_ARCHIVE / 'HUB_PACKAGE_CATALOG_v1.0.yaml')
        old_brain = next(p for p in old['packages'] if p['package_id'] == 'HUB-PKG-BRAINSTORM')
        brain = next(p for p in self.local['entries'] if p['module_id'] == 'HUB-CAP-BRAINSTORM')
        self.assertNotEqual(brain['applicability'], old_brain['applicability'])
        self.assertEqual(brain['activation'], '/BRAINSTORM')
        self.assertIn('SELECT ONLY FOR A VALID EXPLICIT CONTROL SPAN', brain['applicability'])
        for phrase in ['thử động não', 'brainstorm sâu', 'semantically equivalent imperatives']:
            self.assertNotIn(phrase, brain['applicability'])

    def test_C08_missing_leaf_and_catalog_block_dependent_only(self):
        fixture = current_fixture()
        del fixture['artifacts']['HUB-CAP-BRAINSTORM']
        result = simulate(fixture, {'CREATIVE', 'BRAINSTORM'})
        self.assertIn((PACKAGE, 'HUB-CAP-BRAINSTORM'), result['blocked'])
        self.assertIn((PACKAGE, 'HUB-DOM-CREATIVE'), result['spec_verified'])
        self.assertTrue(all('repository' not in item.lower() for item in result['artifact_requests']))
        fixture = current_fixture()
        del fixture['artifacts'][CATALOG]
        result = simulate(fixture, {'BRAINSTORM'})
        self.assertIn(PACKAGE, result['blocked'])
        self.assertNotIn('HUB-CAP-BRAINSTORM', result['spec_reads'])
        for read_kind in ['HEADER_ONLY', 'SNIPPET']:
            fixture = current_fixture()
            fixture['artifacts']['HUB-CAP-BRAINSTORM'][0]['read_kind'] = read_kind
            self.assertIn((PACKAGE, 'HUB-CAP-BRAINSTORM'), simulate(fixture, {'BRAINSTORM'})['blocked'])

    def test_verified_library_bindings_preserve_runtime_evidence_boundary(self):
        package = next(p for p in self.root['packages'] if p['package_id'] == PACKAGE)
        self.assertTrue(self.root['runtime_ready'])  # Root eligibility remains distinct from live execution.
        locations = {
            CORE: package['location'],
            CATALOG: package['local_catalog']['location'],
            **{row['module_id']: row['location'] for row in self.local['entries']
               if row['module_id'] in {'HUB-DOM-CREATIVE', 'HUB-CAP-BRAINSTORM'}},
        }
        expected = {
            CORE: ('libfile_25fe61415e408191b974235fa6608edf',
                   'file_00000000e0e48211989902592a6479f8',
                   'Central Hub Config/HUB-DOM-CONCEPT-DEVELOPMENT_v1.0.md'),
            CATALOG: ('libfile_a7fa47cd4e10819194237840dde6c86f',
                      'file_00000000c62482078eb5f87f6885de71',
                      'Central Hub Config/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.0.yaml'),
            'HUB-DOM-CREATIVE': ('libfile_9a5f1f01a39c8191b3b299cbe8c03b8b',
                                 'file_000000005f1482079a499865628b7576',
                                 'Central Hub Config/HUB-DOM-CREATIVE_v1.1.md'),
            'HUB-CAP-BRAINSTORM': ('libfile_9573068db03081918819492a2f297377',
                                   'file_000000008a6c8211b0b9236c790d343f',
                                   'Central Hub Config/HUB-CAP-BRAINSTORM_v1.1.md'),
        }
        for module, location in locations.items():
            if module in {CORE, CATALOG}:
                self.assertEqual(location['resolution'], 'UNRESOLVED')
                self.assertEqual(location['verification'], 'NOT_PERFORMED')
                self.assertIsNone(location['library_file_id'])
                self.assertIsNone(location['library_version_id'])
                continue
            self.assertEqual(location['root'], 'Central Hub Config')
            self.assertEqual(location['verification'], 'CHATGPT_OBSERVED_FULL_FILE_BYTE_EXACT_VERIFIED')
            self.assertEqual(location['resolution'], 'RESOLVED')
            self.assertEqual((location['library_file_id'], location['observed_surface_file_id'],
                              location['observed_path']), expected[module])
            self.assertEqual(location['duplicate_check'],
                             'NO_DUPLICATE_OBSERVED_IN_INSPECTED_CENTRAL_HUB_CONFIG_SCOPE')
            self.assertIsNone(location['locator'])
            self.assertIsNone(location['library_version_id'])  # Artifact Version does not infer Library revision.
            self.assertNotIn('PROJECT_SOURCE', str(location))
        evidence = self.root['concept_development_evidence']
        self.assertEqual(evidence['library_evidence_basis'],
                         'CHATGPT_OBSERVED / USER_PROVIDED; not independently reproduced by Codex')
        self.assertEqual(evidence['runtime_evidence_basis'],
                         'USER_CONFIRMED_LIVE_PASS; not independently reproduced by Codex')
        self.assertEqual(evidence['hub_runtime_retrieval'], 'NOT_VERIFIED')
        self.assertEqual(evidence['central_hub_project_switch'],
                         'USER_CONFIRMED_FOR_INTEGRATED_RUNTIME_SMOKE')
        self.assertEqual(evidence['live_routing'],
                         'USER_CONFIRMED_PASS_FOR_INTEGRATED_RUNTIME_SMOKE_2026_10_27')
        self.assertEqual(evidence['c01_c12_live'], 'NOT_RUN')
        self.assertNotIn('LIVE_VERIFIED', str(self.root))
        row = next(p for p in self.local['entries'] if p['module_id'] == 'HUB-CAP-BRAINSTORM')
        entry = dict(row, entrypoint_module_id=row['module_id'], binding_mode='LIBRARY_MODULE')
        observed = dict(module_id=row['module_id'], package_id=PACKAGE, runtime_role='CAPABILITY',
                        status='ACTIVE', version='1.1', root='Central Hub Config', location='LIBRARY',
                        read_kind='FULL_FILE', has_more=False, body_matches=True,
                        library_file_id=row['location']['library_file_id'])
        result = integration_read_spec(entry, [observed])
        self.assertFalse(result['runtime_ready'])
        self.assertEqual(result['live_integration'], 'NOT_RUN')
        self.assertIsNone(result['library_version_id'])
        for key, wrong in [('version', '1.0'), ('package_id', 'HUB-PKG-BRAINSTORM'),
                           ('root', 'Other root'), ('location', 'repository')]:
            with self.subTest(key=key), self.assertRaises(Closed):
                integration_read_spec(entry, [dict(observed, **{key: wrong})],
                                      direct_identity_usable=True)

    def test_C06_C10_C11_scoped_reasoning_contract_not_behavioral_proof(self):
        # REVIEWED_TEXT guards; only a real model run can establish these behaviors.
        for phrase in ['Institutions only when material', 'Do not run an institutional checklist',
                       'Do not emit an irrelevant-axis or NOT MATERIAL report',
                       'Incidental appeal is not a defect', 'realization of a branch does not accept it',
                       'Findings do not authorize redesign', 'Introduce a primitive only when',
                       'INTERACTION != CONTAINMENT', 'CO-OCCURRENCE != DEPENDENCY',
                       'POWER != AUTHORITY', 'CHRONOLOGY != CAUSALITY',
                       'COOPERATION != PERMANENT COUPLING']:
            self.assertIn(phrase, self.core)
        for duplicate in ['CONTROL GROUNDING:', 'DISCOURSE FIDELITY:', 'EPISTEMIC NON-ESCALATION:',
                          '## Output Contract', '## Explanation and Reader Calibration']:
            self.assertNotIn(duplicate, self.core)
        self.assertEqual(re.findall(r'^\| (C\d{2}) \|', self.notes, re.M), [f'C{i:02}' for i in range(1, 13)])

    @unittest.skip("Historical provenance check: run the original suite in ChatGPT-Creative-Workshops")
    def test_C12_retirement_and_predecessor_bytes(self):
        for relative in ['HUB_PACKAGE_CATALOG_v1.0.yaml', 'HUB_ARCHITECTURE_v1.0.md',
                         'library_modules/HUB-DOM-CREATIVE_v1.0.md',
                         'library_modules/HUB-CAP-BRAINSTORM_v1.0.md', 'HUB_LIBRARY_SINGLETON_MIGRATION.md',
                         'HUB_ROUTER_v1.1.yaml']:
            original = subprocess.check_output(['git', 'show', BASELINE + ':Central Hub/' + relative], cwd=ROOT)
            self.assertEqual((CONCEPT_ARCHIVE / relative).read_bytes(), original)
            if relative != 'HUB_ROUTER_v1.1.yaml':
                self.assertFalse((ROOT / relative).exists())
        mini = ROOT.parent / 'llm-controls/project-instruction-designs/Project CI'
        for version in ['2.1', '2.2']:
            name = f'miniConcept_CI_v{version}.md'
            original = subprocess.check_output(['git', 'show', BASELINE + ':llm-controls/project-instruction-designs/Project CI/' + name], cwd=ROOT)
            self.assertEqual((mini / 'source_archive' / name).read_bytes(), original)
            self.assertFalse((mini / name).exists())
        for text in [str(self.root), str(self.local), self.core,
                     (ROOT / 'library_modules/HUB-DOM-CREATIVE_v1.1.md').read_text(encoding='utf-8'),
                     (ROOT / 'library_modules/HUB-CAP-BRAINSTORM_v1.1.md').read_text(encoding='utf-8')]:
            self.assertNotIn('miniConcept_CI', text)
            self.assertNotIn('Source_archive', text)


def leaf_span_spec(parts):
    """Test-only lexical acceptance oracle, NOT a deployed parser or provenance detector.

    Fixtures label directive/source/quote/code roles. Real platform role detection and
    model compliance require live evidence. Offsets preserve the original context.
    """
    text = ''.join(body for role, body in parts)
    directive = [role == 'USER_DIRECTIVE' for role, body in parts for _ in body]
    local = load(ROOT / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml')
    openers = {row['activation']: row['module_id'] for row in local['entries'] if 'activation' in row}
    tokens = re.compile(r'(?<![\w/])/(?:CREATIVE|DEBATE|BRAINSTORM)(?=\s|$)|(?<!\S)#(?=\s|$)')
    invocations, blocked, occupied = [], [], []
    opened = None
    invalid = False
    for match in tokens.finditer(text):
        if not all(directive[match.start():match.end()]):
            continue
        token = match.group()
        if token in openers:
            if opened is None:
                opened = match
            else:
                invalid = True  # Never implicitly close/switch at a second opener.
        elif opened is not None:
            content = text[opened.end():match.start()]
            span = (opened.start(), match.end())
            occupied.append(span)
            if invalid or not content.strip():
                blocked.append(span)
            else:
                invocations.append((openers[opened.group()], content.strip()))
            opened, invalid = None, False
    if opened is not None:
        blocked.append((opened.start(), len(text)))
        occupied.append((opened.start(), len(text)))
    unscoped, start = [], 0
    for left, right in occupied:
        unscoped.append(text[start:left])
        start = right
    unscoped.append(text[start:])
    return dict(invocations=invocations, blocked=blocked, unscoped=unscoped, context=text)


class ExplicitLeafControlTests(unittest.TestCase):
    def spec(self, text):
        return leaf_span_spec([('USER_DIRECTIVE', text)])

    def test_three_canonical_controls_and_exact_content(self):
        for opener, identity, content in [('/CREATIVE', 'HUB-DOM-CREATIVE', 'make X.'),
                                          ('/DEBATE', 'HUB-CAP-DEBATE', 'challenge X.'),
                                          ('/BRAINSTORM', 'HUB-CAP-BRAINSTORM', 'reverse assumption X.')]:
            with self.subTest(opener=opener):
                result = self.spec(f'{opener} {content} #')
                self.assertEqual(result['invocations'], [(identity, content)])
                self.assertEqual(result['blocked'], [])
                # Feed explicit selections into existing closure/read/failure oracle.
                scopes = {opener[1:]}
                routed = simulate(current_fixture(), scopes)
                self.assertEqual({module for _, module in routed['planned']}, {identity})
                self.assertFalse(routed['runtime_ready'])

    def test_mid_sentence_multiline_and_context_visibility(self):
        result = self.spec('Constraints A, B. I want /CREATIVE design X\nusing A and B. # but preserve Y.')
        self.assertEqual(result['unscoped'], ['Constraints A, B. I want ', ' but preserve Y.'])
        self.assertEqual(result['invocations'], [('HUB-DOM-CREATIVE', 'design X\nusing A and B.')])
        self.assertIn('Constraints A, B.', result['context'])  # Available context != delegated scope.
        self.assertNotIn('preserve Y', result['invocations'][0][1])

    def test_ordered_three_leaves_and_repeated_leaf(self):
        result = self.spec('/CREATIVE design drainage. # Then /DEBATE challenge that design. # '
                           'After that /BRAINSTORM reverse the fixed-network assumption. #')
        self.assertEqual(result['invocations'], [('HUB-DOM-CREATIVE', 'design drainage.'),
                         ('HUB-CAP-DEBATE', 'challenge that design.'),
                         ('HUB-CAP-BRAINSTORM', 'reverse the fixed-network assumption.')])
        result = self.spec('/CREATIVE mechanism A. # ordinary text /CREATIVE mechanism B. #')
        self.assertEqual(result['invocations'], [('HUB-DOM-CREATIVE', 'mechanism A.'),
                                                ('HUB-DOM-CREATIVE', 'mechanism B.')])
        self.assertIn(' ordinary text ', result['unscoped'])

    def test_semantic_fit_and_old_phrases_never_activate(self):
        for text in ['be creative', 'make this more creative', 'brainstorm this', 'thử động não',
                     'brainstorm sâu', 'động não thử cái này', 'argue against this', 'criticize this',
                     'challenge this proposal', 'compare these options', 'audit this',
                     'reverse assumptions and trace second-order consequences']:
            with self.subTest(text=text):
                self.assertEqual(self.spec(text)['invocations'], [])
        self.assertEqual(simulate(current_fixture(), {'CORE'})['planned'], [])

    def test_unclosed_empty_overlapping_and_recovery(self):
        for text in ['/CREATIVE design X', '/CREATIVE design X.\nNext paragraph.',
                     '/CREATIVE design X /DEBATE attack X #', '/DEBATE #']:
            with self.subTest(text=text):
                result = self.spec(text)
                self.assertEqual(result['invocations'], [])
                self.assertEqual(len(result['blocked']), 1)
        result = self.spec('core work /CREATIVE X /DEBATE Y # independent /BRAINSTORM Z #')
        self.assertEqual(result['invocations'], [('HUB-CAP-BRAINSTORM', 'Z')])
        self.assertEqual(len(result['blocked']), 1)
        self.assertIn('core work ', result['unscoped'])

    def test_exact_tokens_stray_hash_and_turn_non_persistence(self):
        for text in ['#', '#heading', '## section', '/creative X #', '/CREATIVELY X #',
                     '/BRAINSTORMING X #', 'path/DEBATE X #', '/DEBATE,X #']:
            self.assertEqual(self.spec(text)['invocations'], [], text)
        self.assertEqual(len(self.spec('/DEBATE X #')['invocations']), 1)
        self.assertEqual(self.spec('ordinary next turn')['invocations'], [])
        result = self.spec('/CREATIVE use #heading and ## section\nthen finish. # unscoped')
        self.assertEqual(result['invocations'][0][1], 'use #heading and ## section\nthen finish.')

    def test_provenance_and_literal_hash_roles_are_fixture_supplied(self):
        for role in ['ASSISTANT', 'PRIOR_TURN', 'TOOL', 'SOURCE', 'ATTACHMENT', 'QUOTE', 'CODE', 'ANALYZED_PROMPT']:
            self.assertEqual(leaf_span_spec([(role, '/DEBATE X #')])['invocations'], [], role)
        result = leaf_span_spec([('USER_DIRECTIVE', '/CREATIVE use '), ('QUOTE', '"#"'),
                                 ('CODE', ' # /DEBATE literal # '),
                                 ('USER_DIRECTIVE', ' without ending early. # outside')])
        self.assertEqual(result['invocations'], [('HUB-DOM-CREATIVE',
                         'use "#" # /DEBATE literal #  without ending early.')])
        self.assertEqual(result['unscoped'][-1], ' outside')

    @unittest.skip("Historical provenance check: run the original suite in ChatGPT-Creative-Workshops")
    def test_local_ownership_and_no_root_router_parser(self):
        local = load(ROOT / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml')
        selected = {row['activation']: row for row in local['entries'] if 'activation' in row}
        self.assertEqual(set(selected), {'/CREATIVE', '/DEBATE', '/BRAINSTORM'})
        for row in selected.values():
            self.assertEqual(row['requires'], [])
            self.assertIn('SELECT ONLY FOR A VALID EXPLICIT CONTROL SPAN', row['applicability'])
        root = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.10.yaml')
        for token in selected:
            self.assertNotIn(token, str(root))
            self.assertNotIn(token, (ROOT / 'HUB_ROUTER_v1.1.yaml').read_text(encoding='utf-8'))
        previous = subprocess.check_output(['git', 'show', '573c8fe:Central Hub/HUB_ROUTER_v1.1.yaml'], cwd=ROOT)
        self.assertEqual((ROOT / 'HUB_ROUTER_v1.1.yaml').read_bytes(), previous.replace(b'1.7', b'1.10'))

    def test_core_contract_guards_and_scope_dependency_distinction(self):
        text = (ROOT / 'library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md').read_text(encoding='utf-8')
        for clause in ('SEMANTIC FIT != LEAF ACTIVATION', 'No nesting or overlap',
                       'TEXTUAL ORDER != AUTOMATIC DEPENDENCY', 'LEAF SCOPE != CONTEXT VISIBILITY',
                       'PREVIOUS SPAN != CURRENT ACTIVATION', 'PREVIOUS TURN != CURRENT ACTIVATION',
                       'block only the dependent specialized portion', 'not refusal of sufficient core work',
                       'do not execute either leaf', 'Sentence endings, punctuation, newlines',
                       'attachments used as sources', 'No aliases, fuzzy matching or syntax repair'):
            self.assertIn(clause, text)

    def test_debate_reviewed_behavior_not_live_opposition_proof(self):
        text = (ROOT / 'library_modules/HUB-CAP-DEBATE_v1.0.md').read_text(encoding='utf-8')
        for clause in ('strongest objection', 'one consequential objection at a time',
                       'same goal and constraints', 'a burden the alternative carries equally',
                       'unavoidable complexity, added design complexity and relocated complexity',
                       'RESOLVED, NARROWED or OPEN', 'Retire resolved objections',
                       'A narrowed objection remains only within its narrowed scope',
                       'A new objection is a separate issue, not retroactive proof',
                       'If the proposal survives the consequential objections, say so',
                       'Do not invent another attack', 'update it instead of defending the stale reading',
                       'fatal flaw, manageable risk, trade-off and unanswered factual question',
                       'Offering a credible alternative does not activate Brainstorm',
                       'without automatically selecting AIS or performing research'):
            self.assertIn(clause, text)
        self.assertNotRegex(text, r'(?m)^Requires:')

    @unittest.skip("Historical provenance check: run the original suite in ChatGPT-Creative-Workshops")
    def test_successor_archive_and_unchanged_owners(self):
        archive = ROOT / 'Source_archive/Concept explicit leaf controls 2026-11-02'
        replaced = ['HUB_ARCHITECTURE_v1.7.md', 'HUB_PACKAGE_CATALOG_v1.7.yaml',
                    'library_modules/HUB-DOM-CONCEPT-DEVELOPMENT_v1.0.md',
                    'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.0.yaml']
        for name in replaced + ['HUB_ROUTER_v1.1.yaml']:
            previous = subprocess.check_output(['git', 'show', '573c8fe:Central Hub/' + name], cwd=ROOT)
            self.assertEqual((archive / name).read_bytes(), previous)
            if name in replaced:
                self.assertFalse((ROOT / name).exists())
        for name in ['HUB_CI_v1.1.md', 'library_modules/HUB-DOM-CREATIVE_v1.1.md',
                     'library_modules/HUB-CAP-BRAINSTORM_v1.1.md', 'library_modules/HUB-CAP-AUTHORING_v0.6.md']:
            previous = subprocess.check_output(['git', 'show', '573c8fe:Central Hub/' + name], cwd=ROOT)
            # This assertion belongs to the historical Concept 1.1 promotion.
            base = ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05' if name.endswith('HUB-CAP-AUTHORING_v0.6.md') else ROOT
            self.assertEqual((base / name).read_bytes(), previous)
        prior = load(archive / 'HUB_PACKAGE_CATALOG_v1.7.yaml')
        current = load(ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05/HUB_PACKAGE_CATALOG_v1.8.yaml')
        independent = lambda c: [row for row in c['packages'] if row['package_id'] != PACKAGE]
        self.assertEqual(independent(prior), independent(current))
        before = load(archive / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.0.yaml')
        after = load(ROOT / 'library_modules/HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml')
        self.assertEqual(before['anti_drift_configuration'], after['anti_drift_configuration'])
        for old in before['entries']:
            if old['status'] == 'INACTIVE':
                self.assertEqual(old, next(row for row in after['entries'] if row['module_id'] == old['module_id']))


if __name__ == '__main__':
    unittest.main()
