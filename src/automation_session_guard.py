from __future__ import annotations

MIN_COOLDOWN_MS = 250
MIN_PROXY_TTL_SECONDS = 60


def verify_worker_profile_isolation(profiles: list[dict[str, int]]) -> bool:
    if not profiles:
        raise ValueError("profiles cannot be empty")
    seeds = set()
    for p in profiles:
        seed = int(p["canvas_seed"])
        ttl = int(p.get("proxy_rotation_ttl", 0))
        if ttl < MIN_PROXY_TTL_SECONDS or seed in seeds:
            return False
        seeds.add(seed)
    return True


def validate_affiliate_and_cooldown(click_timestamp: int, conversion_timestamp: int, action_interval_ms: int) -> bool:
    if action_interval_ms < MIN_COOLDOWN_MS:
        raise ValueError("action_interval_ms violates MIN_COOLDOWN_MS")
    if click_timestamp <= 0 or click_timestamp > conversion_timestamp:
        return False
    return True
