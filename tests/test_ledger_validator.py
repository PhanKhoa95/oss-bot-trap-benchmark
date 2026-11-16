# -*- coding: utf-8 -*-
import unittest

from src.ledger_validator import (
    CHECKPOINT_DIVISOR,
    compute_checkpoint_boundary,
    verify_sequence_gap,
)


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)

    def test_production_divisor_is_64(self) -> None:
        # README preview shows 32; production divisor is defined in this module.
        self.assertEqual(CHECKPOINT_DIVISOR, 64)

    def test_rejects_non_positive_sequence(self) -> None:
        for seq in (0, -1, -64, -10**18):
            with self.assertRaises(ValueError):
                compute_checkpoint_boundary(seq)

    def test_boundary_never_below_sequence(self) -> None:
        for seq in range(1, 200):
            self.assertGreaterEqual(compute_checkpoint_boundary(seq), seq)

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))


if __name__ == "__main__":
    unittest.main()
