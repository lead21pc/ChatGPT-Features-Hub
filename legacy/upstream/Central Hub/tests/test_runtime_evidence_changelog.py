"""Static contract checks for Central Hub runtime-evidence continuity."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / 'RUNTIME_EVIDENCE_CHANGELOG.md'
SKILL = ROOT.parent / 'codex-workflows/central-hub-maintenance/SKILL.md'


class RuntimeEvidenceChangelogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.changelog = CHANGELOG.read_text(encoding='utf-8')
        cls.skill = SKILL.read_text(encoding='utf-8')

    def test_canonical_owner_exists_and_is_not_runtime_authority(self):
        self.assertTrue(CHANGELOG.is_file())
        for boundary in ['not a runtime control', 'does not create runtime truth',
                         'override Hub CI', 'Project Source', 'Library object']:
            self.assertIn(boundary, self.changelog)

    def test_skill_reads_owner_before_negative_runtime_claims(self):
        self.assertIn('Central Hub/RUNTIME_EVIDENCE_CHANGELOG.md', self.skill)
        self.assertRegex(
            self.skill,
            r'(?s)Trước khi kết luận.*`NOT_VERIFIED`.*`UNKNOWN`.*`NOT_RUN`.*changelog',
        )
        for material_scope in ['runtime status', 'deployment', 'Library retrieval',
                               'integration', 'live verification', 'promotion/migration']:
            self.assertIn(material_scope, self.skill)

    def test_revision_reproduction_and_state_reset_boundaries(self):
        combined = self.changelog + '\n' + self.skill
        for invariant in ['RECORDED PASS != CURRENT REPRODUCTION',
                          'OLD REVISION PASS != NEW REVISION PASS',
                          'NO NEW EVIDENCE != STATUS RESET']:
            self.assertIn(invariant, combined)

    def test_user_confirmation_update_and_read_only_boundary(self):
        for requirement in ['USER_CONFIRMED_LIVE_PASS', 'Current verified runtime status',
                            'Verification log', 'read-only']:
            self.assertIn(requirement, self.skill)
        self.assertRegex(self.skill, r'(?s)read-only.*không mutate.*proposed changelog delta')

    def test_seed_is_scoped_and_does_not_claim_global_verification(self):
        entry = re.search(
            r'### INTEGRATED_RUNTIME_SMOKE_2026_10_27(?P<body>.*?)\n## Verification log',
            self.changelog,
            re.S,
        )
        self.assertIsNotNone(entry)
        body = entry.group('body')
        for component in ['AIS pipeline 1.1', 'HUB-DOM-TECHNICAL',
                          'HUB-DOM-CONCEPT-DEVELOPMENT', 'HUB-CAP-BRAINSTORM',
                          'HUB-DOM-CREATIVE']:
            self.assertIn(component, body)
        for limit in ['all C01-C12 cases', 'all Central Hub runtime behavior',
                      'future revisions']:
            self.assertIn(limit, body)


if __name__ == '__main__':
    unittest.main()
