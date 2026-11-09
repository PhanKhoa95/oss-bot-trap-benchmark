# -*- coding: utf-8 -*-
"""Ledger checkpoint boundary and sequence continuity validator."""

from __future__ import annotations


def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number.

    Only exact ``int`` values are accepted. ``bool`` (a subclass of ``int``)
    and ``float`` are rejected with ``TypeError`` before the range check, so
    ``True`` never silently behaves like ``1`` and ``1.0`` never passes.
    """
    if isinstance(seq, bool) or not isinstance(seq, int):
        raise TypeError("seq must be an exact int")
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
