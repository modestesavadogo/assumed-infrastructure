"""Manual-audit statistics for the replication models (Phi-4-mini-instruct, Qwen3-1.7B) next to the Qwen3-4B audit.
Unit = scenario (24 test scenarios); conditions C00 (no context) and C09 (constraints only). Exploratory."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "src")
from analyze import boot_ci, md, load_generations
from scipy.stats import wilcoxon, spearmanr

key = pd.read_csv("audit/audit_rep_key.csv")
cod = pd.read_csv("audit/audit_rep_coded.csv").merge(key, on="audit_id")
import os
if os.path.exists("audit/audit_llama_coded.csv"):          # Llama audit (added later, same rubric)
    cod = pd.concat([cod, pd.read_csv("audit/audit_llama_coded.csv").merge(pd.read_csv("audit/audit_llama_key.csv"), on="audit_id")], ignore_index=True)
k4 = pd.read_csv("audit/audit_key.csv"); c4 = pd.read_csv("audit/audit_coded.csv").merge(k4, on="audit_id")
c4 = c4[c4.condition.isin(["C00_none", "C09_constraints_only"])].assign(model="Qwen3-4B-Instruct-2507")
allc = pd.concat([cod[c4.columns.intersection(cod.columns)], c4[c4.columns.intersection(cod.columns)]], ignore_index=True)
allc["any_high"] = (allc.n_high_infra_steps > 0).astype(int)

rows = []
for (m, c), g in allc.groupby(["model", "condition"]):
    hi, ac = g.n_high_infra_steps.values, g.n_accommodations.values
    rows.append(dict(model=m, condition=c, n=len(g), high_infra=hi.mean(), high_ci=str(np.round(boot_ci(hi), 2).tolist()), share_with_high=g.any_high.mean(),
                     accommodations=ac.mean(), acc_ci=str(np.round(boot_ci(ac), 2).tolist())))
t1 = pd.DataFrame(rows)
rows = []
for m, g in allc.groupby("model"):
    P = g.pivot(index="scenario_id", columns="condition", values="n_high_infra_steps"); A = g.pivot(index="scenario_id", columns="condition", values="n_accommodations")
    for name, M in [("high_infra_steps", P), ("accommodations", A)]:
        d = (M["C09_constraints_only"] - M["C00_none"]).dropna(); ci = boot_ci(d)
        try: p = wilcoxon(d).pvalue if (d != 0).any() else 1.0
        except ValueError: p = 1.0
        rows.append(dict(model=m, measure=name, contrast="constraints_only - none", n=len(d), mean_diff=d.mean(), ci=f"[{ci[0]:.2f}, {ci[1]:.2f}]", p_raw=p))
t2 = pd.DataFrame(rows)

# lexicon vs manual on the replication models (does the weak D lexicon generalise?)
rows = []
for m in ["Phi-4-mini-instruct", "Qwen3-1.7B", "Llama-3.2-3B-Instruct"]:
    g = load_generations(m, greedy_only=True); g = g[(g.set == "s1") & (g.template == "A")][["scenario_id", "condition", "D_total", "A_total"]]
    x = cod[cod.model == m].merge(g, on=["scenario_id", "condition"])
    mf, lf = (x.n_high_infra_steps > 0).astype(int), (x.D_total > 0).astype(int)
    tp, fp, fn, tn = int(((mf == 1) & (lf == 1)).sum()), int(((mf == 0) & (lf == 1)).sum()), int(((mf == 1) & (lf == 0)).sum()), int(((mf == 0) & (lf == 0)).sum())
    n = len(x); po = (tp + tn) / n; pe = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / n ** 2
    rows.append(dict(model=m, n=n, precision=tp / max(1, tp + fp), recall=tp / max(1, tp + fn), kappa=(po - pe) / (1 - pe) if pe < 1 else np.nan,
                     rho_D=spearmanr(x.D_total, x.n_high_infra_steps).correlation, rho_A=spearmanr(x.A_total, x.n_accommodations).correlation))
t3 = pd.DataFrame(rows)
txt = ("# Replication audit (manual codes; single annotator; partly blind to condition; exploratory)\n\n## Per model and condition\n" + md(t1, 2) +
       "\n\n## Within-model change, constraints-only minus none (n = 24 scenarios, no multiplicity correction)\n" + md(t2, 3) +
       "\n\n## Lexicon vs manual on the replication models\n" + md(t3, 2))
open("results/replication_audit_stats.md", "w", encoding="utf-8").write(txt); print(txt)
