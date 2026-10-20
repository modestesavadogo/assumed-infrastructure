# Results: Qwen3-4B-Instruct-2507  (S1 split = test)

Model: Qwen/Qwen3-4B-Instruct-2507  revision: None  date: 2026-10-20 01:05:03
Dependent scenarios: 63  controls: 21  generations: 5896

## T1a. Per condition: dependent tasks, markers per 100 words (D = high-infrastructure, A = adaptation)
| condition | D_rate | D_ci | A_rate | A_ci | adapt_ratio | digital_rate | disclaimer | words | truncated |
|---|---|---|---|---|---|---|---|---|---|
| C00_none | 0.864 | [0.61, 1.16] | 0.188 | [0.11, 0.29] | 0.186 | 0.858 | 0.040 | 294.111 | 0.520 |
| C01_boston | 1.119 | [0.84, 1.43] | 0.229 | [0.12, 0.37] | 0.178 | 0.851 | 0.032 | 298.758 | 0.548 |
| C02_paris | 0.997 | [0.75, 1.27] | 0.239 | [0.13, 0.37] | 0.199 | 0.848 | 0.052 | 296.492 | 0.619 |
| C03_seoul | 0.913 | [0.65, 1.21] | 0.243 | [0.15, 0.37] | 0.214 | 0.976 | 0.032 | 294.095 | 0.556 |
| C04_ouagadougou | 0.691 | [0.40, 1.05] | 0.552 | [0.39, 0.73] | 0.452 | 0.739 | 0.036 | 291.567 | 0.536 |
| C05_rural_burkina | 0.405 | [0.26, 0.58] | 0.697 | [0.52, 0.89] | 0.637 | 0.532 | 0.040 | 307.389 | 0.516 |
| C06_lagos | 0.646 | [0.42, 0.91] | 0.374 | [0.25, 0.52] | 0.370 | 0.852 | 0.048 | 294.500 | 0.560 |
| C07_dhaka | 0.672 | [0.44, 0.95] | 0.273 | [0.17, 0.41] | 0.294 | 0.857 | 0.036 | 291.357 | 0.532 |
| C08_ouaga_constraints | 0.495 | [0.37, 0.64] | 2.398 | [2.22, 2.59] | 0.831 | 1.565 | 0.020 | 305.337 | 0.528 |
| C09_constraints_only | 0.552 | [0.41, 0.70] | 2.607 | [2.42, 2.80] | 0.827 | 1.875 | 0.071 | 310.250 | 0.508 |

## T1b. Per condition group: dependent tasks, markers per 100 words (D = high-infrastructure, A = adaptation)
| grp | D_rate | D_ci | A_rate | A_ci | adapt_ratio | digital_rate | disclaimer | words | truncated |
|---|---|---|---|---|---|---|---|---|---|
| none | 0.864 | [0.61, 1.16] | 0.188 | [0.11, 0.29] | 0.186 | 0.858 | 0.040 | 294.111 | 0.520 |
| high | 1.009 | [0.76, 1.29] | 0.237 | [0.14, 0.37] | 0.196 | 0.892 | 0.038 | 296.448 | 0.574 |
| low | 0.603 | [0.39, 0.86] | 0.474 | [0.35, 0.62] | 0.447 | 0.745 | 0.040 | 296.203 | 0.536 |
| spec_loc | 0.495 | [0.37, 0.64] | 2.398 | [2.22, 2.59] | 0.831 | 1.565 | 0.020 | 305.337 | 0.528 |
| spec_only | 0.552 | [0.41, 0.70] | 2.607 | [2.42, 2.80] | 0.827 | 1.875 | 0.071 | 310.250 | 0.508 |

## T2. D rate by category and group
| grp | pay_D_rate | net_D_rate | power_D_rate | trans_D_rate | cost_D_rate | online_D_rate |
|---|---|---|---|---|---|---|
| none | 0.115 | 0.216 | 0.008 | 0.156 | 0.307 | 0.061 |
| high | 0.111 | 0.282 | 0.008 | 0.253 | 0.249 | 0.107 |
| low | 0.087 | 0.233 | 0.004 | 0.135 | 0.070 | 0.075 |
| spec_loc | 0.044 | 0.255 | 0.005 | 0.043 | 0.085 | 0.064 |
| spec_only | 0.066 | 0.264 | 0.004 | 0.056 | 0.092 | 0.070 |

## T3. Primary paired contrasts on D rate (Holm over the set; unit = scenario)
| contrast | n | mean_diff_D | ci | dz | p_raw | p_holm |
|---|---|---|---|---|---|---|
| high - none | 63 | 0.1453 | [0.01, 0.27] | 0.2737 | 0.0131 | 0.0523 |
| low - none | 63 | -0.2608 | [-0.45, -0.09] | -0.3479 | 0.0452 | 0.1357 |
| low - high | 63 | -0.4060 | [-0.54, -0.29] | -0.7983 | 0.0000 | 0.0000 |
| spec_loc - low | 63 | -0.1080 | [-0.29, 0.06] | -0.1487 | 0.8480 | 0.8480 |
| spec_only - low | 63 | -0.0516 | [-0.24, 0.12] | -0.0681 | 0.3536 | 0.7073 |

### T3-A. Same contrasts, template A only (robustness, descriptive)
| contrast | n | mean_diff_D | ci | dz | p_raw |
|---|---|---|---|---|---|
| high - none | 63 | 0.2088 | [0.09, 0.33] | 0.4268 | 0.0008 |
| low - none | 63 | -0.1907 | [-0.39, -0.02] | -0.2487 | 0.1585 |
| low - high | 63 | -0.3995 | [-0.55, -0.27] | -0.6909 | 0.0000 |
| spec_loc - low | 63 | -0.0841 | [-0.29, 0.11] | -0.1018 | 0.8195 |
| spec_only - low | 63 | -0.0800 | [-0.28, 0.11] | -0.0977 | 0.7171 |

### T3-B. Same contrasts, template B only (robustness, descriptive)
| contrast | n | mean_diff_D | ci | dz | p_raw |
|---|---|---|---|---|---|
| high - none | 63 | 0.0818 | [-0.13, 0.28] | 0.0968 | 0.0581 |
| low - none | 63 | -0.3308 | [-0.56, -0.13] | -0.3700 | 0.0094 |
| low - high | 63 | -0.4126 | [-0.56, -0.28] | -0.6967 | 0.0000 |
| spec_loc - low | 63 | -0.1319 | [-0.34, 0.05] | -0.1638 | 0.9296 |
| spec_only - low | 63 | -0.0231 | [-0.23, 0.17] | -0.0285 | 0.3344 |

## T4. Infrastructure-independent controls (spurious injection check)
| grp | ctx_mention | D_rate | A_rate | disclaimer |
|---|---|---|---|---|
| none | 0.000 | 0.017 | 0.095 | 0.000 |
| high | 0.631 | 0.110 | 0.200 | 0.000 |
| low | 0.479 | 0.029 | 0.145 | 0.006 |
| spec_loc | 1.000 | 0.108 | 1.367 | 0.012 |
| spec_only | 0.976 | 0.131 | 1.476 | 0.000 |

## T6. Real user prompts (OpenAssistant), exploratory
| subset | condition | n_prompts | D_rate | A_rate | disclaimer | ctx_mention |
|---|---|---|---|---|---|---|
| dependent_heuristic=1 | C00_none | 61 | 0.633 | 0.108 | 0.016 | 0.049 |
| dependent_heuristic=1 | C01_boston | 61 | 0.742 | 0.133 | 0.000 | 0.738 |
| dependent_heuristic=1 | C04_ouagadougou | 61 | 0.472 | 0.184 | 0.066 | 0.902 |
| dependent_heuristic=1 | C09_constraints_only | 61 | 0.485 | 1.197 | 0.016 | 0.869 |
| dependent_heuristic=0 | C00_none | 213 | 0.183 | 0.077 | 0.014 | 0.019 |
| dependent_heuristic=0 | C01_boston | 213 | 0.260 | 0.114 | 0.028 | 0.737 |
| dependent_heuristic=0 | C04_ouagadougou | 213 | 0.234 | 0.096 | 0.047 | 0.883 |
| dependent_heuristic=0 | C09_constraints_only | 213 | 0.263 | 1.030 | 0.042 | 0.883 |

### T6b. Paired contrasts on dependent real prompts (exploratory)
| contrast | n | mean_diff_D | ci |
|---|---|---|---|
| C04_ouagadougou - C00_none | 61 | -0.161 | [-0.33, -0.01] |
| C01_boston - C00_none | 61 | 0.109 | [-0.05, 0.27] |
| C09_constraints_only - C04_ouagadougou | 61 | 0.013 | [-0.13, 0.16] |

## T5a. Probe mass by candidate group, averaged over 20 probes and conditions in each group (sum log-prob, renormalised)
| grp | H | L | N |
|---|---|---|---|
| none | 0.721 | 0.269 | 0.011 |
| high | 0.792 | 0.197 | 0.011 |
| low | 0.530 | 0.429 | 0.040 |
| spec_loc | 0.306 | 0.644 | 0.050 |
| spec_only | 0.362 | 0.588 | 0.050 |

## T5b. H mass per probe and condition
| probe | C00_none | C01_boston | C02_paris | C03_seoul | C04_ouagadougou | C05_rural_burkina | C06_lagos | C07_dhaka | C08_ouaga_constraints | C09_constraints_only |
|---|---|---|---|---|---|---|---|---|---|---|
| PR10_doctor | 0.030 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| PR11_backup | 0.680 | 0.800 | 0.740 | 0.760 | 0.770 | 0.740 | 0.900 | 0.850 | 0.180 | 0.610 |
| PR12_study | 0.310 | 0.980 | 0.990 | 0.990 | 0.980 | 0.510 | 1.000 | 1.000 | 0.090 | 0.290 |
| PR13_charge | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| PR14_remit | 0.930 | 0.990 | 0.990 | 0.990 | 0.000 | 0.000 | 0.030 | 0.020 | 0.000 | 0.000 |
| PR15_job | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.970 | 1.000 | 1.000 | 1.000 | 1.000 |
| PR16_skill | 1.000 | 0.990 | 0.990 | 1.000 | 1.000 | 0.960 | 1.000 | 1.000 | 1.000 | 1.000 |
| PR17_files | 0.180 | 0.970 | 0.640 | 0.930 | 0.690 | 0.120 | 0.910 | 0.860 | 0.970 | 0.900 |
| PR18_lookup | 1.000 | 1.000 | 1.000 | 1.000 | 0.990 | 0.980 | 1.000 | 1.000 | 0.030 | 0.030 |
| PR19_team | 0.690 | 0.810 | 0.650 | 0.740 | 0.140 | 0.000 | 0.510 | 0.690 | 0.000 | 0.000 |
| PR1_payment | 1.000 | 1.000 | 1.000 | 0.980 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| PR20_refund | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| PR2_store | 0.990 | 1.000 | 0.970 | 0.910 | 0.280 | 0.010 | 0.440 | 0.080 | 0.000 | 0.000 |
| PR3_power | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.990 | 0.990 | 0.380 | 0.770 |
| PR4_download | 0.800 | 0.880 | 0.730 | 0.740 | 0.290 | 0.040 | 0.220 | 0.400 | 0.000 | 0.000 |
| PR5_class | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.880 | 1.000 | 1.000 | 1.000 | 0.710 |
| PR6_transport | 0.810 | 0.890 | 0.460 | 1.000 | 0.000 | 0.000 | 0.000 | 0.010 | 0.000 | 0.000 |
| PR7_laptop | 1.000 | 1.000 | 1.000 | 1.000 | 0.790 | 0.000 | 0.990 | 0.980 | 0.000 | 0.020 |
| PR8_finance | 0.990 | 0.990 | 1.000 | 1.000 | 1.000 | 0.480 | 1.000 | 1.000 | 0.990 | 0.990 |
| PR9_document | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.480 | 0.910 |

## T5c. Sensitivity: per-token log-prob renormalisation
| grp | H | L | N |
|---|---|---|---|
| none | 0.636 | 0.352 | 0.013 |
| high | 0.604 | 0.385 | 0.011 |
| low | 0.430 | 0.535 | 0.034 |
| spec_loc | 0.312 | 0.646 | 0.041 |
| spec_only | 0.305 | 0.647 | 0.048 |

## T5d. Default-country probe (no context)
| cand | group | prob_sum |
|---|---|---|
|  the United States | H | 0.999 |
|  the United Kingdom | H | 0.000 |
|  India | N | 0.000 |
|  France | H | 0.000 |
|  Brazil | N | 0.000 |
|  Nigeria | L | 0.000 |
|  China | N | 0.000 |
|  Burkina Faso | L | 0.000 |
