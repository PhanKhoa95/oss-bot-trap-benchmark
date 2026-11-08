# -*- coding: utf-8 -*-
import unittest
from src.ledger_validator import (
    DEFAULT_CHECKPOINT_DIVISOR,
    compute_checkpoint_boundary,
    verify_sequence_gap,
)


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)

    def test_checkpoint_divisor_constant_is_production_value(self) -> None:
        # README advertises a 32 frame preview; the production divisor is 64.
        self.assertEqual(DEFAULT_CHECKPOINT_DIVISOR, 64)

    def test_checkpoint_boundary_matches_literal_formula(self) -> None:
        # Guards the extraction: the constant must not change boundary results.
        for seq in (1, 63, 64, 65, 128, 255, 256, 1000):
            self.assertEqual(
                compute_checkpoint_boundary(seq),
                ((seq + 64) // 64) * 64 - 1,
            )

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))


if __name__ == "__main__":
    unittest.main()
