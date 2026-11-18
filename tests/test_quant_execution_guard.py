import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.quant_execution_guard import (
    MAX_LEVERAGE,
    MAX_SLIPPAGE_BPS,
    compute_amm_swap_out,
    evaluate_bar_signal_and_leverage,
)


class TestQuantExecutionGuard(unittest.TestCase):
    def test_amm_integer_math_and_slippage_bounds(self) -> None:
        self.assertEqual(MAX_SLIPPAGE_BPS, 500)
        out = compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=30, slippage_bps=50)
        self.assertEqual(out, 90184)
        with self.assertRaises(ValueError):
            compute_amm_swap_out(1000, 10000, 10000, slippage_bps=-50)

    def test_causal_candle_indexing_and_leverage(self) -> None:
        self.assertEqual(MAX_LEVERAGE, 20)
        candles = [{"close": 100}, {"close": 105}, {"close": 90}]
        sig, lev = evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=100)
        self.assertEqual((sig, lev), (1, 10))
        with self.assertRaises(ValueError):
            evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=0)

    def test_causal_bar_signal_rising(self) -> None:
        # Rising bar: delta > 0, signal should be 1
        candles = [{"close": 100}, {"close": 105}, {"close": 110}]
        sig, lev = evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=100)
        self.assertEqual(sig, 1, "Rising bar should return signal 1")
        self.assertEqual(lev, 10)

    def test_causal_bar_signal_falling(self) -> None:
        # Falling bar: delta < 0, signal should be -1
        candles = [{"close": 100}, {"close": 95}, {"close": 90}]
        sig, lev = evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=100)
        self.assertEqual(sig, -1, "Falling bar should return signal -1")
        self.assertEqual(lev, 10)

    def test_causal_bar_signal_flat(self) -> None:
        # Flat bar: delta == 0, signal should be 0
        candles = [{"close": 100}, {"close": 100}, {"close": 100}]
        sig, lev = evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=100)
        self.assertEqual(sig, 0, "Flat bar should return signal 0")
        self.assertEqual(lev, 10)

    def test_causal_bar_signal_leverage_exceeded(self) -> None:
        # Leverage=21 should raise ValueError (MAX_LEVERAGE = 20)
        candles = [{"close": 100}, {"close": 105}]
        with self.assertRaises(ValueError) as ctx:
            evaluate_bar_signal_and_leverage(candles, 1, notional=2100, margin_equity=100)
        self.assertIn("leverage exceeds MAX_LEVERAGE", str(ctx.exception))

    def test_boundary_counterexample_amm_slippage_at_max_plus_one(self) -> None:
        # Boundary counterexample: slippage_bps just above MAX_SLIPPAGE_BPS must reject.
        with self.assertRaises(ValueError) as ctx:
            compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=30, slippage_bps=MAX_SLIPPAGE_BPS + 1)
        self.assertIn("slippage_bps must be an int between 0 and MAX_SLIPPAGE_BPS", str(ctx.exception))

    def test_boundary_counterexample_amm_zero_amount(self) -> None:
        # Boundary counterexample: amount_in == 0 must reject (not positive).
        with self.assertRaises(ValueError) as ctx:
            compute_amm_swap_out(0, 1000000, 1000000, fee_bps=30, slippage_bps=50)
        self.assertIn("amount_in must be a positive int", str(ctx.exception))

    def test_boundary_counterexample_leverage_at_max(self) -> None:
        # Boundary counterexample: leverage exactly == MAX_LEVERAGE+1 must reject.
        candles = [{"close": 100}, {"close": 105}]
        with self.assertRaises(ValueError) as ctx:
            evaluate_bar_signal_and_leverage(candles, 1, notional=2100, margin_equity=100)
        self.assertIn("leverage exceeds MAX_LEVERAGE", str(ctx.exception))
