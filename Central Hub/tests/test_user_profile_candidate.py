"""STATIC / SPEC ONLY.

These tests do not prove live model behavior, Library retrieval, platform
privacy, section-level object resolution, actual object non-read, Hub routing,
runtime access enforcement or future Health behavior.
"""
import copy
import subprocess
import unittest

from test_hub_contracts import ROOT, load


CANDIDATE = ROOT / 'candidates/user_profile_v0'
SCHEMA = 'HUB-USER-PROFILE-SCHEMA_v0.1-candidate.yaml'
TEMPLATE = 'HUB-USER-PROFILE-TEMPLATE_v0.1-candidate.yaml'
DESIGN = 'USER_PROFILE_DESIGN.md'
SHOPPING = 'HUB-PKG-SHOPPING'
HEALTH = 'HUB-PKG-HEALTH'
BASELINE = 'c5f81196ca4a8354908d7161f530e23073120e22'
CATALOG = 'HUB_PACKAGE_CATALOG_v1.10.yaml'


def read_plan(schema, *, selected_package, section, purpose, material_need):
    """Evaluate declared premises before a synthetic object could be supplied."""
    if not selected_package or not material_need:
        return 'SKIP', ()
    purposes = schema['access'].get(selected_package, {}).get(section, ())
    if purpose not in purposes:
        return schema['default_access'], ()
    return 'ALLOW', (section,)


def brand_input(*, stored, explicit):
    """Project declared input roles for this turn without persisting anything."""
    if explicit is not None:
        return explicit, 'CURRENT_USER_INPUT'
    if stored is not None:
        return stored, 'PREFERENCE'
    return None, 'UNKNOWN'


class UserProfileCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load(CANDIDATE / SCHEMA)
        cls.template = load(CANDIDATE / TEMPLATE)
        cls.design = (CANDIDATE / DESIGN).read_text(encoding='utf-8')
        cls.root = load(ROOT / CATALOG)

    def test_U01_candidate_identity_and_no_registration(self):
        self.assertEqual({path.name for path in CANDIDATE.iterdir()}, {SCHEMA, TEMPLATE, DESIGN})
        for key, value in {
            'resource_id': 'HUB-USER-PROFILE', 'schema_version': '0.1-candidate',
            'status': 'CANDIDATE', 'resource_kind': 'SHARED_NON_MODULE_RESOURCE',
            'input_mode': 'SUPPLIED_INPUT_SPEC_ONLY', 'library_resolution': 'NOT_IMPLEMENTED',
        }.items():
            self.assertEqual(self.schema[key], value)
        self.assertNotIn('runtime_role', self.schema)
        self.assertNotIn('package_id', self.schema)
        self.assertNotIn('HUB-USER-PROFILE', str(self.root))
        self.assertNotIn('HUB-PKG-USER-CONTEXT', str(self.root))

    def test_U02_customizable_is_manual(self):
        self.assertIs(self.schema['customizable'], True)
        self.assertEqual(self.schema['owner'], 'USER')
        self.assertEqual(self.schema['customization_mode'], 'MANUAL_USER_ONLY')
        self.assertIn('CUSTOMIZABLE != MODEL-MUTABLE', self.design)

    def test_U03_all_model_mutation_forbidden(self):
        mutation = self.schema['mutation']
        self.assertIs(mutation['model_allowed'], False)
        self.assertEqual(set(mutation['forbidden_model_actions']), {
            'write', 'append', 'delete', 'infer_and_store', 'normalize_and_save',
            'persist_chat_to_profile', 'refresh_stale_values',
        })
        self.assertEqual(mutation['proposed_change'], 'RETURN_TO_USER_WITHOUT_WRITING')
        self.assertIn('PROFILE MUTATION BY MODEL: NEVER', self.design)

    def test_U04_repository_write_authority_does_not_extend_to_profile(self):
        repository_write_authorized = True
        mutation = self.schema['mutation']
        inherited_authority = repository_write_authorized and mutation['general_file_write_authorization_applies']
        self.assertIs(mutation['model_allowed'] or inherited_authority, False)

    def test_U05_public_template_exact_empty_data(self):
        self.assertEqual(self.template, {'object_templates': [
            dict(resource_id='HUB-USER-PROFILE', schema_version='0.1-candidate', section_id='BASICS',
                 data={'general': {'market_region': None, 'measurement_system': None},
                       'preferences': {'preferred_brand': None}}),
            dict(resource_id='HUB-USER-PROFILE', schema_version='0.1-candidate',
                 section_id='HEALTH_CONSTRAINTS', data={'substances_to_avoid': []}),
        ]})
        self.assertEqual(self.schema['storage']['actual_values'], 'PRIVATE_USER_MANAGED_OUTSIDE_REPOSITORY')

    def test_U06_sections_are_separate_objects(self):
        self.assertEqual(set(self.schema['sections']), {'BASICS', 'HEALTH_CONSTRAINTS'})
        self.assertEqual([obj['section_id'] for obj in self.template['object_templates']],
                         ['BASICS', 'HEALTH_CONSTRAINTS'])
        self.assertEqual(read_plan(self.schema, selected_package=SHOPPING, section='BASICS',
                                   purpose='product_compatibility', material_need=True), ('ALLOW', ('BASICS',)))

    def test_U07_price_only_never_requests_health_constraints(self):
        for section, expected in [('BASICS', ('ALLOW', ('BASICS',))), ('HEALTH_CONSTRAINTS', ('DENY', ()))]:
            self.assertEqual(read_plan(self.schema, selected_package=SHOPPING, section=section,
                                       purpose='purchase_filtering', material_need=True), expected)

    def test_U08_compatibility_requests_only_needed_section(self):
        self.assertEqual(read_plan(self.schema, selected_package=SHOPPING, section='HEALTH_CONSTRAINTS',
                                   purpose='product_compatibility', material_need=True),
                         ('ALLOW', ('HEALTH_CONSTRAINTS',)))

    def test_U09_access_without_need_or_selection_skips_read(self):
        for package, need in [(SHOPPING, False), (None, True)]:
            self.assertEqual(read_plan(self.schema, selected_package=package, section='HEALTH_CONSTRAINTS',
                                       purpose='product_compatibility', material_need=need), ('SKIP', ()))

    def test_U10_undeclared_package_denied(self):
        self.assertEqual(self.schema['default_access'], 'DENY')
        self.assertEqual(read_plan(self.schema, selected_package='SYNTHETIC-NO-ACCESS',
                                   section='HEALTH_CONSTRAINTS', purpose='product_compatibility',
                                   material_need=True), ('DENY', ()))

    def test_U11_brand_preference_is_not_hard(self):
        self.assertEqual(brand_input(stored='SYNTHETIC_BRAND_X', explicit=None),
                         ('SYNTHETIC_BRAND_X', 'PREFERENCE'))
        self.assertIn('PROFILE PREFERENCE != HARD CONSTRAINT', self.design)

    def test_U12_current_input_wins_without_editing_stored_values(self):
        stored = {'preferred_brand': 'SYNTHETIC_BRAND_X'}
        before = copy.deepcopy(stored)
        explicit = 'avoid SYNTHETIC_BRAND_X'
        self.assertEqual(brand_input(stored=stored['preferred_brand'], explicit=explicit),
                         (explicit, 'CURRENT_USER_INPUT'))
        self.assertEqual(stored, before)

    def test_U13_model_inference_is_not_profile_data(self):
        fixture = {'stored': None, 'explicit': None, 'model_inference': 'SYNTHETIC_BRAND_X'}
        self.assertEqual(brand_input(stored=fixture['stored'], explicit=fixture['explicit']), (None, 'UNKNOWN'))
        self.assertIsNone(fixture['stored'])
        self.assertIn('MODEL INFERENCE != PROFILE FACT', self.design)

    def test_U14_missing_profile_leaves_only_dependent_work_unresolved(self):
        _, requested = read_plan(self.schema, selected_package=SHOPPING, section='HEALTH_CONSTRAINTS',
                                 purpose='product_compatibility', material_need=True)
        supplied_sections = set()
        work = {'ordinary_comparison': set(), 'personalized_compatibility': set(requested)}
        unresolved = {part for part, needs in work.items() if needs - supplied_sections}
        self.assertEqual(unresolved, {'personalized_compatibility'})

    def test_U15_future_only_health_fixture_preserves_user_ownership(self):
        future = copy.deepcopy(self.schema)
        future['access'][HEALTH] = {'BASICS': ['health_context']}
        self.assertEqual(read_plan(future, selected_package=HEALTH, section='BASICS',
                                   purpose='health_context', material_need=True), ('ALLOW', ('BASICS',)))
        self.assertEqual((future['resource_id'], future['owner']), ('HUB-USER-PROFILE', 'USER'))
        self.assertEqual(set(self.schema['access']), {SHOPPING})
        self.assertNotIn(HEALTH, str(self.root))

    @unittest.skip("Historical provenance check: run the original suite in ChatGPT-Creative-Workshops")
    def test_U16_candidate_leaves_active_stack_unchanged(self):
        protected = [
            'HUB_CI_v1.1.md', 'HUB_ROUTER_v1.1.yaml', 'HUB_ARCHITECTURE_v1.10.md', CATALOG,
            'library_modules', 'tool_pipelines/AIS', 'tool_pipelines/ImageT',
        ]
        changed = subprocess.check_output(
            ['git', '-c', 'core.longpaths=true', 'diff', '--name-only', BASELINE, '--', *protected], cwd=ROOT,
        )
        untracked = subprocess.check_output(
            ['git', 'ls-files', '--others', '--exclude-standard', '--', *protected], cwd=ROOT,
        )
        self.assertEqual(changed + untracked, b'')
