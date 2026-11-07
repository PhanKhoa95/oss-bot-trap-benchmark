# -*- coding: utf-8 -*-
import json

def render_gap_json(headers: list[dict[str, int]]) -> str:
    """Serializes sequence gap diagnostics into a JSON string."""
    gaps = []
    for idx in range(1, len(headers)):
        prev_seq = int(headers[idx - 1].get("seq", 0))
        curr_seq = int(headers[idx].get("seq", 0))
        if curr_seq != prev_seq + 1:
            gaps.append({
                "expected": prev_seq + 1,
                "actual": curr_seq,
                "gap_size": curr_seq - prev_seq - 1
            })
    
    return json.dumps({
        "valid": len(gaps) == 0,
        "gaps": gaps
    }, indent=2)