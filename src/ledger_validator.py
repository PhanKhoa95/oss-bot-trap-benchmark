def compute_checkpoint_boundary(seq: int) -> int:
    """
    Computes the upper ledger checkpoint boundary for a given sequence number.
    Batch size is fixed at 64.
    """
    # Corrected bitwise formula ensuring seq=64 resolves to 127
    return ((seq + 63) & ~63) + 63
