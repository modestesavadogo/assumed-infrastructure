# Results: Qwen3-4B-Instruct-2507  (S1 split = test)

Model: Qwen/Qwen3-4B-Instruct-2507  revision: None  date: 2026-10-20 01:05:03
Dependent scenarios: 63  controls: 21  generations: 3496

## T1a. Per condition: dependent tasks, markers per 100 words (D = high-infrastructure, A = adaptation)
| condition | D_rate | D_ci | A_rate | A_ci | adapt_ratio | digital_rate | disclaimer | words | truncated |
|---|---|---|---|---|---|---|---|---|---|
| C00_none | 0.836 | [0.59, 1.12] | 0.181 | [0.10, 0.28] | 0.182 | 0.853 | 0.071 | 294.532 | 0.516 |
| C01_boston | 1.147 | [0.85, 1.48] | 0.219 | [0.12, 0.34] | 0.165 | 0.823 | 0.016 | 297.825 | 0.563 |
| C02_paris | 1.028 | [0.76, 1.33] | 0.202 | [0.10, 0.33] | 0.170 | 0.858 | 0.040 | 296.333 | 0.619 |
| C03_seoul | 0.969 | [0.69, 1.28] | 0.230 | [0.13, 0.37] | 0.196 | 0.981 | 0.040 | 293.151 | 0.548 |
| C04_ouagadougou | 0.756 | [0.44, 1.14] | 0.565 | [0.41, 0.74] | 0.436 | 0.757 | 0.032 | 290.675 | 0.532 |
| C05_rural_burkina | 0.423 | [0.25, 0.62] | 0.699 | [0.52, 0.90] | 0.626 | 0.530 | 0.040 | 307.405 | 0.524 |
| C06_lagos | 0.664 | [0.44, 0.92] | 0.390 | [0.26, 0.55] | 0.375 | 0.856 | 0.048 | 296.048 | 0.563 |
| C07_dhaka | 0.654 | [0.43, 0.92] | 0.296 | [0.18, 0.44] | 0.312 | 0.868 | 0.040 | 291.103 | 0.540 |
| C08_ouaga_constraints | 0.488 | [0.35, 0.64] | 2.470 | [2.27, 2.68] | 0.837 | 1.542 | 0.000 | 304.683 | 0.540 |
| C09_constraints_only | 0.552 | [0.42, 0.69] | 2.611 | [2.41, 2.83] | 0.825 | 1.920 | 0.032 | 311.048 | 0.508 |

## T1b. Per condition group: dependent tasks, markers per 100 words (D = high-infrastructure, A = adaptation)
| grp | D_rate | D_ci | A_rate | A_ci | adapt_ratio | digital_rate | disclaimer | words | truncated |
|---|---|---|---|---|---|---|---|---|---|
| none | 0.836 | [0.59, 1.12] | 0.181 | [0.10, 0.28] | 0.182 | 0.853 | 0.071 | 294.532 | 0.516 |
| high | 1.048 | [0.78, 1.34] | 0.217 | [0.12, 0.34] | 0.177 | 0.887 | 0.032 | 295.770 | 0.577 |
| low | 0.624 | [0.40, 0.89] | 0.487 | [0.36, 0.63] | 0.445 | 0.753 | 0.040 | 296.308 | 0.540 |
| spec_loc | 0.488 | [0.35, 0.64] | 2.470 | [2.27, 2.68] | 0.837 | 1.542 | 0.000 | 304.683 | 0.540 |
| spec_only | 0.552 | [0.42, 0.69] | 2.611 | [2.41, 2.83] | 0.825 | 1.920 | 0.032 | 311.048 | 0.508 |

## T2. D rate by category and group
| grp | pay_D_rate | net_D_rate | power_D_rate | trans_D_rate | cost_D_rate | online_D_rate |
|---|---|---|---|---|---|---|
| none | 0.121 | 0.201 | 0.012 | 0.159 | 0.287 | 0.056 |
| high | 0.109 | 0.291 | 0.009 | 0.268 | 0.265 | 0.106 |
| low | 0.093 | 0.241 | 0.004 | 0.141 | 0.063 | 0.083 |
| spec_loc | 0.040 | 0.238 | 0.005 | 0.047 | 0.081 | 0.076 |
| spec_only | 0.077 | 0.267 | 0.003 | 0.055 | 0.069 | 0.082 |

## T3. Primary paired contrasts on D rate (Holm over the set; unit = scenario)
| contrast | n | mean_diff_D | ci | dz | p_raw | p_holm |
|---|---|---|---|---|---|---|
| high - none | 63 | 0.2116 | [0.07, 0.35] | 0.3600 | 0.0020 | 0.0082 |
| low - none | 63 | -0.2123 | [-0.40, -0.04] | -0.2924 | 0.0745 | 0.2234 |
| low - high | 63 | -0.4239 | [-0.59, -0.28] | -0.6700 | 0.0000 | 0.0000 |
| spec_loc - low | 63 | -0.1358 | [-0.33, 0.04] | -0.1769 | 0.3891 | 0.7781 |
| spec_only - low | 63 | -0.0719 | [-0.28, 0.11] | -0.0893 | 0.4414 | 0.7781 |

### T3-A. Same contrasts, template A only (robustness, descriptive)
| contrast | n | mean_diff_D | ci | dz | p_raw |
|---|---|---|---|---|---|
| high - none | 63 | 0.2163 | [0.05, 0.38] | 0.3185 | 0.0027 |
| low - none | 63 | -0.2003 | [-0.42, -0.01] | -0.2377 | 0.2091 |
| low - high | 63 | -0.4166 | [-0.60, -0.26] | -0.5911 | 0.0000 |
| spec_loc - low | 63 | -0.1184 | [-0.33, 0.08] | -0.1383 | 0.4660 |
| spec_only - low | 63 | -0.1002 | [-0.32, 0.10] | -0.1126 | 0.9415 |

### T3-B. Same contrasts, template B only (robustness, descriptive)
| contrast | n | mean_diff_D | ci | dz | p_raw |
|---|---|---|---|---|---|
| high - none | 63 | 0.2070 | [0.00, 0.41] | 0.2437 | 0.0257 |
| low - none | 63 | -0.2242 | [-0.42, -0.04] | -0.2860 | 0.0576 |
| low - high | 63 | -0.4312 | [-0.62, -0.26] | -0.5812 | 0.0000 |
| spec_loc - low | 63 | -0.1531 | [-0.37, 0.04] | -0.1802 | 0.3280 |
| spec_only - low | 63 | -0.0436 | [-0.26, 0.15] | -0.0523 | 0.5692 |

## T4. Infrastructure-independent controls (spurious injection check)
| grp | ctx_mention | D_rate | A_rate | disclaimer |
|---|---|---|---|---|
| none | 0.000 | 0.009 | 0.080 | 0.000 |
| high | 0.619 | 0.108 | 0.199 | 0.000 |
| low | 0.470 | 0.032 | 0.146 | 0.006 |
| spec_loc | 1.000 | 0.119 | 1.429 | 0.024 |
| spec_only | 0.976 | 0.131 | 1.564 | 0.000 |

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
