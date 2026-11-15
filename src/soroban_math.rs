//! Soroban Checked u128 Fee Arithmetic

pub const BPS_SCALE: u128 = 10_000;

pub fn compute_checked_fee_share(amount: u128, fee_bps: u32) -> Option<u128> {
    if fee_bps > 10_000 {
        return None;
    }
    let scaled = amount.checked_mul(fee_bps as u128)?;
    scaled.checked_div(BPS_SCALE)
}
