"""Selected-body MCP boundary: deterministic checks, separate from live host proofs."""
import asyncio
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import mcp_server as hub
from test_mcp_root_selection import record


TECH = hub.t9.t8.TECHNICAL


class SelectedPackageTests(unittest.TestCase):
    def test_technical_chunks_exact_and_only_selected_body(self):
        route = record(TECH)
        before = copy.deepcopy(route)
        retrieve = hub.host.t7_retrieve
        chunks, offset = [], 0
        with patch.object(hub.host, 'OpenAI', side_effect=AssertionError('API')), \
             patch.object(hub.t9.t8, 'call_t8', side_effect=AssertionError('execution')), \
             patch.object(Path, 'write_bytes', side_effect=AssertionError('write')), \
             patch.object(Path, 'write_text', side_effect=AssertionError('write')), \
             patch.object(hub.host, 't7_retrieve', wraps=retrieve) as reads:
            while True:
                result = hub.hub_read_selected_package(route, TECH, offset, 137)
                self.assertEqual(result['offset'], offset)
                self.assertEqual(result['next_offset'], offset + len(result['text']))
                self.assertTrue(result['verified'])
                chunks.append(result['text'])
                if not result['has_more']:
                    break
                offset = result['next_offset']
        expected = Path(result['path']).read_bytes().decode('utf-8')
        self.assertEqual(''.join(chunks), expected)
        self.assertEqual(result['total_length'], len(expected))
        self.assertEqual({c.args[0]['module_id'] for c in reads.call_args_list}, {'HUB-DOM-TECHNICAL'})
        self.assertEqual(route, before)
        self.assertEqual(hub.hub_read_selected_package(route, TECH, len(expected))['text'], '')

    def test_unselected_invalid_identity_blockers_and_corruption_fail_closed(self):
        route = record(TECH)
        bad = [record(), {**route, 'unresolved_blockers': ['missing input']}]
        wrong = copy.deepcopy(route)
        wrong['selected_packages'][0]['version'] = '9.9'
        bad.append(wrong)
        for item in bad:
            with self.subTest(item=item), self.assertRaises(ValueError):
                hub.hub_read_selected_package(item, TECH, 0)
        for pid in ('../config.json', hub.t9.t8.AUTHORING, hub.t9.AIS):
            with self.subTest(pid=pid), self.assertRaises(ValueError):
                hub.hub_read_selected_package(route, pid, 0)
        for pid in (hub.t9.t8.CONCEPT, hub.t9.t8.AUTHORING, hub.t9.AIS):
            with self.subTest(selected_but_unsupported=pid), self.assertRaisesRegex(ValueError, 'bounded MCP proof'):
                hub.hub_read_selected_package(record(pid), pid, 0)
        with patch.object(hub.host, 't7_retrieve', side_effect=ValueError('SHA-256')):
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                hub.hub_read_selected_package(route, TECH, 0)

    def test_current_catalog_revalidated_after_root_receipt(self):
        route = record(TECH)
        receipt = hub.hub_validate_root_selection(route)
        read = hub.host.t7_read
        def changed(path):
            text = read(path)
            return text.replace("version: '1.0'", "version: '9.9'", 1) if path == hub.host.HUB_CATALOG_PATH else text
        with patch.object(hub, 'hub_validate_root_selection', return_value=receipt), \
             patch.object(hub.host, 't7_read', side_effect=changed), \
             patch.object(hub.host, 't7_retrieve', side_effect=AssertionError('stale read')):
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                hub.hub_read_selected_package(route, TECH, 0)

    def test_chunk_limits_and_dispatch(self):
        args = dict(route_record=record(TECH), package_id=TECH, offset=0)
        for delta in ({'offset': -1}, {'offset': True}, {'offset': 999999},
                      {'max_chars': 0}, {'max_chars': 4001}, {'max_chars': True}, {'path': '../config.json'}):
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                asyncio.run(hub.call_tool('hub_read_selected_package', {**args, **delta}))
        with self.assertRaises(ValueError):
            asyncio.run(hub.call_tool('hub_read_selected_package', {}))

    def test_stdio_selected_and_negative(self):
        async def run():
            import sys
            params = StdioServerParameters(command=sys.executable, args=[str(Path(hub.__file__))])
            async with stdio_client(params) as (r, w):
                async with ClientSession(r, w) as session:
                    await session.initialize()
                    for route, error in ((record(TECH), False), (record(), True)):
                        result = await session.call_tool('hub_read_selected_package',
                            dict(route_record=route, package_id=TECH, offset=0))
                        self.assertEqual(result.isError, error)
                        if not error:
                            self.assertEqual(result.structuredContent['module_id'], 'HUB-DOM-TECHNICAL')
        asyncio.run(run())


if __name__ == '__main__':
    unittest.main()
