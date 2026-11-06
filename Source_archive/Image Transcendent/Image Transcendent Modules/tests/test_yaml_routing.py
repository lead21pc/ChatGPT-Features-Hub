"""Static package checks and a test-only routing simulation; no ChatGPT/tool calls.

Run: python -B -m unittest discover -s tests -v
Requires PyYAML (tested with 6.0.3); no runtime router is installed by this file.
"""
import copy
import hashlib
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT.parent / 'Image Transcendent CI'

# Fixed pre-migration evidence: CI sections from Authority onward; modules with
# only the approved compatibility-header substitution. Independent of Git HEAD.
PRESERVED_SHA256 = {'ImageT_v1.0.0.md': '356322bc844caedc7ca769b7b4fd6a16191e99ac7f0497abf70237fa8ca4d79e', 'ImageT_v1.0.0-ready-gate-candidate.md': '697784e6db99dff8aaf7d51521c1334df3beb62b1fd5fa3993158124f1853b8c', 'IMAGE_ANTI_PRIOR.md': 'f08a1d1a09c8b31cd3fe6ed80b38b19f2c662e15f7e192b42c8a5e044aa69b5c', 'config.md': '20b08b3b99b237eebeec0442024e0818245d0b0bebc2fb756e972aca67d4d3d7', 'HUMANOID_CHARACTER_DESIGN_PREFERENCE.md': '3652c341c3f3c5c4caefeca107643b40c58c4ff721c4aa26a3be49095fb7a16e'}


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
            raise Closed('anchor or alias')
    for token in yaml.scan(text):
        if isinstance(token, yaml.ScalarToken) and token.plain:
            value = token.value
            if value.lower() in {'yes', 'no', 'on', 'off', 'true', 'false', 'null', '~'}:
                if value not in {'true', 'false', 'null'}:
                    raise Closed('nonconservative boolean/null')
            if re.match(r'^\d{4}-\d{2}-\d{2}', value):
                raise Closed('implicit date')
    return yaml.load(text, Loader=StrictLoader)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_path(entry):
    if entry['file'] is None:
        raise Closed('source absent')
    path = (ROOT / entry['local_path']).resolve()
    if path.parent not in {ROOT, CI} or path.name != entry['file']:
        raise Closed('nonexact source or archive')
    return path


def verify_source(entry):
    path = source_path(entry)
    if not path.is_file() or digest(path) != entry['sha256']:
        raise Closed('missing source or hash mismatch')
    if path.suffix == '.md':
        body = path.read_text(encoding='utf-8')
        versions = re.findall(r'^(?:IMAGE_T|ANTI_PRIOR|CONFIG|PREFERENCE)_VERSION: (.+)$', body, re.M)
        if versions != [entry['version']] or f"STATUS: {entry['status'].upper()}" not in body:
            raise Closed('header mismatch')
    return path


def simulate(manifest, router, selection=None, isolated=False, session=None, installed=None,
             ended=False, operation='create', unexpected_template=False):
    """Independent acceptance oracle for declared routing contract, NOT model execution."""
    if router['manifest_contract']['format_version'] != manifest['format_version']:
        raise Closed('manifest/router contract mismatch')
    router_entry = manifest['artifacts']['router']
    if router_entry['version'] != router['router_version'] or router_entry['status'] != 'active':
        raise Closed('router inventory mismatch')
    verify_source(router_entry)
    if operation not in router['operations']:
        raise Closed('unknown operation')
    selected = manifest['ci']['active']
    if selected['status'] != 'active':
        raise Closed('invalid baseline')
    if ended:
        selection = None
    if selection is not None and selection != selected['id']:
        matches = [entry for entry in manifest['ci']['candidates'] if entry['id'] == selection]
        if len(matches) != 1:
            raise Closed('unknown or duplicate candidate')
        selected = matches[0]
        if selected['status'] != 'candidate' or selected['selectable'] is not True:
            raise Closed('candidate not selectable')
        if selected['selection_scope'] != 'isolated_test' or not isolated or not session:
            raise Closed('invalid test scope')
    if installed != selected['id']:
        raise Closed('installed CI mismatch; restore or explicitly select matching instructions')
    verify_source(selected)
    for role, version in selected['compatibility'].items():
        if manifest['artifacts'][role]['version'] != version:
            raise Closed('selected CI incompatible')
    for role in ['prior_guard', 'anti_drift']:
        entry = manifest['artifacts'][role]
        if entry['status'] != 'active' or entry['required'] is not True:
            raise Closed('invalid required module')
        verify_source(entry)
    template = manifest['artifacts']['visual_template']
    if template['status'] == 'optional_absent':
        if template['required'] or template['file'] is not None or unexpected_template:
            raise Closed('inconsistent optional absence')
        loaded_template = False
    elif template['status'] == 'active':
        verify_source(template)
        loaded_template = True
    else:
        raise Closed('unknown template state')
    # Ready Gate stays in CI. This oracle can inspect its text; it cannot run ChatGPT.
    body = source_path(selected).read_text(encoding='utf-8')
    pending = '## Ready gate' in body and operation != 'analyze'
    return {'selected': selected['id'], 'template_loaded': loaded_template,
            'next_stage': 'prompt_preparation', 'after_valid_prompt': 'pending_approval' if pending else 'selected_ci_contract',
            'approval_granted': False, 'tool_called': False}


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.manifest = parse((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
        self.router = parse((ROOT / 'IMAGE_SOURCE_ROUTER.yaml').read_text(encoding='utf-8'))

    def route(self, **kwargs):
        return simulate(self.manifest, self.router, installed=kwargs.pop('installed', 'baseline'), **kwargs)

    def test_01_default_baseline(self):
        self.assertEqual(self.route()['selected'], 'baseline')

    def test_02_explicit_candidate(self):
        result = self.route(selection='ready-gate', isolated=True, session='trial-1', installed='ready-gate')
        self.assertEqual(result['selected'], 'ready-gate')
        self.assertEqual(result['next_stage'], 'prompt_preparation')

    def test_03_available_does_not_activate(self):
        self.assertTrue(self.manifest['ci']['candidates'][0]['selectable'])
        self.assertEqual(self.route()['selected'], 'baseline')
        self.assertEqual(self.manifest['preferences'][0]['activation'], 'inactive')

    def test_04_absent_or_unselectable_candidate(self):
        with self.assertRaises(Closed): self.route(selection='unknown')
        self.manifest['ci']['candidates'][0]['selectable'] = False
        with self.assertRaises(Closed):
            self.route(selection='ready-gate', isolated=True, session='trial-1', installed='ready-gate')

    def test_05_manifest_router_mismatch(self):
        self.router['manifest_contract']['format_version'] = 'unsupported'
        with self.assertRaises(Closed): self.route()
        self.router['manifest_contract']['format_version'] = '1'
        self.manifest['artifacts']['router']['version'] = 'unsupported'
        with self.assertRaises(Closed): self.route()

    def test_06_missing_required_source(self):
        for role in ['prior_guard', 'anti_drift']:
            original = copy.deepcopy(self.manifest['artifacts'][role])
            self.manifest['artifacts'][role]['file'] = 'missing.md'
            self.manifest['artifacts'][role]['local_path'] = 'missing.md'
            with self.assertRaises(Closed): self.route()
            self.manifest['artifacts'][role] = original

    def test_07_optional_template_absent(self):
        self.assertFalse(self.route()['template_loaded'])
        with self.assertRaises(Closed): self.route(unexpected_template=True)

    def test_08_archive_same_name_rejected(self):
        self.manifest['artifacts']['prior_guard']['local_path'] = 'source_archive/IMAGE_ANTI_PRIOR.md'
        with self.assertRaises(Closed): self.route()

    def test_09_test_expiry_no_promotion(self):
        original = copy.deepcopy(self.manifest)
        self.route(selection='ready-gate', isolated=True, session='trial-1', installed='ready-gate')
        with self.assertRaises(Closed):
            self.route(selection='ready-gate', ended=True, installed='ready-gate')
        self.assertEqual(self.route(selection='ready-gate', ended=True)['selected'], 'baseline')
        self.assertEqual(self.manifest, original)

    def test_10_candidate_reaches_ready_gate_without_generation(self):
        result = self.route(selection='ready-gate', isolated=True, session='trial-1', installed='ready-gate')
        self.assertEqual(result['after_valid_prompt'], 'pending_approval')
        self.assertFalse(result['approval_granted'])
        self.assertFalse(result['tool_called'])

    def test_candidate_scope_and_installed_ci(self):
        for kwargs in [{}, {'isolated': True}, {'session': 'trial-1'},
                       {'isolated': True, 'session': 'trial-1', 'installed': 'baseline'}]:
            with self.assertRaises(Closed): self.route(selection='ready-gate', **kwargs)

    def test_analyze_never_enters_ready_gate(self):
        result = self.route(selection='ready-gate', isolated=True, session='trial-1', installed='ready-gate', operation='analyze')
        self.assertEqual(result['after_valid_prompt'], 'selected_ci_contract')
        self.assertFalse(result['tool_called'])

    def test_yaml_subset_rejects_ambiguity(self):
        for text in ['a: 1\na: 2', 'a: &x 1\nb: *x', 'a: yes', 'a: FALSE',
                     'a: ~', 'a: 2026-10-12', '<<: {}']:
            with self.assertRaises((Closed, yaml.YAMLError)): parse(text)

    def test_inventory_hashes_and_unique_ids(self):
        entries = [self.manifest['ci']['active'], *self.manifest['ci']['candidates'],
                   *self.manifest['artifacts'].values(), *self.manifest['preferences']]
        ids = [entry['id'] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in entries:
            if entry['file'] is not None: verify_source(entry)
            self.assertTrue(entry['status'].islower())
            if entry['version'] is not None: self.assertIsInstance(entry['version'], str)
        self.assertTrue(self.manifest['release']['published'])
        self.assertEqual(self.manifest['release']['publication_scope'], 'repository_sources')
        self.assertEqual(self.manifest['release']['project_deployment'], 'not_tested')
        self.assertIsNone(self.manifest['integrity']['self_hash'])

    def test_compatibility_and_corruption_fail_closed(self):
        self.manifest['ci']['active']['compatibility']['prior_guard'] = 'wrong'
        with self.assertRaises(Closed): self.route()
        self.manifest['ci']['active']['compatibility']['prior_guard'] = '1.1.0'
        self.manifest['artifacts']['prior_guard']['sha256'] = '0' * 64
        with self.assertRaises(Closed): self.route()

    def test_semantic_preservation_and_ci_size(self):
        for entry in [self.manifest['ci']['active'], *self.manifest['ci']['candidates']]:
            path = source_path(entry)
            self.assertLessEqual(len(path.read_bytes().decode('utf-8')), 8000)
            marker = b'## Authority and conflict'
            self.assertEqual(hashlib.sha256(path.read_bytes().split(marker, 1)[1]).hexdigest(), PRESERVED_SHA256[path.name])
        for name in ['IMAGE_ANTI_PRIOR.md', 'config.md']:
            self.assertEqual(digest(ROOT / name), PRESERVED_SHA256[name])
        name = 'HUMANOID_CHARACTER_DESIGN_PREFERENCE.md'
        self.assertEqual(digest(ROOT / name), PRESERVED_SHA256[name])

    def test_no_release_inventory_in_router(self):
        text = (ROOT / 'IMAGE_SOURCE_ROUTER.yaml').read_text(encoding='utf-8')
        for entry in [self.manifest['ci']['active'], *self.manifest['ci']['candidates']]:
            self.assertNotIn(entry['file'], text)
            self.assertNotIn(entry['sha256'], text)
        self.assertFalse(self.router['selection']['persist_as_active'])
        self.assertFalse(self.router['selection']['mutate_manifest'])

    def test_archive_provenance_and_retired_sources(self):
        self.assertEqual([p for p in ROOT.rglob('*') if p.is_dir() and p.name.lower() == 'source_archive'],
                         [ROOT / 'source_archive'])
        for entry in self.manifest['archives']:
            path = (ROOT / entry['file']).resolve()
            self.assertIn('source_archive', path.parts)
            self.assertEqual(digest(path), entry['sha256'])
            self.assertEqual(entry['status'], 'archived')
        for name in ['manifest.md', 'IMAGE_SOURCE_ROUTER.md']:
            self.assertFalse((ROOT / name).exists())
            expected = {'manifest.md': '609bc18cec5ec1868732b50e9bddf169c4ecb56df1c36d2f8d6c7b4ff9e5dbc2',
                        'IMAGE_SOURCE_ROUTER.md': 'de3daf811c5b14e03ea24dc101655aa0d177153a29c6c6c7c768ee76b6732227'}
            self.assertEqual(digest(ROOT / 'source_archive' / name), expected[name])

    def test_missing_active_template_and_selection_source(self):
        template = self.manifest['artifacts']['visual_template']
        template.update(status='active', file='template.md', local_path='template.md', version='test', sha256='0' * 64)
        with self.assertRaises(Closed): self.route()
        template.update(status='optional_absent', file=None, local_path=None)
        self.manifest['ci']['candidates'][0].update(file='missing.md', local_path='missing.md')
        with self.assertRaises(Closed):
            self.route(selection='ready-gate', isolated=True, session='trial-1', installed='ready-gate')

    def test_no_active_markdown_control_references(self):
        for path in [*CI.glob('ImageT_*.md'), CI / 'README.md', CI / 'READY_GATE_CANDIDATE_TESTS.md',
                     ROOT / 'IMAGE_ANTI_PRIOR.md', ROOT / 'config.md', ROOT / 'ROUTE_TEST_CASES.md']:
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('manifest.md', text)
            self.assertNotIn('IMAGE_SOURCE_ROUTER.md', text)


if __name__ == '__main__':
    unittest.main()
