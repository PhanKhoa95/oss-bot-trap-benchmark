import unittest
from src.automation_session_guard import MIN_COOLDOWN_MS, verify_worker_profile_isolation, validate_affiliate_and_cooldown


class TestAutomationSessionGuard(unittest.TestCase):
    def test_sybil_fingerprint_and_proxy_isolation(self) -> None:
        self.assertTrue(verify_worker_profile_isolation([
            {"canvas_seed": 101, "proxy_rotation_ttl": 120},
            {"canvas_seed": 202, "proxy_rotation_ttl": 120},
        ]))
        self.assertFalse(verify_worker_profile_isolation([
            {"canvas_seed": 0xDEADBEEF, "proxy_rotation_ttl": 0},
            {"canvas_seed": 0xDEADBEEF, "proxy_rotation_ttl": 0},
        ]))

    def test_causal_affiliate_and_cooldown(self) -> None:
        self.assertEqual(MIN_COOLDOWN_MS, 250)
        self.assertTrue(validate_affiliate_and_cooldown(1000, 1050, 300))
        self.assertFalse(validate_affiliate_and_cooldown(1100, 1050, 300))
        with self.assertRaises(ValueError):
            validate_affiliate_and_cooldown(1000, 1050, -1)
