"""Bounded, local M2 promotion edits; no API calls or Git mutation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HUB = ROOT / 'legacy/upstream/Central Hub'
OUT = Path(__file__).resolve().parent
ARCHIVE = HUB / 'Source_archive/Authoring 0.7 M2 2026-11-05'


def write(path, text):
    path.write_text(text, encoding='utf-8', newline='\n')


def edit(path, old, new):
    text = path.read_text(encoding='utf-8')
    assert old in text, (path, old)
    write(path, text.replace(old, new))


def run():
    for identity in ('I1', 'I3'):
        assert json.loads((OUT / f'candidate_{identity}.json').read_text(encoding='utf-8'))['result'] == 'PASS'
    assert not ARCHIVE.exists()
    ARCHIVE.mkdir()
    receipt = {}
    predecessors = ['library_modules/HUB-CAP-AUTHORING_v0.6.md',
                    'HUB_PACKAGE_CATALOG_v1.8.yaml', 'HUB_ARCHITECTURE_v1.8.md',
                    'HUB_ROUTER_v1.1.yaml', 'AUTHORING_PROMOTION.md']
    for relative in predecessors:
        source = HUB / relative
        target = ARCHIVE / relative
        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_bytes(source.read_bytes())
        receipt[relative] = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256(target.read_bytes()).hexdigest() == receipt[relative]
    write(ARCHIVE / 'ARCHIVE_RECEIPT.json', json.dumps(receipt, indent=2) + '\n')

    candidate = HUB / 'candidates/authoring_v0_7'
    text = (candidate / 'HUB-CAP-AUTHORING_v0.7-candidate.md').read_text(encoding='utf-8')
    text = text.replace('# Prompt Authoring — v0.7 candidate', '# Prompt Authoring — v0.7')
    text = text.replace('Status: CANDIDATE', 'Status: ACTIVE').replace('Version: 0.7-candidate', 'Version: 0.7')
    start = text.index('Candidate root singleton')
    end = text.index('\n\nFor the current turn only,', start)
    text = text[:start] + (
        'Active root singleton with the same direct entrypoint, no local catalog or new relations. '
        'Architecture/Catalog 1.9 retain the existing package/runtime role and Router ownership. '
        'Repository promotion does not establish ChatGPT Library installation, production binding '
        'verification or Project deployment; local runtime bindings are verified separately.'
    ) + text[end:]
    module = HUB / 'library_modules/HUB-CAP-AUTHORING_v0.7.md'
    write(module, text)
    runtime = ROOT / 'runtime/packages/authoring/HUB-CAP-AUTHORING_v0.7.md'
    runtime.write_bytes(module.read_bytes())

    # Start from active metadata, retaining every unrelated package byte-for-byte.
    catalog = (HUB / 'HUB_PACKAGE_CATALOG_v1.8.yaml').read_text(encoding='utf-8')
    catalog = catalog.replace("version: '1.8'", "version: '1.9'", 1)
    first, authoring = catalog.split('- package_id: HUB-PKG-AUTHORING\n', 1)
    authoring, rest = authoring.split('- package_id: HUB-PKG-AIS\n', 1)
    authoring = authoring.replace("version: '0.6'", "version: '0.7'").replace('ACTIVE 0.6 object', 'ACTIVE 0.7 object')
    delta = (candidate / 'HUB_PACKAGE_CATALOG_v1.9-candidate.yaml').read_text(encoding='utf-8').split(
        '    Also admit exactly `/AUTHOR <OUTPUT_TARGET> ISOLATED`', 1)[1].split('  location:', 1)[0]
    authoring = authoring.replace('  location:', '    Also admit exactly `/AUTHOR <OUTPUT_TARGET> ISOLATED`' + delta + '  location:', 1)
    write(HUB / 'HUB_PACKAGE_CATALOG_v1.9.yaml', first + '- package_id: HUB-PKG-AUTHORING\n' + authoring + '- package_id: HUB-PKG-AIS\n' + rest)

    architecture = (HUB / 'HUB_ARCHITECTURE_v1.8.md').read_text(encoding='utf-8')
    architecture = architecture.replace('1.8', '1.9').replace('Authoring 0.6', 'Authoring 0.7').replace(
        'Authoring ACTIVE/0.6', 'Authoring ACTIVE/0.7').replace('CAPABILITY/0.6', 'CAPABILITY/0.7')
    architecture = architecture.replace('Authoring 0.7 optional strategies and bounded composition remain unchanged;',
        'Authoring 0.7 adds exact per-turn ISOLATED source admission owned by Authoring; '
        'without ISOLATED, 0.6 behavior is unchanged. Optional strategies and bounded composition remain unchanged;')
    write(HUB / 'HUB_ARCHITECTURE_v1.9.md', architecture)
    edit(HUB / 'HUB_ROUTER_v1.1.yaml', '1.8', '1.9')
    edit(ROOT / 'app.py', 'HUB_ARCHITECTURE_v1.8.md', 'HUB_ARCHITECTURE_v1.9.md')
    edit(ROOT / 'app.py', 'HUB_PACKAGE_CATALOG_v1.8.yaml', 'HUB_PACKAGE_CATALOG_v1.9.yaml')

    for version in ('0.2', '0.3'):
        path = ROOT / f'runtime/HUB_LOCAL_BINDINGS_v{version}.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        entry = data['packages']['HUB-PKG-AUTHORING']['entrypoint']
        entry.update(version='0.7', path=runtime.relative_to(ROOT).as_posix(),
                     sha256=hashlib.sha256(runtime.read_bytes()).hexdigest())
        write(path, json.dumps(data, indent=2) + '\n')
    edit(ROOT / 't8.py', '("HUB-CAP-AUTHORING", "CAPABILITY", "0.6")', '("HUB-CAP-AUTHORING", "CAPABILITY", "0.7")')
    edit(ROOT / 't8.py', 'HUB-CAP-AUTHORING_v0.6.md', 'HUB-CAP-AUTHORING_v0.7.md')
    data = json.loads((ROOT / 'runtime/HUB_LOCAL_BINDINGS_v0.2.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256(json.dumps(data['packages'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    edit(ROOT / 't9.py', 'ad98963c428fd92f3fabc60bbe67cfa1ca005a0e681a4259f5eb59986582bb3f', digest)
    edit(ROOT / 't9.py', '# Pin exact v0.2 entries, without reading an old manifest on every T9 request.',
         '# Pin the current shared v0.2 package entries, including the M2 Authoring 0.7 promotion.')
    edit(ROOT / 'test_t8.py', 'HUB-CAP-AUTHORING_v0.6.md', 'HUB-CAP-AUTHORING_v0.7.md')
    edit(ROOT / 'test_t9.py', '("HUB-CAP-AUTHORING", "CAPABILITY", "0.6", "")', '("HUB-CAP-AUTHORING", "CAPABILITY", "0.7", "")')
    for filename in ('test_t8.py', 'test_m1.py'):
        edit(ROOT / filename, 'dict(active=True, target=', 'dict(active=True, isolated=False, target=')

    edit(HUB / 'README.md', 'Architecture/Catalog v1.8 và Authoring 0.6 ACTIVE', 'Architecture/Catalog v1.9 và Authoring 0.7 ACTIVE')
    edit(HUB / 'README.md', 'v1.8', 'v1.9')

    # Historical tests retain their original revision scope, using exact predecessor snapshots.
    path = HUB / 'tests/test_authoring_isolation.py'
    edit(path, "ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.6.md'", "ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05/library_modules/HUB-CAP-AUTHORING_v0.6.md'")
    edit(path, "ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml'", "ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05/HUB_PACKAGE_CATALOG_v1.8.yaml'")
    path = HUB / 'tests/test_authoring_m4.py'
    text = path.read_text(encoding='utf-8')
    begin = text.index('class Authoring06PromotionTests')
    a, b = text[:begin], text[begin:]
    b = b.replace('class Authoring06PromotionTests', 'class Authoring06HistoricalPromotionTests')
    b = b.replace("ROOT / 'library_modules/HUB-CAP-AUTHORING_v0.6.md'", "PREDECESSOR / 'library_modules/HUB-CAP-AUTHORING_v0.6.md'")
    b = b.replace("(ROOT / 'library_modules').glob", "(PREDECESSOR / 'library_modules').glob")
    b = b.replace("ROOT.glob('HUB_PACKAGE_CATALOG_v*.yaml')", "PREDECESSOR.glob('HUB_PACKAGE_CATALOG_v*.yaml')")
    b = b.replace("ROOT / 'HUB_PACKAGE_CATALOG_v1.8.yaml'", "PREDECESSOR / 'HUB_PACKAGE_CATALOG_v1.8.yaml'")
    b = b.replace("ROOT / 'HUB_ROUTER_v1.1.yaml'", "PREDECESSOR / 'HUB_ROUTER_v1.1.yaml'")
    b = b.replace("(ROOT / pin['file']).is_file()", "(PREDECESSOR / pin['file']).is_file()")
    write(path, a + "# M2 0.7 supersedes active 0.6; these tests preserve the 0.6 promotion evidence.\nPREDECESSOR = ROOT / 'Source_archive/Authoring 0.7 M2 2026-11-05'\n\n" + b)

    # Archive removal follows byte verification; diagnostic bindings now both use 0.7.
    for relative in predecessors[:3]:
        (HUB / relative).unlink()
    old_runtime = runtime.with_name('HUB-CAP-AUTHORING_v0.6.md')
    target = runtime.parent / 'source_archive' / old_runtime.name
    target.parent.mkdir()
    target.write_bytes(old_runtime.read_bytes())
    assert hashlib.sha256(target.read_bytes()).hexdigest() == receipt['library_modules/HUB-CAP-AUTHORING_v0.6.md']
    old_runtime.unlink()


if __name__ == '__main__':
    run()
