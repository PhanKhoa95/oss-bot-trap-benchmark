# Existing code remains unchanged except for the return statement in compute_checkpoint_boundary
def compute_checkpoint_boundary(seq: int) -> int:
    """Return the 64-ledger checkpoint boundary for a positive sequence number."""
    if seq < 1:
        raise ValueError("sequence number must be >= 1")
    # Corrected formula to properly calculate the checkpoint boundary
    return ((seq + 63) // 64) * 64 - 1
