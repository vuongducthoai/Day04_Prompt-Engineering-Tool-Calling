# Artifact v0

## Run information

- Provider: `openai`
- Suite: `base`
- Run file: `runs/v2_B_base_openrouter_20260729T152711535973.json`
- Artifact version: `v2+p87d2e5cc289d+td833307e2f90`
- Prompt hash: `87d2e5cc289d016050b2283a93f1037b348e57b6528e16173ad026b8e8816c05`
- Tools hash: `d833307e2f901dd8987b669aec72ba183c3155ac8c3ae12d136ffa3187192f43`

## Metrics

- Total cases: 20
- Measured cases: 20
- Provider error cases: 0
- Passed cases: 19
- Case accuracy: 0.95
- Tool routing accuracy: 1.0
- Argument accuracy: 0.95
- Multiturn accuracy: 1.0

## Failed cases

- - R12_confirm_before_send

## Baseline observation

The updated prompt and tool descriptions substantially improved routing and argument extraction, achieving 95% accuracy (19/20 cases). The remaining failure comes from the confirmation workflow: the agent still requests missing content before asking for explicit confirmation when a write action is requested. This artifact captures the latest behavior before refining confirmation priority.