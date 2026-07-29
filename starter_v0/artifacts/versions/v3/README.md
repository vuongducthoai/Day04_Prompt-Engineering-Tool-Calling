# Artifact v3

## Hypothesis

V2 achieved full accuracy on the fixed base evaluation, but the agent did not
yet have a declared routing policy for the new `source_compare` tool.

Adding a narrow tool declaration and a minimal routing rule should extend the
agent's source-comparison capability without causing regression on the base
suite.

## Changed artifacts

- `artifacts/system_prompt.md`
- `artifacts/tools.yaml`
- `tools/source_compare/`
- `tools/__init__.py`

## Main changes

- Added the `source_compare` tool to the agent registry.
- Added a deterministic source-comparison implementation and a callable smoke
  test.
- Added tool declaration with supported criteria:
  - `coverage`
  - `agreement`
  - `conflicts`
- Restricted the tool to source items already collected.
- Preserved literal user search keywords.
- Preserved confirmation-first behavior for side-effecting actions.

## Run information

- Provider: `openrouter`
- Model: `openai/gpt-4o-mini`
- Suite: `base`
- Run file: `runs/v3_B_base_openrouter_20260729T153413547933.json`
- Artifact version: `v3+p7e4ab0940e48+tc26f50b256ea`
- Case accuracy: `0.95` (19/20 passed)
- Passed cases: 20/20
- Case accuracy: 1.00
- Tool routing accuracy: 1.00
- Argument accuracy: 1.00
- Multiturn accuracy: 1.00
- Provider error cases: 0

## Regression result

V3 preserved the complete v2 base score while adding the new
`source_compare` capability.
