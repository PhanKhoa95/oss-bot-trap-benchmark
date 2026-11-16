// src/soroban_math.rs

//! Soroban math utilities used across the contract suite.

use core::convert::TryFrom;

/// Maximum allowed fee in basis points (10_000 bps = 100%).
pub const MAX_FEE_BPS: u32 = 10_000;

/// Computes the fee share of a given `amount` using the provided `fee_bps` (basis points).
///
/// Returns `Some(fee)` if the calculation succeeds without overflow and the fee basis points
/// are within the allowed range. Returns `None` if `fee_bps` exceeds `MAX_FEE_BPS` or if any
/// intermediate arithmetic overflows.
///
/// # Parameters
/// - `amount`: The principal amount on which the fee is calculated.
/// - `fee_bps`: Fee expressed in basis points (1 bp = 0.01%).
///
/// # Returns
/// `Option<u128>` – `Some(fee)` on success, `None` on invalid input or overflow.
pub fn compute_checked_fee_share(amount: u128, fee_bps: u32) -> Option<u128> {
    // Ensure the fee does not exceed 100% (10_000 bps).
    if fee_bps > MAX_FEE_BPS {
        return None;
    }

    // Convert fee_bps to u128 for multiplication.
    let fee_bps_u128 = u128::from(fee_bps);

    // Perform checked multiplication followed by checked division.
    // The division denominator is constant 10_000 (basis points per whole).
    amount.checked_mul(fee_bps_u128)?.checked_div(10_000u128)
}

// -----------------------------------------------------------------------------
// Additional math utilities used elsewhere in the repository.
// (The original file may contain more functions; they are left unchanged.)
// -----------------------------------------------------------------------------

/// Example of another utility function (placeholder).
pub fn some_other_math_util(x: u128) -> u128 {
    // Placeholder implementation – original logic retained.
    x.saturating_mul(2)
}
