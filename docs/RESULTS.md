# Results: assumed infrastructure in four small instruct LLMs (main analysis: Qwen3-4B-Instruct-2507)

Scope: the main analysis is on one model (`Qwen/Qwen3-4B-Instruct-2507`, fp16, non-thinking) with the pre-registered prompt sets and contexts (PREREGISTRATION.md v2), run once on Kaggle on 2026-10-19/20. Three other models (Phi-4-mini-instruct, Qwen3-1.7B, Llama-3.2-3B-Instruct) were then run on the controlled scenarios only and are reported in the replication sections. Everything follows the pre-registered analysis unless marked *exploratory*. Raw outputs: `results/<model>/generations.jsonl`, `probes.jsonl`. Tables: `results/<model>/tables_test.md`, `audit_stats.md`, `results/cross_model_test_greedy.md`, `results/replication_audit_stats.md`. Every number below can be recomputed with `python scripts/reproduce.py` (see REPRODUCE.md); confidence intervals are percentile bootstrap intervals (10,000 resamples over scenarios, seed 0).

## Headline findings
1. **With no context the model behaves like a high-infrastructure user.** The default-country probe puts 99.9% on "the United States". Told "Boston/Paris/Seoul", it uses slightly *more* high-infrastructure markers than with no context (D rate 1.01 vs 0.86 per 100 words; paired dz = 0.27, Holm p = 0.052).
2. **Naming a lower-infrastructure place changes the text, but modestly in lexical terms.** D rate falls from 0.86 (none) to 0.60 (low group) (dz = -0.35, Holm p = 0.14, not significant after correction) and from 1.01 (high group) to 0.60 (dz = -0.80, Holm p < 0.0001). Adaptation markers rise from 0.19 to 0.47 per 100 words.
3. **Explicit constraints change the plan far more than a place name.** Adaptation markers reach 2.40 (location + constraints) and 2.61 (constraints only) per 100 words, versus 0.47 for place only. The blind manual audit agrees: explicit accommodations per response 0.42 (place only) vs 4.21 and 4.58 (constraints).
4. **The model plans well under stated constraints but does not infer them from the place.** The pre-registered D-rate contrast did not show it (spec_only vs low: -0.05, Holm p = 0.71), but accommodations and manual high-infrastructure steps do (see audit).
5. **Next-token probes show a split picture.** Payment, remittance, transport and purchase probes flip completely to adapted options (mobile money, bus, local shop) as soon as the place is Ouagadougou. **The power probe does not move with place at all** (P("leave the laptop plugged in") = 1.00 for none, Boston, Ouagadougou and rural Burkina; it drops only with explicit constraints: 0.38 and 0.77).
6. **The lexicon underestimates adaptation.** Against the blind manual audit it has weak response-level agreement (kappa = 0.15), so the lexical D-rate differences above are a conservative view.
7. **Across four models** (replication below): all default to the United States and show the same probe pattern (none, then a low-infrastructure place, then constraints). Given explicit constraints all four add accommodations, but **only Qwen3-4B removes reliance on high-infrastructure services**; Phi-4-mini, Llama-3.2-3B and Qwen3-1.7B add accommodations while keeping such steps in 67%, 71% and 96% of their constraint responses (manual audit).

## Pre-registered hypotheses
| | Verdict | Evidence |
|---|---|---|
| H1 default world | **Partly supported** (criterion not met as written) | |D(high)-D(none)| gives dz = 0.27, above the |dz| < 0.2 criterion; adaptation ratio none 0.19 < low 0.45 holds; probe H mass none 0.72 vs high 0.79 vs low 0.53; default country = United States (0.999). |
| H2 shallow adaptation | **Mostly not supported as stated** | A markers do rise (0.19 to 0.47) and D(low) stays > 0 (0.60), but the generic-disclaimer rate does not rise (0.040 vs 0.040) and D(low) is not distinguishable from D(spec_loc) (-0.11, CI [-0.29, 0.06]). Adaptation to place alone is real but small, and mostly localisation. |
| H3 inference gap | **Not supported on D rate; supported on accommodations (exploratory)** | D: spec_only - low = -0.05, Holm p = 0.71. A markers 2.61 vs 0.47; audit accommodations 4.58 vs 0.42; audit high-infrastructure steps 0.38 vs 1.00 (raw p = 0.052, n = 24). |
| H4 spurious injection | **Not informative as operationalised** | Context mentions in controls are higher under low (0.48) than none (0.00), but this is mostly echoing the stated place (Boston: 0.63). D markers stay near zero in controls (0.03). No evidence of unwarranted infrastructure injection. |
| H5 probes | **Supported, with caveats** | Mean H mass none 0.72 > 0.5; low 0.53 (shifted, not fully); spec_only 0.36 < low. Three probes (doctor, charge, refund) are degenerate under the pre-registered sum log-prob normalisation because of candidate wording (see below). |
| H6 heterogeneity | Descriptive | D rate: Ouagadougou 0.69, rural Burkina 0.41, Lagos 0.65, Dhaka 0.67. A rate: 0.55, 0.70, 0.37, 0.27. Adaptation is strongest for the rural-village context and weaker for Lagos and Dhaka than for Ouagadougou. |

## Primary paired contrasts (S1 test split, 63 dependent scenarios, D rate per 100 words)
| contrast | mean diff | 95% CI | dz | p (Holm) |
|---|---|---|---|---|
| high - none | +0.145 | [0.01, 0.27] | 0.27 | 0.052 |
| low - none | -0.261 | [-0.45, -0.09] | -0.35 | 0.136 |
| low - high | -0.406 | [-0.54, -0.29] | -0.80 | < 0.0001 |
| spec_loc - low | -0.108 | [-0.29, 0.06] | -0.15 | 0.848 |
| spec_only - low | -0.052 | [-0.24, 0.12] | -0.07 | 0.707 |

Per template: the template-A pattern is the same for high - none (+0.21, p_raw = 0.0008) and low - high (-0.40); for low - none template B shows -0.33 (p_raw = 0.009) while template A shows -0.19 (p_raw = 0.16). Template differences are descriptive.

## Real user prompts (OpenAssistant, 274 prompts; exploratory)
For the 61 prompts flagged as infrastructure-dependent by a prompt-only keyword heuristic: D rate 0.63 (none), 0.74 (Boston), 0.47 (Ouagadougou), 0.49 (constraints only); A rate 0.11, 0.13, 0.18, 1.20. Ouagadougou vs none: -0.16, CI [-0.33, -0.01]. The direction matches the controlled scenarios. 92% of these responses were truncated at 500 tokens.

## Blind audit (120 responses, 24 scenarios x 5 conditions; single annotator)
| condition | high-infrastructure steps | share with at least one | accommodations |
|---|---|---|---|
| none | 2.46 [1.79, 3.17] | 0.83 | 0.04 |
| Boston | 2.88 [2.29, 3.42] | 0.92 | 0.00 |
| Ouagadougou | 1.00 [0.54, 1.46] | 0.50 | 0.42 [0.17, 0.71] |
| Ouagadougou + constraints | 0.29 [0.08, 0.54] | 0.25 | 4.21 [3.88, 4.54] |
| constraints only | 0.38 [0.12, 0.62] | 0.29 | 4.58 [4.21, 4.96] |

Exploratory paired contrasts (n = 24, no multiplicity correction): Ouagadougou - none = -1.46 high-infrastructure steps (CI [-2.17, -0.75]); constraints-only - Ouagadougou = -0.63 steps ([-1.17, -0.08]) and +4.17 accommodations ([3.67, 4.62]). Residual high-infrastructure steps remain in about a quarter of constraint responses (for example app downloads or streaming despite a stated data limit).

**Lexicon validity.** Response-level flag (D_total > 0 vs manual > 0): precision 0.62, recall 0.66, kappa 0.15; Spearman between D counts and manual steps 0.45; between A counts and manual accommodations 0.85. The A lexicon is reliable; the D lexicon is weak. Generic dependence (apps, websites, cloud sheets, USD prices, online filing) is mostly missed, and some matches occur inside adapted advice.

## What the probes add
- Per-token sensitivity (T5c) gives the same ordering of groups (none 0.64, high 0.60, low 0.43, spec_loc 0.31, spec_only 0.31 on H mass).
- *Exploratory:* three probes (doctor, charge, refund) are saturated near 0 under the sum log-prob normalisation because short candidates such as "carry a power bank" dominate; their per-token values are non-degenerate (0.35 to 0.84). They should be treated as uninformative for the pre-registered measure.
- The power result rests on one probe and should be treated as a lead, not a finding.

## Limitations (in addition to those pre-registered)
- **No independent second annotation was done** (a 20-item instrument is provided: `audit/second_annotation_form.html`), so there is no inter-annotator agreement estimate; all audit conclusions rest on one annotator, who is not a resident of the studied places.
- The annotation is partly unblinded: responses naming Ouagadougou or restating constraints reveal the condition.
- The lexicon was refined once on the dev split (LEXICON_CHANGELOG.md) and then frozen; it still misses most generic dependence, and `power_D` is nearly empty.
- 61% of generations are truncated at 500 tokens (template B 100%, real prompts 92%, template A 7.5%); rates describe roughly the first 350 words.
- The runner did not record the model revision (`meta.json` has `revision: null`); each model's commit at check time is in its `model_revision_note.txt` (Qwen3-4B: cdbee75f, unchanged since 2025-09-17).
- Main analysis on a single model (replications cover the controlled scenarios only), English, one persona per place; hallucinated local institutions and apps appear in some responses and were not scored.
- Several probe candidate sets differ in length, which affects the pre-registered normalisation.

## Replication on three other models (controlled scenarios only, greedy; test split, n = 63 dependent scenarios)
Phi-4-mini-instruct (3.84B, MIT) and Qwen3-1.7B (1.72B) were run on Kaggle on 2026-10-20 with the same code and frozen lexicon; Llama-3.2-3B-Instruct has its own subsection below. For comparability the Qwen3-4B numbers below use its greedy runs only (they differ slightly from the main table, which averages greedy and sampled runs). Files: `results/*/tables_test_greedy.md`, `results/cross_model_test_greedy.md`. Holm correction is applied within each model's set of five contrasts, not across models.

| | Qwen3-4B | Phi-4-mini | Qwen3-1.7B |
|---|---|---|---|
| Default country probe, "United States" | 0.999 | 0.940 | 0.909 |
| Probe H mass: none / low / constraints-only | 0.72 / 0.53 / 0.36 | 0.70 / 0.60 / 0.49 | 0.71 / 0.54 / 0.51 |
| D rate: none / high / low / constraints-only | 0.84 / 1.05 / 0.62 / 0.55 | 0.53 / 0.63 / 0.58 / 0.62 | 0.63 / 0.77 / 0.74 / 1.28 |
| A rate: none / low / constraints-only | 0.18 / 0.49 / 2.61 | 0.20 / 0.27 / 1.66 | 0.24 / 0.34 / 1.47 |
| high - none (D), Holm p | +0.21 (0.008) | +0.10 (0.25) | +0.14 (0.033) |
| low - high (D), Holm p | -0.42 (< 0.0001) | -0.05 (0.25) | -0.03 (0.71) |
| spec_only - low (D), Holm p | -0.07 (0.78) | +0.04 (0.36) | +0.55 (< 0.0001) |

What replicates across the first three models (Llama-3.2-3B shows the same, see below):
- **The default world is the United States** (0.91 to 0.999 on the default-country probe) and next-token mass on high-infrastructure candidates is about 0.70 to 0.72 with no context. It falls with a lower-infrastructure place (0.53 to 0.60) and further with explicit constraints (0.36 to 0.51). The probe pattern is the most consistent result across models.
- **Telling a "high-income" city slightly increases high-infrastructure markers** relative to no context in all three (+0.10 to +0.21).
- **Explicit constraints produce many more adaptation markers** (6 to 14 times the no-context rate), while a place name alone produces a much weaker increase in the smaller models (1.4 times, versus 2.7 times for Qwen3-4B).

What does not replicate, and is model-dependent:
- **Only Qwen3-4B substitutes away from high-infrastructure services.** Its D rate falls from 0.84 (none) to 0.62 (low) to 0.55 (constraints). Phi-4-mini's D rate does not change (0.53 to 0.62), so its adaptation is additive. Qwen3-1.7B's D rate *rises* under constraints (0.63 to 1.28).
- *Exploratory, post hoc (12 matches read; confirmed by the manual audit below):* in Qwen3-1.7B constraint responses, payment markers often come from confusing mobile money with card wallets ("mobile money apps like PayPal, Apple Pay") and from advising "a stable internet connection for online payments" despite the stated constraints. This looks like a real failure of the small model, not only a lexicon artifact; the manual audit agrees (96% of its constraint responses contain at least one high-infrastructure step).
- *Exploratory sensitivity:* the lexicon counts the word "visa" as a payment-card marker, which inflates D in scenario G9 (visa application). Excluding G9 (`python src/analyze.py --tags <four models> --split test --greedy-only --exclude G9`; `results/cross_model_test_greedy_excl_G9.md`) leaves all directions and conclusions unchanged; the only threshold crossing is Qwen3-1.7B high - none, whose Holm p moves from 0.033 to 0.052 (Qwen3-1.7B low - none: 0.072 to 0.109).

### Fourth model: Llama-3.2-3B-Instruct (official Meta weights via Kaggle Models; same design, greedy, test split, n = 63)
Run after the first three replications (68 minutes of run time), with the same frozen lexicon. Files: `results/Llama-3.2-3B-Instruct/`. Lexical and probe results first; a manual audit (48 responses) follows below.

| | Llama-3.2-3B |
|---|---|
| Default country probe, "United States" | 0.972 |
| Probe H mass: none / low / constraints-only | 0.67 / 0.52 / 0.39 |
| D rate: none / high / low / constraints-only | 0.54 / 0.75 / 0.63 / 0.57 |
| A rate: none / low / constraints-only | 0.15 / 0.32 / 1.45 |
| high - none (D), Holm p | +0.21 (0.0014) |
| low - high (D), Holm p | -0.11 (0.14) |
| spec_only - low (D), Holm p | -0.06 (0.29) |

Llama behaves like Phi-4-mini on these measures: the United States default, the probe pattern (none, then low, then constraints) and the rise in adaptation markers under explicit constraints replicate, but the D rate does not fall under constraints (0.54 with no context, 0.57 with constraints only). On the lexical evidence its adaptation is additive, as for the two smaller models; the manual audit below supports this. Truncation: 44% overall (template A 0.7%, template B 87%).

### Blind audit of the replication models (144 responses: 48 per model; exploratory; single annotator, partly blind to condition)
Same rubric as the main audit, same 24 test scenarios, conditions no-context and constraints-only (template A, greedy). Files: `audit/audit_rep_*.csv`, `results/replication_audit_stats.md`.

| model | high-infrastructure steps: none -> constraints | share of responses with at least one: none -> constraints | accommodations: none -> constraints |
|---|---|---|---|
| Qwen3-4B | 2.46 -> 0.38 (-2.08, CI [-2.79, -1.42]) | 0.83 -> 0.29 | 0.04 -> 4.58 |
| Phi-4-mini | 1.62 -> 1.25 (-0.38, CI [-0.92, 0.17]) | 0.79 -> 0.67 | 0.00 -> 3.33 |
| Qwen3-1.7B | 1.46 -> 1.92 (+0.46, CI [-0.21, 1.17]) | 0.71 -> 0.96 | 0.04 -> 1.75 |
| Llama-3.2-3B | 1.33 -> 1.08 (-0.25, CI [-0.88, 0.33]) | 0.62 -> 0.71 | 0.00 -> 2.38 |

This **confirms by manual coding** the pattern seen lexically: given explicit constraints, all four models add accommodations (offline use, mobile money, power planning), but only Qwen3-4B removes reliance on high-infrastructure services. Phi-4-mini keeps most of its high-infrastructure steps (adaptation is additive), Llama-3.2-3B behaves the same way (1.33 steps with no context, 1.08 with constraints; 71% of constraint responses still contain at least one), and Qwen3-1.7B ends with at least one such step in 96% of constraint responses (for example Zoom or stable internet advised "with limited resources", Google Pay and Apple Pay proposed to someone without a card, app downloads despite slow data). The confidence intervals for the three smaller models include zero (n = 24), so the claim is about the contrast with Qwen3-4B, not about a measured increase for Qwen3-1.7B.

Lexicon validity on these models is no better than on Qwen3-4B for dependence (kappa 0.01 for Phi-4-mini, 0.17 for Qwen3-1.7B, 0.33 for Llama-3.2-3B; D-count correlation 0.11, 0.37 and 0.43) but good for adaptation (correlation 0.85, 0.75 and 0.85). The lexical A rate is therefore trustworthy across models; the lexical D rate is a weak indicator.

Caveats specific to the replication: the same annotator coded all four models, so systematic coding drift cannot be ruled out; real prompts and sampled runs were not run for the replication models; truncation differs by model (Phi-4-mini 34%, Qwen3-1.7B 50%, Qwen3-4B 52% greedy, Llama-3.2-3B 44%).

## Not done yet
- Independent second annotation of 20 audit items (`audit/second_annotation_form.html`): not done, so there is no inter-annotator agreement estimate.
- Length-matched next-token probes (three of the 20 are degenerate under the pre-registered normalisation).
- A larger and independently coded audit, real-prompt and sampled runs for the replication models, and a better measure of high-infrastructure dependence than the lexicon.
