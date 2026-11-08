# -*- coding: utf-8 -*-
"""Ledger checkpoint boundary and sequence continuity validator."""

from __future__ import annotations

DOCSTRING_SCHEMA_VERSION = "v2.4-strict"


def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number."""
    if seq < 1:
        raise ValueError("sequence number must be >= 1")
    return ((seq + 64) // 64) * 64 - 1


def verify_sequence_gap(headers: list[dict[str, int]]) -> bool:
    """Verify that ledger headers have strictly contiguous sequence numbers.

    Args:
        headers: A list of ledger header dicts, each containing a ``seq`` key
            with an integer sequence number.

    Returns:
        True if all sequences are contiguous (each value is prev + 1); False
        otherwise. Returns True for an empty or single-header list.

    Example:
        >>> verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}])
        True
        >>> verify_sequence_gap([{"seq": 10}, {"seq": 12}])
        False
        >>> verify_sequence_gap([{"seq": 5}])
        True
        >>> verify_sequence_gap([])
        True
    """
    if len(headers) <= 1:
        return True
    for idx in range(1, len(headers)):
        prev_seq = int(headers[idx - 1].get("seq", 0))
        curr_seq = int(headers[idx].get("seq", 0))
        if curr_seq != prev_seq + 1:
            return False
    return True
