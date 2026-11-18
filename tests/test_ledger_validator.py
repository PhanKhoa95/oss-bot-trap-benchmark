# -*- coding: utf-8 -*-
import unittest

from src.ledger_validator import (
    WORKFLOW_JOB_IDS,
    compute_checkpoint_boundary,
    verify_sequence_gap,
    workflow_job_id,
)

CANONICAL_GAP_CONTRACT = "STRICT_CONTIGUOUS_STEP_1"


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))


class TestWorkflowJobIds(unittest.TestCase):
    def test_contributor_check_job_id(self) -> None:
        self.assertEqual(
            workflow_job_id("require-vouch-and-assignment.yml"),
            "enforce-vouch-and-assignment",
        )

    def test_telemetry_job_id(self) -> None:
        self.assertEqual(
            workflow_job_id("bot-trap-telemetry.yml"),
            "classify-bot-footprint",
        )

    def test_known_workflows(self) -> None:
        self.assertEqual(
            sorted(WORKFLOW_JOB_IDS),
            ["bot-trap-telemetry.yml", "require-vouch-and-assignment.yml"],
        )

    def test_unknown_workflow_raises(self) -> None:
        with self.assertRaises(KeyError):
            workflow_job_id("unknown-workflow.yml")


if __name__ == "__main__":
    unittest.main()
