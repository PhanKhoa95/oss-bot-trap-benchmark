# -*- coding: utf-8 -*-
import unittest
from src.ledger_validator import compute_checkpoint_boundary, verify_sequence_gap


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))

    def test_sequence_gap_semantics_preserved(self) -> None:
        # missing "seq" key defaults to 0, same as .get("seq", 0) before the rewrite
        self.assertTrue(verify_sequence_gap([{}, {"seq": 1}, {"seq": 2}]))
        self.assertFalse(verify_sequence_gap([{"seq": 0}, {}]))
        # int() coercion of str values is kept
        self.assertTrue(verify_sequence_gap([{"seq": "4"}, {"seq": "5"}]))
        # empty / single-header inputs short-circuit to True
        self.assertTrue(verify_sequence_gap([]))
        self.assertTrue(verify_sequence_gap([{"seq": 7}]))
        # duplicates and backwards steps are gaps
        self.assertFalse(verify_sequence_gap([{"seq": 5}, {"seq": 5}]))
        self.assertFalse(verify_sequence_gap([{"seq": 5}, {"seq": 4}]))


if __name__ == "__main__":
    unittest.main()
