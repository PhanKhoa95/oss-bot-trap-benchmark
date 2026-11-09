# -*- coding: utf-8 -*-
import unittest
from src.ledger_validator import compute_checkpoint_boundary, verify_sequence_gap


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)
        self.assertEqual(compute_checkpoint_boundary(256), 319)

    def test_checkpoint_boundary_rejects_bool(self) -> None:
        for value in (True, False):
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as ctx:
                    compute_checkpoint_boundary(value)
                self.assertEqual(str(ctx.exception), "seq must be an exact int")

    def test_checkpoint_boundary_rejects_float(self) -> None:
        for value in (1.0, 1.9, 256.0):
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as ctx:
                    compute_checkpoint_boundary(value)
                self.assertEqual(str(ctx.exception), "seq must be an exact int")

    def test_checkpoint_boundary_type_error_precedes_range_check(self) -> None:
        # bool/float must fail on type before the seq < 1 rule is reached
        self.assertRaises(TypeError, compute_checkpoint_boundary, False)
        self.assertRaises(TypeError, compute_checkpoint_boundary, 0.5)

    def test_checkpoint_boundary_still_rejects_zero_and_negative(self) -> None:
        self.assertRaises(ValueError, compute_checkpoint_boundary, 0)
        self.assertRaises(ValueError, compute_checkpoint_boundary, -1)

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))


if __name__ == "__main__":
    unittest.main()
