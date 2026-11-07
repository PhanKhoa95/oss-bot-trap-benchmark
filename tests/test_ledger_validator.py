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

    def test_missing_seq_key(self) -> None:
        # Test single header missing 'seq'
        with self.assertRaises(KeyError) as cm:
            verify_sequence_gap([{"height": 1}])
        self.assertEqual(str(cm.exception), "missing seq key in header")
        
        # Test middle header missing 'seq'
        with self.assertRaises(KeyError) as cm:
            verify_sequence_gap([{"seq": 1}, {"height": 2}, {"seq": 3}])
        self.assertEqual(str(cm.exception), "missing seq key in header")
        
        # Test multiple headers missing 'seq'
        with self.assertRaises(KeyError) as cm:
            verify_sequence_gap([{"seq": 1}, {"height": 2}])
        self.assertEqual(str(cm.exception), "missing seq key in header")


if __name__ == "__main__":
    unittest.main()
