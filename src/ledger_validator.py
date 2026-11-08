# -*- coding: utf-8 -*-
"""Ledger checkpoint boundary and sequence continuity validator."""

from __future__ import annotations


def compute_checkpoint_boundary(seq: int, genesis_floor: int = 1) -> int:
    """Return the 64-ledger checkpoint boundary for a sequence number >= genesis_floor."""
    if seq < genesis_floor:
        raise ValueError(f"sequence number must be >= {genesis_floor}")
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
