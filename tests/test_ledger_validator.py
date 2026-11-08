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


if __name__ == "__main__":
    unittest.main()