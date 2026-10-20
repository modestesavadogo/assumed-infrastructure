"""Agreement between a second annotation (audit/second_annotation_coded.csv) and the primary manual codes (audit/manual_codes.csv).

python src/second_annotation_agreement.py [path/to/second_annotation_coded.csv]
Writes audit/second_annotation_agreement.md. The second annotation file must have: audit_id, n_high_infra_steps, n_accommodations (note optional).
"""
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

path = sys.argv[1] if len(sys.argv) > 1 else "audit/second_annotation_coded.csv"
second = pd.read_csv(path, encoding="utf-8-sig")
if "note" not in second.columns:
    second["note"] = ""
primary = pd.read_csv("audit/manual_codes.csv")[["audit_id", "n_high_infra_steps", "n_accommodations", "note"]]
m = second.merge(primary, on="audit_id", suffixes=("_2", "_1"))
for c in ["n_high_infra_steps_2", "n_accommodations_2"]:
    m[c] = pd.to_numeric(m[c], errors="coerce")
m = m.dropna(subset=["n_high_infra_steps_2", "n_accommodations_2"]).reset_index(drop=True)
n = len(m)
assert n > 0, "no complete rows found"


def kappa(a, b):
    a, b = np.asarray(a, int), np.asarray(b, int)
    po = (a == b).mean(); pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def block(name, y, a):
    d = y - a
    rho = spearmanr(y, a).correlation if np.std(y) > 0 and np.std(a) > 0 else float("nan")
    return (f"| {name} | {(d == 0).mean():.2f} | {(np.abs(d) <= 1).mean():.2f} | {np.abs(d).mean():.2f} | {d.mean():+.2f} | {rho:.2f} |")


rows = [block("high-infrastructure steps", m.n_high_infra_steps_2.values, m.n_high_infra_steps_1.values),
        block("accommodations", m.n_accommodations_2.values, m.n_accommodations_1.values)]
flag_2, flag_1 = (m.n_high_infra_steps_2 > 0).astype(int), (m.n_high_infra_steps_1 > 0).astype(int)
k = kappa(flag_2, flag_1)
m["gap_total"] = (m.n_high_infra_steps_2 - m.n_high_infra_steps_1).abs() + (m.n_accommodations_2 - m.n_accommodations_1).abs()
worst = m.sort_values("gap_total", ascending=False).head(5)
lines = [f"# Second annotation: agreement with the primary codes (n = {n})", "",
         "| measure | exact agreement | within 1 | mean absolute difference | mean (second - primary) | Spearman |", "|---|---|---|---|---|---|", *rows, "",
         f"Binary flag 'at least one high-infrastructure step': agreement {(flag_2 == flag_1).mean():.2f}, Cohen's kappa {k:.2f}.", "",
         "A positive mean difference means the second annotation counted more than the primary codes. Spearman measures whether the two rank responses similarly even if their scales differ.", "",
         "## Largest disagreements", "",
         "| id | second: steps / accommodations | primary: steps / accommodations | primary note | second note |", "|---|---|---|---|---|"]
for r in worst.itertuples():
    lines.append(f"| {r.audit_id} | {int(r.n_high_infra_steps_2)} / {int(r.n_accommodations_2)} | {int(r.n_high_infra_steps_1)} / {int(r.n_accommodations_1)} | {r.note_1} | {r.note_2} |")
with open("audit/second_annotation_agreement.md", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))
print("\n".join(lines))
