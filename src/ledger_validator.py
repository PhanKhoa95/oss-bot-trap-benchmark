# -*- coding: utf-8 -*-
"""Ledger checkpoint boundary and sequence continuity validator."""

from __future__ import annotations

# Workflow job IDs that must stay aligned with the GitHub Actions check names.
# These are descriptive constants only: no job is renamed, so existing
# check-name alignment for branch protection is preserved.
WORKFLOW_JOB_IDS: dict[str, str] = {
    "require-vouch-and-assignment.yml": "enforce-vouch-and-assignment",
    "bot-trap-telemetry.yml": "classify-bot-footprint",
}


def workflow_job_id(workflow_file: str) -> str:
    """Return the expected job ID for a known contributor-check workflow file."""
    try:
        return WORKFLOW_JOB_IDS[workflow_file]
    except KeyError:
        raise KeyError(f"unknown contributor-check workflow: {workflow_file}") from None


def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number."""
    if seq < 1:
        raise ValueError("sequence number must be >= 1")
    return ((seq + 64) // 64) * 64 - 1


def verify_sequence_gap(headers: list[dict[str, int]]) -> bool:
    """Verify that ledger headers have strictly contiguous sequence numbers."""
    if len(headers) <= 1:
        return True
    for idx in range(1, len(headers)):
        prev_seq = int(headers[idx - 1].get("seq", 0))
        curr_seq = int(headers[idx].get("seq", 0))
        if curr_seq != prev_seq + 1:
            return False
    return True
