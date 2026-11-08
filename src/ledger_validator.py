def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number."""
    if seq < 1:
        raise ValueError("sequence number must be >= 1")
    # Corrected formula to properly calculate the checkpoint boundary
    return (seq // 64) * 64 + 63

def verify_sequence_gap(headers: list[dict[str, int]]) -> bool:
    """Verify that the sequence numbers in headers are consecutive with no gaps."""
    seqs = [header['seq'] for header in headers]
    for i in range(1, len(seqs)):
        if seqs[i] != seqs[i-1] + 1:
            return False
    return True
