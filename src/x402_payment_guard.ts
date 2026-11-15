export interface TxConsumptionRecord {
  txId: string;
  boundAt: number;
  consumedAt?: number;
}

export function computeDerivedHints(statusCode: number, explicitRetryable?: boolean): { retryable: boolean } {
  if (typeof explicitRetryable === "boolean") {
    return { retryable: explicitRetryable };
  }
  return { retryable: statusCode === 429 || statusCode >= 500 };
}

export function markTxConsumed(existing: TxConsumptionRecord | undefined, txId: string, nowMs: number): TxConsumptionRecord {
  return {
    txId,
    boundAt: existing?.boundAt ?? nowMs,
    consumedAt: nowMs,
  };
}

export function verifyExactMicroUsdcPayment(paidMicroUsdc: bigint, requiredMicroUsdc: bigint, idempotencyKey: string): boolean {
  if (!idempotencyKey || idempotencyKey.trim().length < 8) {
    return false;
  }
  return paidMicroUsdc >= requiredMicroUsdc && requiredMicroUsdc > 0n;
}
