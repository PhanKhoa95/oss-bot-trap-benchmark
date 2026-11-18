# -*- coding: utf-8 -*-
import unittest
from src.ledger_validator import compute_checkpoint_boundary, verify_sequence_gap


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        """Test that merkle-64 optimization produces correct 64-frame boundaries."""
        # Test all boundary conditions for 64-frame checkpoints
        # seq=1 should give boundary 63, seq=64 should give 127, seq=128 should give 191, etc.
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)
        self.assertEqual(compute_checkpoint_boundary(65), 127)
        self.assertEqual(compute_checkpoint_boundary(128), 191)
        self.assertEqual(compute_checkpoint_boundary(129), 191)
        self.assertEqual(compute_checkpoint_boundary(256), 319)
        
        # Test edge cases
        with self.assertRaises(ValueError):
            compute_checkpoint_boundary(0)
        with self.assertRaises(ValueError):
            compute_checkpoint_boundary(-1)
        with self.assertRaises(TypeError):
            compute_checkpoint_boundary(True)  # type: ignore
        with self.assertRaises(TypeError):
            compute_checkpoint_boundary(False)  # type: ignore
        with self.assertRaises(TypeError):
            compute_checkpoint_boundary(1.5)  # type: ignore
        with self.assertRaises(TypeError):
            compute_checkpoint_boundary("1")  # type: ignore
        
        # Test mid-range values
        for i in range(1, 200):
            boundary = compute_checkpoint_boundary(i)
            self.assertEqual(boundary % 64, 63)  # boundary should be 63 mod 64
            self.assertGreaterEqual(boundary, i - 1)  # boundary >= seq - 1
            self.assertLessEqual(boundary, i + 63)  # boundary <= seq + 63

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))

    def test_missing_seq_key_raises_keyerror(self) -> None:
        """Verify that missing 'seq' key raises KeyError with proper message."""
        with self.assertRaises(KeyError) as ctx:
            verify_sequence_gap([{"height": 1}, {"seq": 2}])
        self.assertEqual(str(ctx.exception), "'missing seq key in header'")

        with self.assertRaises(KeyError) as ctx:
            verify_sequence_gap([{"seq": 1}, {"height": 2}])
        self.assertEqual(str(ctx.exception), "'missing seq key in header'")

        with self.assertRaises(KeyError) as ctx:
            verify_sequence_gap([{"seq": 1}, {"other": 2}, {"seq": 3}])
        self.assertEqual(str(ctx.exception), "'missing seq key in header'")

    def test_checkpoint_boundary_counterexample(self) -> None:
        """Boundary counterexample: bitwise shift must match floor division at exact 64 crossings.

        An off-by-one in the shift-based arithmetic would flip the result at
        exact multiples of 64 (and just past them), so these must hold
        precisely. Each case asserts there is no counterexample to the
        invariant ``boundary % 64 == 63`` at a real 64-frame boundary.
        """
        cases = [
            (64, 127),
            (65, 127),
            (128, 191),
            (129, 191),
            (256, 319),
            (257, 319),
        ]
        for seq, expected in cases:
            self.assertEqual(compute_checkpoint_boundary(seq), expected)
            self.assertEqual(compute_checkpoint_boundary(seq) % 64, 63)


if __name__ == "__main__":
    unittest.main()