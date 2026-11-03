"""Inactive ImageT Library candidate: STATIC and declared SPEC fixtures only, no model/Library calls."""
import copy
import hashlib
from pathlib import Path
import re
import subprocess
import unittest

from test_hub_contracts import ROOT, load, Closed

PACKAGE = 'HUB-PKG-IMAGET'
CANDIDATE = ROOT / 'candidates/imaget_library_v0'
BASELINE = 'f69304225f267b116878ed36eacd2b3cc6424935'
# Concept core/catalog now have an authorized local anti-drift extension; their prior
# behavior is protected by test_concept_anti_drift, not frozen to this ImageT snapshot.
PROTECTED = ["HUB_CI_v1.1.md","HUB_ROUTER_v1.1.yaml","HUB_ARCHITECTURE_v1.3.md","HUB_PACKAGE_CATALOG_v1.3.yaml","tool_pipelines/ImageT/IMAGE_CONTROLLER_v1.2.md","tool_pipelines/ImageT/IMAGE_SOURCE_ROUTER.yaml","tool_pipelines/ImageT/manifest.yaml","tool_pipelines/ImageT/READY_GATE_v1.0.md","tool_pipelines/ImageT/IMAGE_ANTI_PRIOR.md","tool_pipelines/ImageT/config.md","tool_pipelines/ImageT/preferences/HUMANOID_CHARACTER_DESIGN_PREFERENCE.md","tool_pipelines/ImageT/tests/ROUTE_TEST_CASES.md","tool_pipelines/ImageT/tests/READY_GATE_TEST_CASES.md","library_modules/HUB-DOM-CREATIVE_v1.1.md","library_modules/HUB-CAP-BRAINSTORM_v1.1.md","library_modules/HUB-CAP-AUTHORING_v0.3.md"]
MANIFEST = 'HUB-IMAGET-MANIFEST_v2.3.0-candidate.yaml'
CATALOG = 'HUB-CATALOG-IMAGET_v0.1-candidate.yaml'
EXPECTED = [["HUB-PIPE-IMAGET","1.3-candidate","TOOL_PIPELINE","md"],["HUB-IMAGET-CONTROLLER","1.3-candidate","DOMAIN_PROCEDURE","md"],["HUB-IMAGET-ROUTER","3.2.0-candidate","DOMAIN_PROCEDURE","yaml"],["HUB-IMAGET-MANIFEST","2.3.0-candidate","PIPELINE_MANIFEST","yaml"],["HUB-IMAGET-READY-GATE","1.1-candidate","DOMAIN_PROCEDURE","md"],["HUB-IMAGET-ANTI-PRIOR","1.2.0-candidate","DOMAIN_PROCEDURE","md"],["HUB-IMAGET-ANTI-DRIFT","2.1.0-candidate","DOMAIN_PROCEDURE","md"],["HUB-CATALOG-IMAGET","0.1-candidate","PACKAGE_CATALOG","yaml"],["HUB-IMAGET-HUMANOID-CONSTRUCTION","0.1-candidate","DOMAIN_PROCEDURE","md"],["HUB-IMAGET-HUMANOID-DESIGN-PREFERENCE","0.2-candidate","PREFERENCE","md"]]
CONSTRUCTION = 'HUB-IMAGET-HUMANOID-CONSTRUCTION'
PREFERENCE = 'HUB-IMAGET-HUMANOID-DESIGN-PREFERENCE'


def artifact(module_id):
    row = next(row for row in EXPECTED if row[0] == module_id)
    return CANDIDATE / f'{row[0]}_v{row[1]}.{row[3]}'


def read_identity(path):
    if path.suffix == '.yaml':
        return load(path)
    text = path.read_text(encoding='utf-8')
    names = {'module_id': 'Module ID', 'package_id': 'Package ID',
             'runtime_role': 'Runtime role', 'status': 'Status', 'version': 'Version'}
    result = {}
    for key, name in names.items():
        values = re.findall(r'^' + re.escape(name) + r': (.+)$', text, re.M)
        if len(values) != 1:
            raise Closed('missing/duplicate header')
        result[key] = values[0]
    return result


def verify_core(manifest):
    """Resolve candidate bytes/closure only in this explicit STATIC test view."""
    rows = manifest['core']
    inventory = {row['module_id']: row for row in rows}
    if len(rows) != len(inventory):
        raise Closed('duplicate core identity')
    visited, visiting = set(), set()

    def visit(identity):
        if identity in visiting or identity not in inventory:
            raise Closed('cycle or missing core')
        if identity in visited:
            return
        visiting.add(identity)
        row = inventory[identity]
        path = CANDIDATE / row['file']
        if not path.resolve().is_relative_to(CANDIDATE.resolve()):
            raise Closed('scope escape')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise Closed('missing/corrupt core')
        actual = read_identity(path)
        for key in ['module_id', 'package_id', 'runtime_role', 'status', 'version']:
            if actual[key] != row[key]:
                raise Closed('identity mismatch')
        for dependency in row['requires']:
            visit(dependency)
        visiting.remove(identity)
        visited.add(identity)
    for identity in inventory:
        visit(identity)
    return visited


def selection_spec(catalog, *, humanoid, authority, fields=(), delegated=(),
                   preference_fields=(), need=False, payload=''):
    """Fixture-supplied intent/authority; does not recognize language or run leaf prose."""
    if authority not in {'RAW', 'PRESERVED_AUTHORED'}:
        raise Closed('unknown authority')
    allowed = set(fields)
    constructible = allowed if authority == 'RAW' else allowed.intersection(delegated)
    preferred = allowed.intersection(preference_fields)
    selected = {}
    for row in catalog['entries']:
        # Explicit test admission only. Inactive candidates are not normal runtime eligible.
        if row['status'] != 'CANDIDATE' or row['package_id'] != PACKAGE:
            raise Closed('candidate metadata mismatch')
        if not humanoid:
            continue
        if row['runtime_role'] == 'DOMAIN_PROCEDURE' and need and constructible:
            selected[row['module_id']] = constructible
        if row['runtime_role'] == 'PREFERENCE' and preferred:
            selected[row['module_id']] = preferred
    return {'selected': selected, 'payload': payload, 'new_field_authority': set()}


class ImageTLibraryCandidateTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load(CANDIDATE / MANIFEST)
        self.catalog = load(CANDIDATE / CATALOG)

    def test_identity_structure_and_inactive_core_closure(self):
        expected_files = {f'{i}_v{v}.{ext}' for i, v, role, ext in EXPECTED}
        self.assertEqual({p.name for p in CANDIDATE.iterdir()}, expected_files)
        for identity, version, role, ext in EXPECTED:
            with self.subTest(module=identity):
                path = artifact(identity)
                actual = read_identity(path)
                for key, expected in [('module_id', identity), ('package_id', PACKAGE),
                                      ('runtime_role', role), ('status', 'CANDIDATE'), ('version', version)]:
                    self.assertEqual(actual[key], expected)
                data = path.read_bytes()
                self.assertFalse(data.startswith(b'\xef\xbb\xbf'))
                text = data.decode('utf-8')
                self.assertNotIn('\r', text)
                self.assertTrue(text.endswith('\n'))
                self.assertNotRegex(text, r'(?m)[ \t]+$')
                if ext == 'yaml':
                    self.assertFalse(actual['active'])
                else:
                    self.assertIn('Activation: INACTIVE; explicit static candidate tests only', text)
        self.assertEqual(len(verify_core(self.manifest)), 5)
        self.assertEqual({e['module_id'] for e in self.catalog['entries']}, {CONSTRUCTION, PREFERENCE})
        self.assertNotIn('entries', self.manifest)
        self.assertNotIn('preferences', self.manifest)
        self.assertEqual(self.manifest['runtime_role'], 'PIPELINE_MANIFEST')
        self.assertEqual(self.catalog['runtime_role'], 'PACKAGE_CATALOG')
        for row in self.catalog['entries']:
            self.assertEqual(row['requires'], [])
            self.assertFalse(row['active'])
            self.assertEqual(row['location']['class'], 'LIBRARY')
            self.assertEqual(row['location']['root'], 'Central Hub Config')
            self.assertEqual(row['location']['candidate_artifact'], artifact(row['module_id']).name)
            actual = read_identity(artifact(row['module_id']))
            self.assertEqual(actual['version'], row['version'])
            self.assertEqual(actual['runtime_role'], row['runtime_role'])
        pref = next(row for row in self.catalog['entries'] if row['module_id'] == PREFERENCE)
        self.assertEqual(pref['activation'], 'inactive')
        bad = copy.deepcopy(self.manifest)
        bad['core'][0]['requires'].append(bad['core'][0]['module_id'])
        with self.assertRaises(Closed):
            verify_core(bad)
        bad = copy.deepcopy(self.manifest)
        bad['core'][0]['sha256'] = '0' * 64
        with self.assertRaises(Closed):
            verify_core(bad)

    def test_active_sources_byte_exact_and_existing_gate_bodies_preserved(self):
        for name in PROTECTED:
            with self.subTest(active=name):
                original = subprocess.check_output(['git', 'show', BASELINE + ':Central Hub/' + name], cwd=ROOT)
                path = ROOT / name
                if name in {'HUB_ROUTER_v1.1.yaml', 'HUB_ARCHITECTURE_v1.3.md', 'HUB_PACKAGE_CATALOG_v1.3.yaml', 'library_modules/HUB-CAP-AUTHORING_v0.3.md'}:
                    path = ROOT / 'Source_archive/Authoring 0.4 promotion 2026-11-01' / name
                self.assertEqual(path.read_bytes(), original)
        root = load(ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml')
        binding = next(p for p in root['packages'] if p['package_id'] == PACKAGE)
        self.assertEqual(binding['binding_mode'], 'LEGACY_PROJECT_SOURCE')
        self.assertEqual(binding['version'], '1.2')
        for identity, source, marker in [
                ('HUB-IMAGET-ANTI-PRIOR', 'IMAGE_ANTI_PRIOR.md', '## Function'),
                ('HUB-IMAGET-ANTI-DRIFT', 'config.md', '## Authority and scope')]:
            active = (ROOT / 'tool_pipelines/ImageT' / source).read_text(encoding='utf-8')
            candidate = artifact(identity).read_text(encoding='utf-8')
            self.assertEqual(active.split(marker, 1)[1], candidate.split(marker, 1)[1])
        ready = artifact('HUB-IMAGET-READY-GATE').read_text(encoding='utf-8')
        active = (ROOT / 'tool_pipelines/ImageT/READY_GATE_v1.0.md').read_text(encoding='utf-8')
        marker = '## Preserved approval protocol'
        self.assertEqual(ready.split(marker, 1)[1], active.split(marker, 1)[1])
        entry = artifact('HUB-PIPE-IMAGET').read_text(encoding='utf-8')
        self.assertNotIn('## PRESERVED_AUTHORED path', entry)
        self.assertNotIn('## Relational primitives', entry)
        controller = artifact('HUB-IMAGET-CONTROLLER').read_text(encoding='utf-8')
        self.assertLess(controller.index('## Input authority / Open Gate'),
                        controller.index('## Authority-bounded local work'))
        self.assertIn('CONSTRUCTION SELECTED != FIELD OPENED',
                      artifact(CONSTRUCTION).read_text(encoding='utf-8'))

    def test_C01_raw_humanoid(self):
        result = selection_spec(self.catalog, humanoid=True, authority='RAW', need=True,
                                fields={'layer_relationship'})
        self.assertEqual(result['selected'], {CONSTRUCTION: {'layer_relationship'}})
        self.assertEqual(result['new_field_authority'], set())
        for missing in ['material', 'count', 'pose']:
            self.assertNotIn(missing, result['selected'][CONSTRUCTION])

    def test_C02_preserved_without_open_fields(self):
        payload = 'ACCEPTED: layered coat. OPEN: material. REJECTED: trim. no text.'
        result = selection_spec(self.catalog, humanoid=True, authority='PRESERVED_AUTHORED',
                                need=True, payload=payload)
        self.assertEqual(result['selected'], {})
        self.assertEqual(result['payload'], payload)

    def test_C03_preserved_exact_delegation_and_separate_preference(self):
        payload = 'Keep identity and palette. Clarify only existing layer overlap.'
        result = selection_spec(self.catalog, humanoid=True, authority='PRESERVED_AUTHORED',
                                need=True, fields={'layer_overlap', 'identity'}, delegated={'layer_overlap'},
                                payload=payload)
        self.assertEqual(result['selected'], {CONSTRUCTION: {'layer_overlap'}})
        self.assertEqual(result['payload'], payload)
        preferred = selection_spec(self.catalog, humanoid=True, authority='PRESERVED_AUTHORED',
                                   fields={'layer_overlap'}, preference_fields={'layer_overlap', 'pose'})
        self.assertEqual(preferred['selected'], {PREFERENCE: {'layer_overlap'}})
        self.assertEqual(preferred['new_field_authority'], set())

    def test_C04_nonhumanoid(self):
        result = selection_spec(self.catalog, humanoid=False, authority='RAW', need=True,
                                fields={'composition'}, preference_fields={'composition'})
        self.assertEqual(result['selected'], {})

    def test_C05_growth_preserves_interface_and_core_structure(self):
        root_interface = {'entrypoint_module_id': 'HUB-PIPE-IMAGET',
                          'local_catalog': {'module_id': 'HUB-CATALOG-IMAGET',
                                            'package_id': PACKAGE, 'runtime_role': 'PACKAGE_CATALOG',
                                            'format_version': '1'}}
        before = copy.deepcopy(root_interface), copy.deepcopy(self.manifest)
        expanded = copy.deepcopy(self.catalog)
        expanded['version'] = '0.2-candidate'
        expanded['entries'].append({
            'module_id': 'TEST-ONLY-SYNTHETIC-LEAF', 'package_id': PACKAGE,
            'runtime_role': 'DOMAIN_PROCEDURE', 'status': 'CANDIDATE'})
        self.assertEqual(len(expanded['entries']), 3)
        self.assertEqual((root_interface, self.manifest), before)
        self.assertNotIn('TEST-ONLY-SYNTHETIC-LEAF', str(root_interface) + str(self.manifest))
        self.assertFalse((CANDIDATE / 'TEST-ONLY-SYNTHETIC-LEAF.md').exists())
        # This proves structural growth only; exact Catalog deployment version binding must refresh.
        self.assertNotEqual(expanded['version'], self.catalog['version'])


if __name__ == '__main__':
    unittest.main()
