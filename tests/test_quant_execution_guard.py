import unittest
from src.quant_execution_guard import MAX_LEVERAGE, MAX_SLIPPAGE_BPS, compute_amm_swap_out, evaluate_bar_signal_and_leverage


class TestQuantExecutionGuard(unittest.TestCase):
    def test_amm_integer_math_and_slippage_bounds(self) -> None:
        self.assertEqual(MAX_SLIPPAGE_BPS, 500)
        out = compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=30, slippage_bps=50)
        self.assertEqual(out, 90184)
        with self.assertRaises(ValueError):
            compute_amm_swap_out(1000, 10000, 10000, slippage_bps=-50)

    def test_amm_reference_values(self) -> None:
        self.assertEqual(compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=30, slippage_bps=50), 90184)
        self.assertEqual(compute_amm_swap_out(200000, 1000000, 1000000, fee_bps=30, slippage_bps=50), 165336)

    def test_amm_fee_and_slippage_are_monotonic(self) -> None:
        base = compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=0, slippage_bps=0)
        self.assertEqual(base, 90910)
        self.assertGreater(base, compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=100, slippage_bps=0))
        self.assertGreater(base, compute_amm_swap_out(100000, 1000000, 1000000, fee_bps=0, slippage_bps=500))

    def test_amm_output_stays_inside_reserve(self) -> None:
        self.assertLess(compute_amm_swap_out(1000000, 1000000, 1000000, fee_bps=0, slippage_bps=0), 1000000)
        self.assertGreater(compute_amm_swap_out(1, 1000000, 1000000, fee_bps=0, slippage_bps=0), 0)
        self.assertRaises(ValueError, compute_amm_swap_out, 100000, 1000000, 1000000, 30, 501)

    def test_causal_candle_indexing_and_leverage(self) -> None:
        self.assertEqual(MAX_LEVERAGE, 20)
        candles = [{"close": 100}, {"close": 105}, {"close": 90}]
        sig, lev = evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=100)
        self.assertEqual((sig, lev), (1, 10))
        with self.assertRaises(ValueError):
            evaluate_bar_signal_and_leverage(candles, 1, notional=1000, margin_equity=0)
