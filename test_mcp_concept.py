"""C4 static Concept boundary; host owns semantics and live verification."""
import asyncio
import copy
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import mcp_server as hub
from test_mcp_root_selection import record

CONCEPT = hub.t9.t8.CONCEPT
BRAINSTORM = 'HUB-CAP-BRAINSTORM'
CREATIVE = 'HUB-DOM-CREATIVE'


def leaves(*modules, blockers=()):
    return dict(selected_leaves=[dict(module_id=mid,
        runtime_role='DOMAIN_CONTROL' if mid == CREATIVE else 'CAPABILITY',
        application_scope='Fixture scope', reason='Host fixture decision') for mid in modules],
        unresolved_blockers=list(blockers))


class ConceptBoundaryTests(unittest.TestCase):
    def reconstruct(self, read):
        parts, offset, identity = [], 0, None
        while True:
            result = read(offset)
            current = {k: result[k] for k in ('module_id', 'runtime_role', 'version', 'path', 'sha256', 'total_length')}
            if identity is None:
                identity = current
            self.assertEqual(current, identity)
            self.assertTrue(result['verified'])
            self.assertEqual(result['offset'], offset)
            self.assertEqual(result['next_offset'], offset + len(result['text']))
            self.assertLessEqual(len(result['text']), 4000)
            parts.append(result['text'])
            if not result['has_more']:
                break
            offset = result['next_offset']
        expected = Path(result['path']).read_bytes()
        self.assertEqual(''.join(parts).encode('utf-8'), expected)
        self.assertEqual(result['sha256'], hashlib.sha256(expected).hexdigest())
        self.assertEqual(result['total_length'], len(expected.decode('utf-8')))
        self.assertEqual(read(result['total_length'])['text'], '')
        return result

    def test_exact_interface_and_host_contract_no_execution_or_write(self):
        route = record(CONCEPT)
        before = copy.deepcopy(route)
        retrieve = hub.host.t7_retrieve
        with patch.object(hub.host, 'OpenAI', side_effect=AssertionError('API')), \
             patch.object(hub.t9.t8, 'call_t8', side_effect=AssertionError('T8')), \
             patch.object(hub.t9, 'call_t9', side_effect=AssertionError('T9')), \
             patch.object(Path, 'write_bytes', side_effect=AssertionError('write')), \
             patch.object(Path, 'write_text', side_effect=AssertionError('write')), \
             patch.object(hub.host, 't7_retrieve', wraps=retrieve) as reads:
            for component, mid in (('entrypoint', 'HUB-DOM-CONCEPT-DEVELOPMENT'),
                                   ('local_catalog', 'HUB-CATALOG-CONCEPT-DEVELOPMENT')):
                result = self.reconstruct(lambda offset: hub.hub_read_selected_concept_interface(route, component, offset, 997))
                self.assertEqual(result['module_id'], mid)
                self.assertEqual(result['result_schema'], hub.host.LEAF_SCHEMA)
                self.assertIn('exact core and Catalog semantics', result['semantic_task'])
            self.assertTrue(hub.hub_validate_concept_selection(route, leaves())['record_valid'])
            self.assertTrue(hub.hub_validate_concept_selection(route, leaves(BRAINSTORM, CREATIVE))['record_valid'])
            self.assertEqual({c.args[0]['module_id'] for c in reads.call_args_list},
                             {'HUB-DOM-CONCEPT-DEVELOPMENT', 'HUB-CATALOG-CONCEPT-DEVELOPMENT'})
            self.reconstruct(lambda offset: hub.hub_read_selected_concept_leaf(route, leaves(BRAINSTORM), BRAINSTORM, offset))
        self.assertEqual(route, before)

    def test_empty_valid_selection_blockers_preserved_and_no_leaf_body(self):
        route, selection = record(CONCEPT), leaves(BRAINSTORM, blockers=['missing premise'])
        before = copy.deepcopy(selection)
        result = hub.hub_validate_concept_selection(route, selection)
        self.assertEqual(result['leaf_record'], before)
        self.assertEqual(result['unresolved_blockers'], ['missing premise'])
        result['leaf_record']['unresolved_blockers'].clear()
        self.assertEqual(selection, before)
        with self.assertRaisesRegex(ValueError, 'blocked'):
            hub.hub_read_selected_concept_leaf(route, selection, BRAINSTORM, 0)
        self.assertEqual(hub.hub_validate_concept_selection(route, leaves())['selected_module_ids'], [])

    def test_root_gate_and_local_catalog_identity_fail_closed(self):
        route = record(CONCEPT)
        wrong = copy.deepcopy(route)
        wrong['selected_packages'][0]['version'] = '9.9'
        for bad in (record(), record(hub.t9.t8.TECHNICAL), wrong,
                    {**route, 'unresolved_blockers': ['blocked']}):
            for call in (lambda: hub.hub_read_selected_concept_interface(bad, 'entrypoint', 0),
                         lambda: hub.hub_validate_concept_selection(bad, leaves()),
                         lambda: hub.hub_read_selected_concept_leaf(bad, leaves(BRAINSTORM), BRAINSTORM, 0)):
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    call()
        read = hub.host.t7_read
        def mismatch(path):
            text = read(path)
            if path == hub.host.HUB_CATALOG_PATH:
                return text.replace('    module_id: HUB-CATALOG-CONCEPT-DEVELOPMENT', '    module_id: HUB-CATALOG-WRONG')
            return text
        with patch.object(hub.host, 't7_read', side_effect=mismatch):
            with self.assertRaisesRegex(ValueError, 'interface identity mismatch'):
                hub.hub_read_selected_concept_interface(route, 'local_catalog', 0)

    def test_invalid_records_rejected_before_leaf_reads(self):
        valid = leaves(BRAINSTORM)
        bad = [None, [], {}, {**valid, 'extra': ''}, {**valid, 'selected_leaves': {}},
               {**valid, 'unresolved_blockers': [None]}, {**valid, 'unresolved_blockers': ''},
               leaves(BRAINSTORM, BRAINSTORM), leaves('UNKNOWN'), leaves('../config.json'),
               leaves('HUB-DOM-ANTI-PRIOR')]
        for field in hub.host.LEAF_FIELDS:
            item = copy.deepcopy(valid)
            item['selected_leaves'][0][field] = 1
            bad.append(item)
            item = copy.deepcopy(valid)
            del item['selected_leaves'][0][field]
            bad.append(item)
        for delta in ({'runtime_role': 'DOMAIN_CONTROL'}, {'version': '1.1'}, {'path': '../config.json'}):
            item = copy.deepcopy(valid)
            item['selected_leaves'][0].update(delta)
            bad.append(item)
        retrieve = hub.host.t7_retrieve
        def no_leaf(binding):
            self.assertNotIn(binding['module_id'], {BRAINSTORM, CREATIVE, 'HUB-CAP-DEBATE'})
            return retrieve(binding)
        with patch.object(hub.host, 't7_retrieve', side_effect=no_leaf):
            for selection in bad:
                with self.subTest(selection=selection), self.assertRaises(ValueError):
                    hub.hub_validate_concept_selection(record(CONCEPT), selection)

    def test_current_leaf_catalog_status_role_version_and_binding_revalidated(self):
        route, selection = record(CONCEPT), leaves(BRAINSTORM)
        hub.hub_validate_concept_selection(route, selection)
        retrieve = hub.host.t7_retrieve
        for old, new in (("  version: '1.1'", "  version: '9.9'"),
                         ('  status: ACTIVE', '  status: INACTIVE'),
                         ('  runtime_role: CAPABILITY', '  runtime_role: DOMAIN_CONTROL')):
            def changed(binding):
                self.assertNotEqual(binding['module_id'], BRAINSTORM, 'leaf body read before validation')
                text = retrieve(binding)
                if binding['module_id'] == 'HUB-CATALOG-CONCEPT-DEVELOPMENT':
                    prefix, rest = text.split('- module_id: ' + BRAINSTORM, 1)
                    return prefix + '- module_id: ' + BRAINSTORM + rest.replace(old, new, 1)
                return text
            with self.subTest(field=old), patch.object(hub.host, 't7_retrieve', side_effect=changed):
                with self.assertRaises(ValueError):
                    hub.hub_validate_concept_selection(route, selection)
                with self.assertRaises(ValueError):
                    hub.hub_read_selected_concept_leaf(route, selection, BRAINSTORM, 0)

    def test_selected_leaf_exact_and_unselected_arbitrary_reads_rejected(self):
        route, selection = record(CONCEPT), leaves(BRAINSTORM)
        retrieve = hub.host.t7_retrieve
        with patch.object(hub.host, 't7_retrieve', wraps=retrieve) as reads:
            self.reconstruct(lambda offset: hub.hub_read_selected_concept_leaf(route, selection, BRAINSTORM, offset, 719))
            self.assertEqual({c.args[0]['module_id'] for c in reads.call_args_list},
                             {'HUB-DOM-CONCEPT-DEVELOPMENT', 'HUB-CATALOG-CONCEPT-DEVELOPMENT', BRAINSTORM})
        self.reconstruct(lambda offset: hub.hub_read_selected_concept_leaf(route, leaves(CREATIVE), CREATIVE, offset))
        for mid in (CREATIVE, 'HUB-CAP-DEBATE', '../config.json', 'HUB-DOM-CONCEPT-DEVELOPMENT', '', None):
            with self.subTest(mid=mid), self.assertRaises(ValueError):
                hub.hub_read_selected_concept_leaf(route, selection, mid, 0)

    def test_sha_corruption_fails_closed(self):
        read_bytes = Path.read_bytes
        for filename, call in (
            ('HUB-DOM-CONCEPT-DEVELOPMENT_v1.1.md', lambda: hub.hub_read_selected_concept_interface(record(CONCEPT), 'entrypoint', 0)),
            ('HUB-CATALOG-CONCEPT-DEVELOPMENT_v1.1.yaml', lambda: hub.hub_validate_concept_selection(record(CONCEPT), leaves())),
            ('HUB-CAP-BRAINSTORM_v1.1.md', lambda: hub.hub_read_selected_concept_leaf(record(CONCEPT), leaves(BRAINSTORM), BRAINSTORM, 0))):
            def corrupt(path):
                data = read_bytes(path)
                return data + b'corrupt' if path.name == filename else data
            with self.subTest(filename=filename), patch.object(Path, 'read_bytes', corrupt):
                with self.assertRaisesRegex(ValueError, 'SHA-256'):
                    call()

    def test_chunk_limits_component_allowlist_and_dispatch(self):
        for name, args in (
            ('hub_read_selected_concept_interface', dict(route_record=record(CONCEPT), component='entrypoint', offset=0)),
            ('hub_read_selected_concept_leaf', dict(route_record=record(CONCEPT), leaf_record=leaves(BRAINSTORM), module_id=BRAINSTORM, offset=0))):
            for delta in ({'offset': -1}, {'offset': True}, {'offset': 999999}, {'max_chars': 0},
                          {'max_chars': 4001}, {'max_chars': True}, {'path': '../config.json'}):
                with self.subTest(name=name, delta=delta), self.assertRaises(ValueError):
                    asyncio.run(hub.call_tool(name, {**args, **delta}))
        for component in ('../config.json', 'leaves', BRAINSTORM, None):
            with self.assertRaises(ValueError):
                hub.hub_read_selected_concept_interface(record(CONCEPT), component, 0)
        for name in ('hub_read_selected_concept_interface', 'hub_validate_concept_selection', 'hub_read_selected_concept_leaf'):
            with self.assertRaises(ValueError):
                asyncio.run(hub.call_tool(name, {}))
        with self.assertRaises(ValueError):
            asyncio.run(hub.call_tool('hub_validate_concept_selection', dict(route_record=record(CONCEPT), leaf_record=leaves(), extra=True)))

    def test_stdio_concept_interface_validation_leaf_and_negative_calls(self):
        async def run():
            params = StdioServerParameters(command=sys.executable, args=[str(Path(hub.__file__))])
            async with stdio_client(params) as (r, w):
                async with ClientSession(r, w) as session:
                    await session.initialize()
                    route = record(CONCEPT)
                    for component in hub.CONCEPT_COMPONENTS:
                        result = await session.call_tool('hub_read_selected_concept_interface', dict(route_record=route, component=component, offset=0))
                        self.assertFalse(result.isError)
                        self.assertTrue(result.structuredContent['verified'])
                    for selection in (leaves(), leaves(BRAINSTORM), leaves(CREATIVE)):
                        result = await session.call_tool('hub_validate_concept_selection', dict(route_record=route, leaf_record=selection))
                        self.assertFalse(result.isError)
                        self.assertEqual(result.structuredContent['leaf_record'], selection)
                    result = await session.call_tool('hub_read_selected_concept_leaf', dict(route_record=route, leaf_record=leaves(BRAINSTORM), module_id=BRAINSTORM, offset=0))
                    self.assertFalse(result.isError)
                    self.assertEqual(result.structuredContent['module_id'], BRAINSTORM)
                    for name, args in (
                        ('hub_read_selected_concept_interface', dict(route_record=record(), component='entrypoint', offset=0)),
                        ('hub_read_selected_concept_interface', dict(route_record=route, component='../config.json', offset=0)),
                        ('hub_validate_concept_selection', dict(route_record=route, leaf_record=leaves(BRAINSTORM, BRAINSTORM))),
                        ('hub_validate_concept_selection', dict(route_record=route, leaf_record=leaves('UNKNOWN'))),
                        ('hub_read_selected_concept_leaf', dict(route_record=route, leaf_record=leaves(), module_id=BRAINSTORM, offset=0))):
                        result = await session.call_tool(name, args)
                        self.assertTrue(result.isError)
        asyncio.run(run())


if __name__ == '__main__':
    unittest.main()
