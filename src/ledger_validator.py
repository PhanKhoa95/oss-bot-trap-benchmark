def verify_sequence_gap(headers: list[dict[str, int]]) -> bool:
    """Verify that ledger headers have strictly contiguous sequence numbers.

    Example usage:
    >>> verify_sequence_gap([{'seq': 10}, {'seq': 11}, {'seq': 12}])
    True
    >>> verify_sequence_gap([{'seq': 10}, {'seq': 12}])
    False

    """
    if len(headers) <= 1:
        return True
    for idx in range(1, len(headers)):
        prev_seq = int(headers[idx - 1].get("seq", 0))
        curr_seq = int(headers[idx].get("seq", 0))
        if curr_seq != prev_seq + 1:
            return False
    return True