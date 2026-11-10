from __future__ import annotations

MAX_SLIPPAGE_BPS = 500
MAX_LEVERAGE = 20


def compute_amm_swap_out(amount_in: int, reserve_in: int, reserve_out: int, fee_bps: int = 30, slippage_bps: int = 50) -> int:
    if isinstance(amount_in, bool) or not isinstance(amount_in, int) or amount_in <= 0:
        raise ValueError("amount_in must be a positive int (wei/lamports)")
    if isinstance(slippage_bps, bool) or not isinstance(slippage_bps, int) or not (0 <= slippage_bps <= MAX_SLIPPAGE_BPS):
        raise ValueError("slippage_bps must be an int between 0 and MAX_SLIPPAGE_BPS")
    if fee_bps < 0 or fee_bps >= 10000:
        raise ValueError("fee_bps out of range")
    raw_out = (amount_in * reserve_out) // (reserve_in + amount_in)
    fee = (raw_out * fee_bps) // 10000
    after_fee = raw_out - fee
    slippage = (after_fee * slippage_bps) // 10000
    return after_fee - slippage


def evaluate_bar_signal_and_leverage(candles: list[dict[str, int]], index: int, notional: int, margin_equity: int) -> tuple[int, int]:
    if index <= 0 or index >= len(candles):
        raise ValueError("causal index must satisfy 0 < index < len(candles)")
    if margin_equity <= 0:
        raise ValueError("margin_equity must be > 0")
    leverage = notional // margin_equity
    if leverage > MAX_LEVERAGE:
        raise ValueError("leverage exceeds MAX_LEVERAGE")
    delta = int(candles[index]["close"]) - int(candles[index - 1]["close"])
    return (1 if delta > 0 else (-1 if delta < 0 else 0)), leverage
