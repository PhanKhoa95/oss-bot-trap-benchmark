# Add a new test case for seq=256
class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)
        self.assertEqual(compute_checkpoint_boundary(256), 319)  # New test case

    # Existing tests remain unchanged
    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))
