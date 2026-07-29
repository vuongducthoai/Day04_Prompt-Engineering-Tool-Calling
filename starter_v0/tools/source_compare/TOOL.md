---
name: source_compare
track: bonus
kind: local_analysis
inputs: [items, criterion, max_items]
outputs: [criterion, item_count, sources, source_claims, common_claims, potential_conflicts, missing_metadata, note]
side_effect: false
---

# source_compare

Compares metadata and text that have already been collected in the conversation.
It is a local, deterministic analysis tool: it never searches, fetches URLs,
calls external services, verifies facts, selects a correct source, or assigns
trustworthiness.

## Use when

- The user explicitly asks to compare at least two already available sources.
- The agent has the source items to pass in `items`.
- The requested comparison concerns coverage, agreements, or possible conflicts.

## Do not use when

- The user needs new web, social, paper, or URL research; use the relevant
  research tool first.
- Fewer than two items are available.
- The user asks which source is true, reliable, or authoritative.

## Inputs

- `items` (required): two or more source dictionaries. Supported fields are
  `title`, `url`, `source`, `summary`, `section`, and `published_at`.
- `criterion`: `coverage` (default), `agreement`, or `conflicts`.
- `max_items`: maximum items to analyze; defaults to `5` and is at least `2`.

## Output behavior

Every result includes `item_count`, selected source metadata, and a note that
the analysis does not verify facts.

- `coverage` returns each supplied source claim, indexes of items missing a URL
  or source name, and an empty `potential_conflicts` list.
- `agreement` returns only exact duplicate non-empty `summary` or `title` text
  in `common_claims`.
- `conflicts` returns supplied claims and an empty `potential_conflicts` list.

An empty conflict list means this minimal implementation found no automated
signal; it is not evidence that sources agree.

## Example

```python
source_compare(
    items=[
        {"title": "Report A", "source": "Publisher A", "summary": "Claim one."},
        {"title": "Report B", "source": "Publisher B", "summary": "Claim two."},
    ],
    criterion="coverage",
)
```

Use the returned information as a structured aid for the user's comparison,
and clearly label potential differences as unverified unless other evidence
establishes them.
