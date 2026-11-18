//! Soroban Instance Storage TTL Extension Guard

pub const MAX_INSTANCE_TTL_LEDGERS: u32 = 3_110_400;

pub fn extend_instance_ttl_window(
    current_ledger: u32,
    live_until_ledger: u32,
    threshold: u32,
    extend_to: u32,
    max_ttl: u32,
) -> Option<u32> {
    if threshold == 0 || threshold > extend_to || extend_to > max_ttl || max_ttl > MAX_INSTANCE_TTL_LEDGERS {
        return None;
    }
    let remaining = live_until_ledger.saturating_sub(current_ledger);
    if remaining > threshold {
        return Some(live_until_ledger);
    }
    let target = current_ledger.checked_add(extend_to)?;
    let ceiling = current_ledger.checked_add(max_ttl)?;
    Some(target.min(ceiling).max(live_until_ledger))
}
