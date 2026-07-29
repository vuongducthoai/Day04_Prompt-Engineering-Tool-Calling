# Artifact v0

## Run information

- Provider: `openai`
- Suite: `base`
- Run file: `runs/v0_B_base_openai_20260729T101359397246.json`
- Artifact version: `v0+pf0c107a9d7a1+t011c271ef0bb`
- Prompt hash: `eb1c8179815bd79d34de7d326420bb99b3072e6e8ae96464c02d4411f905fc68`
- Tools hash: `6cdb53d5d7b8de80d60b298b1357f462cedbedfae261d5ba60b08ccc401687c5`

## Metrics

- Total cases: 20
- Measured cases: 20
- Provider error cases: 0
- Passed cases: 14
- Case accuracy: 0.7
- Tool routing accuracy: 0.75
- Argument accuracy: 0.7
- Multiturn accuracy: 1.0

## Failed cases

- R08_out_of_scope
- R10_missing_handle
- R11_missing_url
- R12_confirm_before_send
- R13_parallel_web_and_tweets
- R14_out_of_scope_coding

## Baseline observation

The starter prompt encourages guessing missing arguments, selecting only one tool,
and performing sensitive actions without explicit confirmation. This artifact is
preserved as the baseline before prompt and tool-declaration optimization.
