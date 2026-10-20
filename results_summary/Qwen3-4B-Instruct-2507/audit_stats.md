# Blind audit: manual codes (single annotator, partly blind to condition)

## Per condition
| condition | n | high_infra_mean | high_ci | share_with_high | accommodations_mean | acc_ci |
|---|---|---|---|---|---|---|
| C00_none | 24 | 2.46 | [1.79, 3.17] | 0.83 | 0.04 | [0.0, 0.12] |
| C01_boston | 24 | 2.88 | [2.29, 3.42] | 0.92 | 0.00 | [0.0, 0.0] |
| C04_ouagadougou | 24 | 1.00 | [0.54, 1.46] | 0.50 | 0.42 | [0.17, 0.71] |
| C08_ouaga_constraints | 24 | 0.29 | [0.08, 0.54] | 0.25 | 4.21 | [3.88, 4.54] |
| C09_constraints_only | 24 | 0.38 | [0.12, 0.62] | 0.29 | 4.58 | [4.21, 4.96] |

## Paired contrasts (exploratory, n = 24 scenarios, no multiplicity correction)
| contrast | measure | n | mean_diff | ci | p_raw |
|---|---|---|---|---|---|
| C01_boston - C00_none | high_infra_steps | 24 | 0.417 | [-0.08, 0.92] | 0.138 |
| C01_boston - C00_none | accommodations | 24 | -0.042 | [-0.12, 0.00] | 0.317 |
| C04_ouagadougou - C00_none | high_infra_steps | 24 | -1.458 | [-2.17, -0.75] | 0.002 |
| C04_ouagadougou - C00_none | accommodations | 24 | 0.375 | [0.17, 0.62] | 0.007 |
| C08_ouaga_constraints - C04_ouagadougou | high_infra_steps | 24 | -0.708 | [-1.25, -0.17] | 0.022 |
| C08_ouaga_constraints - C04_ouagadougou | accommodations | 24 | 3.792 | [3.38, 4.21] | 0.000 |
| C09_constraints_only - C04_ouagadougou | high_infra_steps | 24 | -0.625 | [-1.17, -0.08] | 0.052 |
| C09_constraints_only - C04_ouagadougou | accommodations | 24 | 4.167 | [3.67, 4.62] | 0.000 |
| C08_ouaga_constraints - C09_constraints_only | high_infra_steps | 24 | -0.083 | [-0.42, 0.25] | 0.623 |
| C08_ouaga_constraints - C09_constraints_only | accommodations | 24 | -0.375 | [-0.75, -0.04] | 0.059 |