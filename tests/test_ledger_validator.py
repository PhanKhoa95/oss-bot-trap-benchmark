# -*- coding: utf-8 -*-
import unittest
from src.ledger_validator import compute_checkpoint_boundary, verify_sequence_gap

CANONICAL_GAP_CONTRACT = "STRICT_CONTIGUOUS_STEP_1"


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary_mandatory_cases(self) -> None:
        """Validate exact mandatory checkpoint boundary test vectors."""
        cases = [
            (1, 63),
            (63, 63),
            (64, 127),
            (65, 127),
            (127, 127),
            (128, 191),
            (129, 191),
        ]
        for seq, expected in cases:
            with self.subTest(seq=seq, expected=expected):
                self.assertEqual(compute_checkpoint_boundary(seq), expected)

    def test_checkpoint_boundary_invalid_inputs(self) -> None:
        """Validate that non-positive sequence numbers raise ValueError."""
        for invalid_seq in [0, -1, -63, -64, -100]:
            with self.subTest(seq=invalid_seq):
                with self.assertRaises(ValueError):
                    compute_checkpoint_boundary(invalid_seq)

    def test_checkpoint_boundary_large_values(self) -> None:
        """Validate boundary calculation for large sequence numbers."""
        large_cases = [
            (1_000_000, ((1_000_000 + 64) // 64) * 64 - 1),
            (2**20, ((2**20 + 64) // 64) * 64 - 1),
            (2**30, ((2**30 + 64) // 64) * 64 - 1),
        ]
        for seq, expected in large_cases:
            with self.subTest(seq=seq):
                self.assertEqual(compute_checkpoint_boundary(seq), expected)

    def test_checkpoint_boundary_block_transitions(self) -> None:
        """Verify continuous alignment across all 64-ledger blocks up to 512."""
        for seq in range(1, 513):
            expected = ((seq + 64) // 64) * 64 - 1
            self.assertEqual(compute_checkpoint_boundary(seq), expected)

    def test_sequence_continuity(self) -> None:
        """Validate sequence continuity verification contract."""
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))
        self.assertTrue(verify_sequence_gap([]))
        self.assertTrue(verify_sequence_gap([{"seq": 1}]))


if __name__ == "__main__":
    unittest.main()
