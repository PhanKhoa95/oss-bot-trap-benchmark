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

    def test_empty_and_single_header_batch(self) -> None:
        # Regression guard for issue #15: empty header batches must not raise.
        self.assertTrue(verify_sequence_gap([]))
        self.assertTrue(verify_sequence_gap([{"seq": 1}]))
        self.assertTrue(verify_sequence_gap([{}]))


if __name__ == "__main__":
    unittest.main()
