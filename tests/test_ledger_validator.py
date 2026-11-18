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

    def test_sequence_continuity_with_step_size(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 15}, {"seq": 20}], step_size=5))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 15}, {"seq": 19}], step_size=5))
        self.assertTrue(verify_sequence_gap([{"seq": 0}, {"seq": 10}], step_size=10))
        self.assertTrue(verify_sequence_gap([{"seq": 1}], step_size=3))
        self.assertTrue(verify_sequence_gap([], step_size=2))
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}], step_size=1))


if __name__ == "__main__":
    unittest.main()
