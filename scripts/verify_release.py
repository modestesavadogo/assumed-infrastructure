"""Verify a checkout: inputs match the recorded hashes, output counts are complete, and the frozen analysis re-computes the shipped numbers.

python scripts/verify_release.py        (run from the repository root, with results/ and audit/ in place)
The analysis runs on a temporary copy, so nothing in results/ is modified. Means, effect sizes, p-values and bootstrap
confidence intervals are all compared (the bootstrap uses a fixed seed per call, see src/analyze.py: boot_ci).
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
import numpy as np
import pandas as pd

ROOT = os.getcwd()
MODELS = ["Qwen3-4B-Instruct-2507", "Phi-4-mini-instruct", "Qwen3-1.7B", "Llama-3.2-3B-Instruct"]
EXPECTED_GEN = {"Qwen3-4B-Instruct-2507": 5896, "Phi-4-mini-instruct": 2400, "Qwen3-1.7B": 2400, "Llama-3.2-3B-Instruct": 2400}
checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + (f"  [{detail}]" if detail else ""), flush=True)


# 1. files present
missing = [f"results/{m}/{f}" for m in MODELS for f in ("generations.jsonl", "probes.jsonl", "meta.json") if not os.path.exists(f"results/{m}/{f}")]
if missing:
    print("Missing files (download the Hugging Face dataset into this folder, see docs/REPRODUCE.md):", *missing[:6], sep="\n  ")
    sys.exit(2)

# 2. input hashes recorded in meta.json (line endings normalised)
for fn in ["scenarios.csv", "contexts.json", "probes.json"]:
    h = hashlib.sha256(open(f"data/{fn}", "rb").read().replace(b"\r\n", b"\n")).hexdigest()[:12]
    for m in MODELS:
        rec = json.load(open(f"results/{m}/meta.json"))["data_hash"][fn]
        check(f"input hash {fn} == meta.json of {m}", rec == h, f"{h} vs {rec}")

# 3. counts
probes = json.load(open("data/probes.json"))
exp_probe_rows = sum(len(p["cands"]) for p in probes["context_probes"]) * 10 + len(probes["default_world_probe"]["cands"])
for m in MODELS:
    g = pd.read_json(f"results/{m}/generations.jsonl", lines=True); p = pd.read_json(f"results/{m}/probes.jsonl", lines=True)
    check(f"{m}: generations count", len(g) == EXPECTED_GEN[m], f"{len(g)}")
    check(f"{m}: no duplicate (set, scenario, condition, template, run)", not g.duplicated(["set", "scenario_id", "condition", "template", "run"]).any())
    check(f"{m}: probe rows", len(p) == exp_probe_rows, f"{len(p)}")

# 4. lexicon unit tests
r = subprocess.run([sys.executable, "tests/test_coding.py"], capture_output=True, text=True)
check("lexicon unit tests", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-120:])

# 5. recompute the frozen analysis on a temporary copy and compare with the shipped cross-model table
tmp = tempfile.mkdtemp(prefix="iab_verify_")
for m in MODELS:
    os.makedirs(f"{tmp}/{m}")
    for f in ("generations.jsonl", "probes.jsonl", "meta.json"):
        shutil.copy(f"results/{m}/{f}", f"{tmp}/{m}/{f}")
os.environ["IAB_OUT"] = tmp
sys.path.insert(0, "src")
import analyze  # noqa: E402  (reads IAB_OUT at import)
new = pd.concat([analyze.report_one(m, "test", True)[1] for m in MODELS])
ref_path = next((p for p in ("results_summary/cross_model_test_greedy.md", "results/cross_model_test_greedy.md") if os.path.exists(p)), None)
if ref_path is None:
    check("shipped cross-model table found", False, "results_summary/ or results/ cross_model_test_greedy.md")
else:
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in open(ref_path, encoding="utf-8") if ln.startswith("|")]
    hdr, body = rows[0], [r for r in rows[2:]]
    ref = pd.DataFrame(body, columns=hdr)
    for c in ("n", "mean_diff_D", "dz", "p_raw", "p_holm"):
        ref[c] = pd.to_numeric(ref[c])
    ref["ci"] = ref["ci"].astype(str)
    mm = new.merge(ref, on=["model", "contrast"], suffixes=("_new", "_ref"))
    check("cross-model contrasts: bootstrap 95% CIs reproduced exactly", (mm["ci_new"] == mm["ci_ref"]).all(), f"{int((mm['ci_new'] != mm['ci_ref']).sum())} differ")
    check("cross-model contrasts: all 20 rows matched", len(mm) == 20, f"{len(mm)} matched")
    for c, tol in (("mean_diff_D", 1e-3), ("dz", 1e-3), ("p_raw", 1e-3), ("p_holm", 1e-3)):
        d = float(np.abs(mm[f"{c}_new"] - mm[f"{c}_ref"]).max())
        check(f"cross-model contrasts: {c} reproduced", d < tol, f"max abs diff {d:.5f}")

# 6. default-country probe and group probe mass (headline numbers)
exp_us = {"Qwen3-4B-Instruct-2507": 0.999, "Phi-4-mini-instruct": 0.940, "Qwen3-1.7B": 0.909, "Llama-3.2-3B-Instruct": 0.972}
for m in MODELS:
    p = pd.read_json(f"results/{m}/probes.jsonl", lines=True)
    d = p[p.probe == "PR0_default_country"].copy()
    d["pr"] = np.exp(d.logp - d.logp.max()) / np.exp(d.logp - d.logp.max()).sum()
    us = float(d[d.cand.str.strip() == "the United States"].pr.iloc[0])
    check(f"{m}: default-country probe 'United States'", abs(us - exp_us[m]) < 0.0015, f"{us:.3f}")

# 7. audit means against the shipped figure data
if os.path.exists("figures/fig_audit_data.csv"):
    k4 = pd.read_csv("audit/audit_key.csv"); c4 = pd.read_csv("audit/audit_coded.csv").merge(k4, on="audit_id").assign(model="Qwen3-4B-Instruct-2507")
    cr = pd.read_csv("audit/audit_rep_coded.csv").merge(pd.read_csv("audit/audit_rep_key.csv"), on="audit_id")
    cl = pd.read_csv("audit/audit_llama_coded.csv").merge(pd.read_csv("audit/audit_llama_key.csv"), on="audit_id")
    allc = pd.concat([c4, cr, cl], ignore_index=True)
    ref = pd.read_csv("figures/fig_audit_data.csv"); short = {"Qwen3-4B-Instruct-2507": "Qwen3-4B", "Phi-4-mini-instruct": "Phi-4-mini", "Llama-3.2-3B-Instruct": "Llama-3.2-3B", "Qwen3-1.7B": "Qwen3-1.7B"}
    worst = 0.0
    for r_ in ref.itertuples():
        cond = "C00_none" if r_.condition == "no context" else "C09_constraints_only"
        mdl = [k for k, v in short.items() if v == r_.model][0]
        v = allc[(allc.model == mdl) & (allc.condition == cond)].groupby("scenario_id")[r_.measure].mean().mean()
        worst = max(worst, abs(v - r_.mean))
    check("audit means reproduced (16 cells)", worst < 1e-3, f"max abs diff {worst:.5f}")

shutil.rmtree(tmp, ignore_errors=True)
bad = [c for c in checks if not c[1]]
print(f"\n{len(checks) - len(bad)} / {len(checks)} checks passed")
sys.exit(1 if bad else 0)
