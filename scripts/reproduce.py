"""One-command reproduction of every number and figure in RESULTS.md from the released model outputs (CPU only).

python scripts/reproduce.py        (run from the repository root, with results/ and audit/ in place)

Steps: (1) lexicon and statistics unit tests, (2) scripts/verify_release.py (input hashes, counts, frozen analysis vs shipped tables including
bootstrap CIs, probe and audit headline numbers), (3) figure data regenerated and compared with the shipped figure data.
Exit status 0 only if everything matches. Nothing in results/ is modified; figures/ is rewritten with identical content.
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.getcwd()
ok = True


def run(title, args):
    global ok
    print(f"\n=== {title}", flush=True)
    r = subprocess.run([sys.executable, *args], cwd=ROOT)
    if r.returncode != 0:
        ok = False
        print(f"FAILED: {title}")


def sha(path):
    return hashlib.sha256(open(path, "rb").read().replace(b"\r\n", b"\n")).hexdigest()


run("1a. lexicon unit tests", ["tests/test_coding.py"])
run("1b. statistics unit tests", ["tests/test_stats.py"])
run("2. verify inputs, counts and frozen analysis", ["scripts/verify_release.py"])

fig_data = sorted(f for f in os.listdir("figures") if f.endswith("_data.csv")) if os.path.isdir("figures") else []
before = {f: sha(f"figures/{f}") for f in fig_data}
run("3. regenerate figures", ["scripts/make_figures.py"])
for f in fig_data:
    same = sha(f"figures/{f}") == before[f]
    print(("PASS  " if same else "FAIL  ") + f"figure data unchanged: {f}")
    ok &= same

print("\nREPRODUCED: all checks passed" if ok else "\nNOT REPRODUCED: see failures above")
sys.exit(0 if ok else 1)
