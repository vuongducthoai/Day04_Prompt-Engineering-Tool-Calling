from __future__ import annotations

from typing import Any


def compare_sources(
    items: list[dict[str, Any]], criterion: str = "coverage", max_items: int = 5
) -> dict[str, Any]:
    """Compare supplied source metadata only; never retrieves or verifies sources."""
    selected = items[:max(2, max_items)]
    summaries = [str(item.get("summary") or item.get("title") or "").strip() for item in selected]
    sources = [
        {key: item[key] for key in ("title", "url", "source", "published_at") if item.get(key)}
        for item in selected
    ]
    result: dict[str, Any] = {
        "tool": "source_compare",
        "criterion": criterion,
        "item_count": len(selected),
        "sources": sources,
        "note": "Comparison is limited to supplied source text and metadata; it does not verify facts.",
    }
    if criterion == "agreement":
        result["common_claims"] = [text for text in summaries if summaries.count(text) > 1 and text]
    elif criterion == "conflicts":
        result["potential_conflicts"] = []
        result["source_claims"] = summaries
    else:
        result["source_claims"] = summaries
        result["missing_metadata"] = [
            index for index, item in enumerate(selected) if not item.get("url") or not item.get("source")
        ]
        result["potential_conflicts"] = []
    return result
