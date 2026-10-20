# Replication audit (manual codes; single annotator; partly blind to condition; exploratory)

## Per model and condition
| model | condition | n | high_infra | high_ci | share_with_high | accommodations | acc_ci |
|---|---|---|---|---|---|---|---|
| Llama-3.2-3B-Instruct | C00_none | 24 | 1.33 | [0.83, 1.88] | 0.62 | 0.00 | [0.0, 0.0] |
| Llama-3.2-3B-Instruct | C09_constraints_only | 24 | 1.08 | [0.75, 1.42] | 0.71 | 2.38 | [1.88, 2.88] |
| Phi-4-mini-instruct | C00_none | 24 | 1.62 | [1.17, 2.12] | 0.79 | 0.00 | [0.0, 0.0] |
| Phi-4-mini-instruct | C09_constraints_only | 24 | 1.25 | [0.79, 1.75] | 0.67 | 3.33 | [2.58, 4.08] |
| Qwen3-1.7B | C00_none | 24 | 1.46 | [1.0, 1.92] | 0.71 | 0.04 | [0.0, 0.12] |
| Qwen3-1.7B | C09_constraints_only | 24 | 1.92 | [1.46, 2.42] | 0.96 | 1.75 | [1.33, 2.21] |
| Qwen3-4B-Instruct-2507 | C00_none | 24 | 2.46 | [1.79, 3.17] | 0.83 | 0.04 | [0.0, 0.12] |
| Qwen3-4B-Instruct-2507 | C09_constraints_only | 24 | 0.38 | [0.12, 0.62] | 0.29 | 4.58 | [4.21, 4.96] |

## Within-model change, constraints-only minus none (n = 24 scenarios, no multiplicity correction)
| model | measure | contrast | n | mean_diff | ci | p_raw |
|---|---|---|---|---|---|---|
| Llama-3.2-3B-Instruct | high_infra_steps | constraints_only - none | 24 | -0.250 | [-0.88, 0.33] | 0.498 |
| Llama-3.2-3B-Instruct | accommodations | constraints_only - none | 24 | 2.375 | [1.88, 2.88] | 0.000 |
| Phi-4-mini-instruct | high_infra_steps | constraints_only - none | 24 | -0.375 | [-0.92, 0.17] | 0.190 |
| Phi-4-mini-instruct | accommodations | constraints_only - none | 24 | 3.333 | [2.58, 4.08] | 0.000 |
| Qwen3-1.7B | high_infra_steps | constraints_only - none | 24 | 0.458 | [-0.21, 1.17] | 0.208 |
| Qwen3-1.7B | accommodations | constraints_only - none | 24 | 1.708 | [1.29, 2.12] | 0.000 |
| Qwen3-4B-Instruct-2507 | high_infra_steps | constraints_only - none | 24 | -2.083 | [-2.79, -1.42] | 0.000 |
| Qwen3-4B-Instruct-2507 | accommodations | constraints_only - none | 24 | 4.542 | [4.17, 4.96] | 0.000 |

## Lexicon vs manual on the replication models
| model | n | precision | recall | kappa | rho_D | rho_A |
|---|---|---|---|---|---|---|
| Phi-4-mini-instruct | 48 | 0.74 | 0.40 | 0.01 | 0.11 | 0.85 |
| Qwen3-1.7B | 48 | 0.92 | 0.55 | 0.17 | 0.37 | 0.75 |
| Llama-3.2-3B-Instruct | 48 | 0.94 | 0.47 | 0.33 | 0.43 | 0.85 |