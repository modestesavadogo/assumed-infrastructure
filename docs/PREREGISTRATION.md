# Pre-registration v2: assumed-infrastructure bias in instruct LLMs

*v1 (commit 24e859c) was a 40-scenario, one-template pilot design. Before any real model output existed, the design was expanded to v2 for representativeness and validity (this file). Only a 0.6B debugging smoke test and synthetic data have been run; neither informed any design decision beyond fixing bugs.*

## Question
When asked for practical help, does an instruction-tuned LLM silently assume a high-infrastructure setting (reliable electricity, fast always-on internet, international cards, cloud services, cars and delivery), and how deeply does it adapt when told where the user lives or what the constraints are?

## Models
Primary: `Qwen/Qwen3-4B-Instruct-2507` (4.02B, Apache-2.0), fp16, non-thinking. Replication (controlled scenarios only, same code): `microsoft/Phi-4-mini-instruct` (3.84B, MIT) and `Qwen/Qwen3-1.7B` (size trend); `meta-llama/Llama-3.2-3B-Instruct` if gated access is available. Replication results are reported alongside, never substituted.

## Materials (frozen in `data/`; SHA-256 prefixes recorded in each `meta.json`)
- **S1, controlled scenarios (120):** 90 infrastructure-dependent (9 domains x 10: learning, tech, money, business, logistics, health, mobility, shopping, communication) and 30 independent controls (3 domains x 10: wellbeing, people, home). **Dev split** = items 1-3 of each domain (36); **test split** = items 4-10 (84: 63 dependent, 21 control).
- **S2, real user prompts:** all 274 English initial prompts of OpenAssistant/oasst1 (Apache-2.0) passing a fixed filter (`src/make_real_prompts.py`: practical help-seeking intent, 60-500 characters, no code/creative/role-play, no place names). `dependent_heuristic` is a keyword flag on the prompt only.
- **Conditions (10):** C00 none; C01 Boston, C02 Paris, C03 Seoul (group *high*); C04 Ouagadougou, C05 rural Burkina Faso, C06 Lagos, C07 Dhaka (group *low*); C08 Ouagadougou plus explicit constraints (*spec_loc*); C09 the same constraints with no location (*spec_only*). The constraint profile is a persona defined by the study, not a claim about a real city.
- **Templates (S1):** A "Give me a concrete step-by-step plan in under 300 words." B "How should I go about this? Keep it practical." S2 prompts are used as written. S2 is run under C00, C01, C04, C09.
- **Decoding:** greedy; S1 additionally one sampled run (T=0.7, top-p 0.8, top-k 20, fixed seed). Max 500 new tokens; truncation rate reported.
- **Probes (21):** next-token candidate sets fixed in advance (`data/probes.json`): 20 context probes (payment, power, connectivity, transport, shopping, finance, administration, health, backup, study, remittance, jobs, skills, files, lookup, team contact, refunds) under all 10 conditions, plus a default-country probe. Candidate groups H (high-infrastructure default), L (adapted), N (neutral).

## Measures
- **D rate / A rate:** lexicon matches per 100 words (`src/coding.py`): D = reliance on high-infrastructure services, A = adaptation markers; **adaptation ratio** A/(A+D); **disclaimer rate**; **context-mention rate** (controls).
- **Probe mass** on H/L/N after renormalising over candidates (sum log-prob primary; per-token as sensitivity).
- **Blind manual audit (validity):** 120 responses (24 test scenarios x conditions C00, C01, C04, C08, C09; greedy, template A), shuffled, condition hidden from the annotator. Coded for: number of steps relying on high-infrastructure services, number of explicit accommodations, generic-disclaimer-only (0/1). One annotator; a 20-item independent second annotation is provided as an instrument (`audit/second_annotation_form.html`). Reported: lexicon-vs-manual precision, recall, Cohen's kappa, Spearman correlations.

## Lexicon freeze protocol
1. Generate all outputs. 2. Inspect and analyse **only the dev split** (S1); refine the lexicon if it misses or mislabels markers, each change committed with its reason. 3. Tag the commit `lexicon-frozen`. 4. Run the test-split analysis once. Changes after step 3 are not allowed; any later analysis is labelled exploratory.

## Hypotheses (all on S1 test split, dependent scenarios, unit = scenario, n = 63)
- **H1 default world:** C00 resembles *high*: D rate(high) - D rate(none) is small (|dz| < 0.2) and the adaptation ratio of *none* is below that of *low*.
- **H2 shallow adaptation:** *low* has more A markers and more generic disclaimers than *none*, but D rate(low) stays above zero and above D rate(spec_loc).
- **H3 inference gap:** D rate(spec_only) < D rate(low): the model plans under stated constraints but does not infer them from the place.
- **H4 spurious injection (controls):** context-mention rate in controls is higher under *low* than under *none* while D markers stay near zero.
- **H5 probes:** under C00 the mean H mass exceeds 0.5; *low* shifts mass towards L but not fully; *spec_only* shifts more than *low*.
- **H6 heterogeneity:** *low* places differ from each other (reported per place); no direction predicted.

## Analysis plan
- Bootstrap 95% CIs over scenarios (10,000 resamples). **Primary paired contrasts on D rate, Holm-corrected over the set:** high - none, low - none, low - high, spec_loc - low, spec_only - low (Wilcoxon signed-rank; effect size dz). With n = 63, a paired effect of about dz = 0.36 is detectable at 80% power before correction.
- Robustness: the same contrasts per template; per-place table; truncation rate; sampled vs greedy.
- S2 (real prompts), probes, controls and the audit are reported descriptively or as exploratory contrasts; replication models report the primary contrasts only.
- Null and reversed results are reported as such. No scenario, condition, template or lexicon entry is changed after the freeze.

## Scope and known limitations
Representative of: this sample of practical-advice prompts (systematic scenarios plus a documented real-prompt pool), these 10 location/constraint contexts, English, and the models tested. Not representative of all LLMs, all users, other languages, or real deployments. Small instruct models are not frontier models. Lexicon coding is coarse (hence the audit); the audit has a single annotator who is not a resident of the places studied; the persona constraints are operational assumptions; oasst1 volunteers skew towards technical, English-speaking users; one prompt template family; two decoding settings.

## Addendum (2026-10-20, before any output was analysed)
One reviewer judged the persona constraints in conditions C08 and C09 realistic for Ouagadougou (a single reviewer; not a systematic validation). No change was made to `data/contexts.json`.

## Addendum (2026-10-20): Llama-3.2-3B-Instruct replication setup
Prepared before any Llama output exists. The Llama 3.x chat template injects today's date; the runner now passes a fixed `date_string="26 Jul 2024"` (templates that do not use it ignore it; the rendered prompts of Qwen3-4B, Qwen3-1.7B and Phi-4-mini were verified identical before and after this change). Llama tokenizers have no pad token, so the runner sets pad = eos (left padding with attention masks; no effect on the content). The model is read from Kaggle Models (`metaresearch/llama-3.2`, Transformers, 3b-instruct) so no Hugging Face token is needed; it requires acceptance of Meta's license on Kaggle by the account used to run the kernel. Same design as the other replications: controlled scenarios only, greedy, frozen lexicon.

## Document history
Terminology edits (neutral annotator wording; renamed second-annotation files). Design, hypotheses, measures, freeze protocol and analysis plan are unchanged since v2.

Changes made after the test-split analysis, none of which alters a pre-registered choice:
- The bootstrap uses a fresh generator seeded with 0 for every interval (previously one generator shared across calls), so intervals no longer depend on call order. Point estimates, effect sizes and p-values are unchanged; some interval bounds moved by at most 0.05 and the reported values were updated.
- Exploratory sensitivity analysis excluding scenario G9 (`--exclude G9`), added because the word "visa" is a lexicon payment marker.
- Pinned source revision and file hash for `src/make_real_prompts.py`; the rebuilt `data/real_prompts.csv` is identical in content.
