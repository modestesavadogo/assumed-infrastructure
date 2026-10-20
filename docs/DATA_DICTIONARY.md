# Data dictionary

Paths are relative to the repository root. Files under `results/` and the large audit files live in the Hugging Face dataset; `data/`, `audit/` and `results_summary/` are also in the GitHub repository.

## Study inputs (`data/`)

### `data/scenarios.csv` (120 rows)
| column | type | meaning |
|---|---|---|
| `id` | string | scenario id: domain letter + number 1-10 (e.g. `L3`, `W7`). Numbers 1-3 form the development split, 4-10 the test split. |
| `group` | string | domain: learning, tech, money, business, logistics, health, mobility, shopping, communication (dependent) or wellbeing, people, home (controls) |
| `dependent` | 0/1 | 1 = outcome plausibly depends on infrastructure; 0 = infrastructure-independent control |
| `text` | string | the first-person request, without any location |

### `data/contexts.json`
Keys `C00_none` ... `C09_constraints_only`: the one-sentence context prepended to each request (empty string for `C00`). Groups used in the analysis: *none* = C00; *high* = C01-C03 (Boston, Paris, Seoul); *low* = C04-C07 (Ouagadougou, rural Burkina Faso, Lagos, Dhaka); *spec_loc* = C08; *spec_only* = C09. `_note` states that C08/C09 are an operational persona.

### `data/probes.json`
`context_probes`: 20 probes, each with `id`, `user` (the question), `prefix` (assistant text already written) and `cands` (list of `[continuation, group]`, group H = high-infrastructure default, L = adapted, N = neutral). `default_world_probe`: the "which country do I live in" probe (`PR0_default_country`), run with no context.

### `data/real_prompts.csv` (274 rows)
| column | meaning |
|---|---|
| `id` | `R001`-`R274` |
| `message_id` | OpenAssistant (oasst1) message id |
| `text` | the user prompt, unchanged |
| `dependent_heuristic` | 1 if a fixed keyword list matches the prompt (prompt only, never model output); used for exploratory splits |

## Model outputs (`results/<model>/`, Hugging Face)

### `generations.jsonl` (one JSON object per line)
| field | meaning |
|---|---|
| `set` | `s1` controlled scenarios, `s2` real prompts (main model only) |
| `scenario_id` | scenario id (`s1`) or `R...` id (`s2`) |
| `group`, `dependent`, `split` | domain, dependence flag, `dev`/`test` (all `s2` rows are `test`) |
| `condition` | `C00_none` ... `C09_constraints_only` |
| `template` | `A` (step-by-step plan, under 300 words), `B` (practical, no length instruction), `R` (real prompt as written) |
| `prompt` | the exact user message (context sentence + request + template suffix) |
| `run` | `greedy` or `sample1` (temperature 0.7, top-p 0.8, top-k 20; seed 1000 + batch offset, so the sample depends on batch size and order; main model only) |
| `response` | the model's text (special tokens stripped) |
| `n_new_tokens` | generated tokens before the stop token or the 500-token cap |
| `truncated` | 1 if the 500-token cap was hit before a stop token |

Counts: Qwen3-4B-Instruct-2507 5,896 (2,400 greedy + 2,400 sampled on `s1`, 1,096 greedy on `s2`); Phi-4-mini-instruct, Llama-3.2-3B-Instruct and Qwen3-1.7B 2,400 each (`s1`, greedy).

### `probes.jsonl` (938 rows per model)
`probe` (probe id), `condition`, `cand` (candidate continuation), `group` (H/L/N), `logp` (sum of token log-probabilities of the candidate given the chat prompt and prefix), `n_tok` (candidate token count), `boundary_shift` (1 if tokenisation of the prefix changed when the candidate was appended; 0 throughout). Within each (`probe`, `condition`) the candidate probabilities are renormalised with a softmax over `logp` (pre-registered); a per-token variant is reported as sensitivity.

### `meta.json`
`model`, `revision` (null when not recorded; see `model_revision_note.txt`), `args` (run arguments), `torch`, `transformers`, `platform`, `cuda`, `n_items`, `data_hash` (first 12 hex characters of SHA-256 of the line-ending-normalised input files), `date`, `seconds`.

## Audit (`audit/`)

The blind audit coded responses for two quantities (rubric in `audit/RUBRIC.md`): `n_high_infra_steps` (steps that rely on high-infrastructure services without an alternative in the same step) and `n_accommodations` (explicit accommodations to low-infrastructure conditions). `generic_disclaimer_only(0/1)` was recorded but is 0 for every response and is not used.

| file | rows | meaning |
|---|---|---|
| `audit_blind.csv` | 120 | main audit: id and response as shown to the annotator (condition hidden); code columns are empty |
| `audit_key.csv` | 120 | `audit_id` -> `scenario_id`, `condition` (kept apart from the coding view) |
| `manual_codes.csv` | 120 | the codes: `audit_id`, `n_high_infra_steps`, `n_accommodations`, `generic_disclaimer_only(0/1)`, `note` |
| `audit_coded.csv` | 120 | blind responses merged with the codes |
| `audit_rep_*.csv` | 96 each | same four files for Phi-4-mini-instruct and Qwen3-1.7B (`audit_rep_key.csv` also has `model`) |
| `audit_llama_*.csv`, `manual_codes_llama.csv` | 48 | same for Llama-3.2-3B-Instruct |
| `second_annotation_sample.csv`, `second_annotation_form.html` | 20 | instrument for an independent second annotation of 20 responses (form generated by `scripts/make_annotation_form.py`); **not completed** |

Main audit: 24 test scenarios x conditions C00, C01, C04, C08, C09 (greedy, template A). Replication audits: the same 24 scenarios x C00 and C09 per model. Annotation: single annotator.

## Derived summary files (`results_summary/` on GitHub; `results/*.md` and per-model tables on Hugging Face)
`tables_test*.md` (all pre-registered tables), `cross_model_test_greedy.md` (primary contrasts per model), `cross_model_test_greedy_excl_G9.md` (sensitivity: same contrasts without scenario G9), `audit_stats.md`, `audit_eval.md`, `replication_audit_stats.md`, per-model figures, and `figures/fig_*_data.csv` (the numbers behind the two cross-model figures).

## Redactions in the released copies
E-mail-like strings inside model responses (hallucinated or placeholder addresses of the form `name@organisation.tld`; 24 occurrences in `generations.jsonl` and the audit response files) are replaced by `[email redacted]` because some could coincide with real contacts. No other text was altered. `scripts/verify_release.py` recomputes every reported number from the redacted files and they match.
