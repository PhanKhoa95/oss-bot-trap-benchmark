# -*- coding: utf-8 -*-
"""Ledger checkpoint boundary and sequence continuity validator."""

from __future__ import annotations


def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number."""
    if seq < 1:
        raise ValueError("sequence number must be >= 1")
    return ((seq + 64) // 64) * 64 - 1


def verify_sequence_gap(headers: list[dict[str, int]]) -> bool:
    """Verify that ledger headers have strictly contiguous sequence numbers."""
    if len(headers) <= 1:
        return True
    prev_seq = int(headers[0].get("seq", 0))
    for header in headers[1:]:
        curr_seq = int(header.get("seq", 0))
        if curr_seq != prev_seq + 1:
            return False
        prev_seq = curr_seq
    return True
