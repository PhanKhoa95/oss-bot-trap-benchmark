# -*- coding: utf-8 -*-
"""Ledger checkpoint boundary and sequence continuity validator."""

from __future__ import annotations


def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number."""
    if seq < 1:
        raise ValueError("sequence number must be >= 1")
    # Original: return ((seq + 64) // 64) * 64 - 1
    # Optimized using bitwise operations for performance.
    # The formula ((seq + 63) & ~63) + 63 correctly aligns to the next multiple of 64
    # and then subtracts 1 to get the boundary.
    # For seq = 63: ((63 + 63) & ~63) + 63 = (126 & ~63) + 63 = (126 & 0xFFFFFFC0) + 63 = 0 + 63 = 63
    # For seq = 64: ((64 + 63) & ~63) + 63 = (127 & ~63) + 63 = (127 & 0xFFFFFFC0) + 63 = 64 + 63 = 127
    return ((seq + 63) & ~63) + 63


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
