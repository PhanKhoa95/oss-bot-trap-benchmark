from __future__ import annotations

MAX_AUTO_REFUND_CENTS = 5000


def authorize_refund_tool_call(amount_cents: int, user_message: str, is_authenticated_admin: bool = False) -> bool:
    if amount_cents <= 0:
        raise ValueError("amount_cents must be positive")
    if amount_cents <= MAX_AUTO_REFUND_CENTS:
        return True
    return bool(is_authenticated_admin)


def filter_tenant_rag_documents(docs: list[dict[str, str]], session_tenant_id: str) -> list[dict[str, str]]:
    if not session_tenant_id:
        raise ValueError("session_tenant_id is required")
    return [d for d in docs if d.get("tenant_id") == session_tenant_id]


def process_idempotent_payment_webhook(reference_code: str, amount_cents: int, processed_refs: set[str]) -> dict[str, int | bool]:
    if reference_code in processed_refs:
        return {"duplicate": True, "credited_cents": 0}
    processed_refs.add(reference_code)
    return {"duplicate": False, "credited_cents": amount_cents}
