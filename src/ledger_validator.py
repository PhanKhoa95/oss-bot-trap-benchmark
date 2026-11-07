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
    for idx in range(1, len(headers)):
        prev_header = headers[idx - 1]
        curr_header = headers[idx]
        if "seq" not in prev_header:
            raise KeyError("missing seq key in header")
        if "seq" not in curr_header:
            raise KeyError("missing seq key in header")
        prev_seq = int(prev_header["seq"])
        curr_seq = int(curr_header["seq"])
        if curr_seq != prev_seq + 1:
            return False
    return True
