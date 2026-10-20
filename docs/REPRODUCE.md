# Reproducing the analysis

## 0. Get the files
```bash
git clone https://github.com/modestesavadogo/assumed-infrastructure.git && cd assumed-infrastructure
# download the Hugging Face dataset into this folder so that results/ and audit/ exist:
hf download SavadogoModeste/assumed-infrastructure-audit --repo-type dataset --local-dir .
pip install -r requirements.txt
```
(Without the Hugging Face files you still have the inputs in `data/`, the rubric, the codes in `audit/` and all summary tables.)

## 1. Check the release (CPU, a few minutes)
```bash
python scripts/reproduce.py          # everything below in one command; exit status 0 only if all checks pass
python tests/test_coding.py          # lexicon unit tests
python tests/test_stats.py           # bootstrap / Holm unit tests
python scripts/verify_release.py     # re-runs the frozen analysis and compares means, dz, p-values and bootstrap CIs with the shipped tables
```
Tested environment: Python 3.13, numpy 2.2, pandas 2.2, scipy 1.15, matplotlib 3.11 (`requirements.txt` gives the tested pins).

## 2. Re-run the analysis by hand
```bash
# primary contrasts and tables, four models, greedy runs only (comparable across models)
python src/analyze.py --tags Qwen3-4B-Instruct-2507,Phi-4-mini-instruct,Qwen3-1.7B,Llama-3.2-3B-Instruct --split test --greedy-only
# main model, greedy + sampled runs
python src/analyze.py --tags Qwen3-4B-Instruct-2507 --split test
# development split (what the lexicon was refined on)
python src/analyze.py --tags Qwen3-4B-Instruct-2507 --split dev
# sensitivity: drop scenario G9 (the word "visa" is a lexicon payment marker)
python src/analyze.py --tags Qwen3-4B-Instruct-2507,Phi-4-mini-instruct,Qwen3-1.7B,Llama-3.2-3B-Instruct --split test --greedy-only --exclude G9
# audit statistics
python src/analyze.py --tags Qwen3-4B-Instruct-2507 --audit-eval audit/audit_coded.csv
python src/audit_stats.py
python src/audit_rep_stats.py
python scripts/make_figures.py
```
Expected values to compare (Qwen3-4B, greedy only, test split, D rate contrasts, n = 63): high - none +0.2116 (Holm p 0.0082); low - high -0.4239; default-country probe 0.999; audit high-infrastructure steps 2.46 -> 0.38. Tables are written to `results/<model>/tables_test*.md` and `results/cross_model_test_greedy.md`.

Note: running `analyze.py` rewrites the `coded_generations*.csv` and table files in `results/<model>/`.

## 3. Regenerate the model outputs (GPU)
Prompts, contexts and probes are in `data/`; `src/run_experiment.py` does generation and probes:
```bash
python src/run_experiment.py --model Qwen/Qwen3-4B-Instruct-2507 --batch 24 --dtype fp16
python src/run_experiment.py --model microsoft/Phi-4-mini-instruct --sets s1 --samples 0 --batch 24 --dtype fp16
python src/run_experiment.py --model Qwen/Qwen3-1.7B --sets s1 --samples 0 --batch 32 --dtype fp16
# Llama needs accepted license: --model <local path or meta-llama/Llama-3.2-3B-Instruct> --tag Llama-3.2-3B-Instruct --sets s1 --samples 0
```
`kaggle/build_bundle.py` packs data and runner into one script for a Kaggle kernel (set `KAGGLE_OWNER`, `IAB_MODEL`, optionally `IAB_SETS`, `IAB_SAMPLES`, `IAB_BATCH`, `IAB_MODEL_SOURCE`, `IAB_MODEL_MATCH`, `IAB_TAG`). Runs used two T4 GPUs, transformers 5.20.2, torch 2.11.0+cu128; times are in each `meta.json`. Greedy decoding is deterministic only up to hardware and library versions, so expect small differences in individual responses.

## 4. What is and is not deterministic
- Analysis from the released outputs is deterministic: the lexicon is fixed, the Wilcoxon test and Holm correction are exact functions of the data, and each bootstrap interval uses its own generator seeded with 0 (`boot_ci` in `src/analyze.py`), so intervals do not depend on call order.
- Regenerating model outputs is deterministic only up to hardware and library versions (GPU kernels, fp16 accumulation, `transformers`/`torch` releases). The sampled run of the main model is seeded per batch (1000 + batch offset), so it also depends on the batch size and prompt order used (`--batch 24`). Expect small differences in individual responses and therefore in the last digits of the tables; the shipped outputs are the reference.
- `data/real_prompts.csv` is rebuilt from a pinned source: `python src/make_real_prompts.py <output.csv>` stops if the oasst1 file differs from the recorded SHA-256 and writes the same content as the shipped file.
- Model weights are identified by commit revision (listed in the README); the Llama weights come from Kaggle Models and cannot be pinned by hash here.
- Released files are LF-normalised and listed in `MANIFEST.sha256`; check a checkout with `python scripts/verify_manifest.py MANIFEST.sha256` (tolerates CRLF conversion of text files).

## 5. Second annotation (optional)
To estimate inter-annotator agreement, a second annotator opens `audit/second_annotation_form.html` (20 responses, rubric in `audit/RUBRIC.md`), exports `second_annotation_coded.csv` into `audit/`, and runs `python src/second_annotation_agreement.py`. The form is regenerated from `audit/second_annotation_sample.csv` by `python scripts/make_annotation_form.py`.

## 6. Notes on the runner
- Chat templates are applied with thinking disabled where supported; the Llama template date is pinned (`date_string="26 Jul 2024"`), which leaves the other templates' prompts unchanged.
- Llama tokenizers have no pad token: the runner uses the end token for padding (left padding with attention masks).
- Input files are hashed after normalising line endings (`meta.json` -> `data_hash`).
