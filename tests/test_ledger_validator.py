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

    def test_legacy_sequence_key_forbidden(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            verify_sequence_gap([{"sequence": 10}, {"seq": 11}])
        self.assertIn("deprecated key 'sequence' is forbidden", str(ctx.exception))

    def test_deprecated_sequence_key(self) -> None:
        with self.assertRaises(ValueError):
            verify_sequence_gap([{"sequence": 10}, {"seq": 11}])


if __name__ == "__main__":
    unittest.main()
