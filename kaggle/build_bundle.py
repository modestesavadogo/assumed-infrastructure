"""Builds kaggle/run_all.py: ONE self-contained script (data + code) so the Kaggle kernel needs no dataset upload.

IAB_MODEL=Qwen/Qwen3-4B-Instruct-2507 KAGGLE_OWNER=<user> python kaggle/build_bundle.py
Optional: IAB_SETS=s1 (controlled scenarios only, for replication models), IAB_BATCH=24
"""
import base64, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["data/scenarios.csv", "data/contexts.json", "data/probes.json", "data/real_prompts.csv", "src/run_experiment.py"]
MODEL = os.environ.get("IAB_MODEL", "Qwen/Qwen3-4B-Instruct-2507")
SETS = os.environ.get("IAB_SETS", "s1,s2")
BATCH = os.environ.get("IAB_BATCH", "24")
SAMPLES = os.environ.get("IAB_SAMPLES", "1")          # 0 = greedy only
OUTDIR = os.environ.get("IAB_OUTDIR", "kaggle")       # one folder per kernel
OWNER = os.environ.get("KAGGLE_OWNER", "REPLACE_WITH_KAGGLE_USERNAME")
MODEL_SOURCE = os.environ.get("IAB_MODEL_SOURCE", "")    # e.g. metaresearch/llama-3.2/transformers/3b-instruct/1 (Kaggle Models; no HF token needed)
MODEL_MATCH = os.environ.get("IAB_MODEL_MATCH", "")      # substring identifying the model folder under /kaggle/input
TAG = os.environ.get("IAB_TAG", "")
short = TAG or MODEL.split("/")[-1]
SLUG = "iab-" + re.sub(r"[^a-z0-9]+", "-", short.lower()).strip("-")

blob = {f: open(os.path.join(ROOT, f), encoding="utf-8").read() for f in FILES}
script = f'''import json, os, subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-U", "transformers", "accelerate"])
BLOB = json.loads(__import__('base64').b64decode('{base64.b64encode(json.dumps(blob).encode()).decode()}').decode())
for path, text in BLOB.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
os.environ["IAB_OUT"] = "/kaggle/working/results"
import torch
print("cuda:", torch.cuda.is_available(), torch.cuda.device_count(), flush=True)
assert torch.cuda.is_available(), "GPU not available: aborting before loading the model"
MODEL = "{MODEL}"
MATCH = "{MODEL_MATCH}"
if MATCH:
    import glob
    found = sorted(os.path.dirname(p) for p in glob.glob("/kaggle/input/**/config.json", recursive=True) if MATCH in p.lower())
    print("model folders found:", found, flush=True)
    assert found, "model source not attached or license not accepted: aborting before any generation"
    MODEL = found[0]
cmd = [sys.executable, "src/run_experiment.py", "--model", MODEL, "--tag", "{short}", "--sets", "{SETS}",
       "--samples", "{SAMPLES}", "--batch", "{BATCH}", "--dtype", "fp16"]
print(" ".join(cmd), flush=True)
sys.exit(subprocess.call(cmd))
'''
os.makedirs(os.path.join(ROOT, OUTDIR), exist_ok=True)
open(os.path.join(ROOT, OUTDIR, "run_all.py"), "w", encoding="utf-8").write(script)
meta = {"id": f"{OWNER}/{SLUG}", "title": f"IAB {short}", "code_file": "run_all.py", "language": "python",
        "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True,
        "dataset_sources": [], "competition_sources": [], "kernel_sources": []}
if MODEL_SOURCE:
    meta["model_sources"] = [MODEL_SOURCE]
json.dump(meta, open(os.path.join(ROOT, OUTDIR, "kernel-metadata.json"), "w"), indent=2)
print("built", len(script), "bytes; kernel id", meta["id"])
