"""R4 is an AIS coverage/reporting SPEC fixture, not Shopping behavior.

Counts below are simulated records, not recovered historical execution.
No production reporter or new shared metric schema is implemented.
"""
import unittest

from test_hub_contracts import ROOT, load
from test_ais_research_core import completion_oracle, execution_oracle


class AISCoverageAccountingTests(unittest.TestCase):
    def test_R4_results_offers_retailers_and_queries_keep_their_units(self):
        queries = [f'query {i}' for i in range(12)]
        unique = [(f'offer {i}', f'retailer {i % 27}') for i in range(65)]
        inspected = unique + unique[:31]
        observed = {'results_inspected': len(inspected),
                    'unique_offers': len({offer for offer, _ in inspected}),
                    'unique_retailers': len({retailer for _, retailer in inspected}),
                    'queries_issued': len(queries)}
        self.assertEqual(observed, {'results_inspected': 96, 'unique_offers': 65,
                                    'unique_retailers': 27, 'queries_issued': 12})
        self.assertEqual(len(inspected) - observed['unique_offers'], 31)
        self.assertNotEqual(observed['queries_issued'], observed['results_inspected'])
        # Typed tuples keep a query count from satisfying result coverage;
        # approximate-result tolerance remains with the actual locked question.
        coverage = completion_oracle({('results inspected', 96)}, {('queries issued', 12)},
                                     limit_reached=True)
        self.assertFalse(coverage['sufficient'])
        self.assertIn(('results inspected', 96), coverage['unresolved'])

    def test_R4_current_AIS_contract_separates_coverage_and_execution(self):
        router = load(ROOT / 'tool_pipelines/AIS/AIS_ROUTER_v1.2.yaml')
        self.assertIn('achieved coverage against locked needs', router['return_contract'])
        self.assertIn('per-action execution status and evidence basis', router['return_contract'])
        self.assertIn('time/version/conditions', router['search_contract']['question'])
        self.assertIn('research mode/lock, depth and coverage planning', router['ownership']['router'])

    def test_unrecovered_historical_trace_stays_unknown(self):
        self.assertEqual(execution_oracle(retrospective='about 100 searches were performed'), 'UNKNOWN')
        # Supplied claims/citations and the fixture counts do not recover a trace.


if __name__ == '__main__':
    unittest.main()
