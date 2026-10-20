"""Paired statistics on the blind audit (manual codes), unit = scenario (24 test scenarios x 5 conditions)."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "src")
from analyze import boot_ci, md
from scipy.stats import wilcoxon

tag = "Qwen3-4B-Instruct-2507"
key = pd.read_csv("audit/audit_key.csv")
cod = pd.read_csv("audit/audit_coded.csv").merge(key, on="audit_id")
cod["any_high"] = (cod.n_high_infra_steps > 0).astype(int)
rows = []
for c, g in cod.groupby("condition"):
    hi = g.set_index("scenario_id").n_high_infra_steps; ac = g.set_index("scenario_id").n_accommodations
    rows.append(dict(condition=c, n=len(g), high_infra_mean=hi.mean(), high_ci=str(np.round(boot_ci(hi), 2).tolist()),
                     share_with_high=g.any_high.mean(), accommodations_mean=ac.mean(), acc_ci=str(np.round(boot_ci(ac), 2).tolist())))
t1 = pd.DataFrame(rows)
P = cod.pivot(index="scenario_id", columns="condition", values="n_high_infra_steps")
A = cod.pivot(index="scenario_id", columns="condition", values="n_accommodations")
rows = []
for x, y in [("C01_boston", "C00_none"), ("C04_ouagadougou", "C00_none"), ("C08_ouaga_constraints", "C04_ouagadougou"), ("C09_constraints_only", "C04_ouagadougou"), ("C08_ouaga_constraints", "C09_constraints_only")]:
    for name, M in [("high_infra_steps", P), ("accommodations", A)]:
        d = (M[x] - M[y]).dropna(); ci = boot_ci(d)
        try: p = wilcoxon(d).pvalue if (d != 0).any() else 1.0
        except ValueError: p = 1.0
        rows.append(dict(contrast=f"{x} - {y}", measure=name, n=len(d), mean_diff=d.mean(), ci=f"[{ci[0]:.2f}, {ci[1]:.2f}]", p_raw=p))
t2 = pd.DataFrame(rows)
txt = "# Blind audit: manual codes (single annotator, partly blind to condition)\n\n## Per condition\n" + md(t1, 2) + "\n\n## Paired contrasts (exploratory, n = 24 scenarios, no multiplicity correction)\n" + md(t2, 3)
open(f"results/{tag}/audit_stats.md", "w", encoding="utf-8").write(txt)
print(txt)

# 20-item sample for an independent second annotation (no codes shown)
sp = cod.groupby("condition", group_keys=False).apply(lambda g: g.sample(4, random_state=5)).sample(frac=1, random_state=9)
out = sp[["audit_id", "response"]].copy()
for c in ["n_high_infra_steps", "n_accommodations", "note"]: out[c] = ""
out.to_csv("audit/second_annotation_sample.csv", index=False)
print("\nsecond-annotation sample written:", len(out), "items")
