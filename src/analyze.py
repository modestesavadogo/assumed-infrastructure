"""Analysis following PREREGISTRATION.md (design v2).

python src/analyze.py --tags Qwen3-4B-Instruct-2507,Phi-4-mini-instruct       # tables + figures (test split)
python src/analyze.py --tags Qwen3-4B-Instruct-2507 --split dev               # development split (lexicon refinement only)
python src/analyze.py --tags Qwen3-4B-Instruct-2507 --make-audit              # blind 120-response audit sample
python src/analyze.py --tags Qwen3-4B-Instruct-2507 --audit-eval audit/audit_coded.csv   # lexicon vs manual coding
"""
import argparse, json, os, sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coding import code_text

RES = os.environ.get("IAB_OUT", "results")
CATS = ["pay", "net", "power", "trans", "cost", "online"]
GROUP = {"C00_none": "none", "C01_boston": "high", "C02_paris": "high", "C03_seoul": "high",
         "C04_ouagadougou": "low", "C05_rural_burkina": "low", "C06_lagos": "low", "C07_dhaka": "low",
         "C08_ouaga_constraints": "spec_loc", "C09_constraints_only": "spec_only"}
GORDER = ["none", "high", "low", "spec_loc", "spec_only"]
BOOT_SEED = 0


def boot_ci(x, n=10000, seed=BOOT_SEED):
    """Percentile bootstrap 95% CI of the mean. A fresh generator per call makes every interval a pure function of its data
    (independent of call order, of which tables are built, and of the process)."""
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    rng = np.random.default_rng(seed)
    return np.percentile(rng.choice(x, (n, len(x))).mean(1), [2.5, 97.5])


def holm(ps):
    ps = np.asarray(ps, float); order = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * ps[i]); adj[i] = min(1.0, run)
    return adj


def md(df, floatfmt=3):
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(f"{v:.{floatfmt}f}" if isinstance(v, (float, np.floating)) else str(v) for v in r) + " |")
    return "\n".join(lines)


def load_generations(tag, greedy_only=False, exclude=()):
    g = pd.read_json(f"{RES}/{tag}/generations.jsonl", lines=True)
    if greedy_only:
        g = g[g.run == "greedy"].reset_index(drop=True)
    if exclude:                                  # sensitivity analyses: drop named scenarios (e.g. G9)
        g = g[~g.scenario_id.isin(exclude)].reset_index(drop=True)
    coded = pd.DataFrame([code_text(t) for t in g.response])
    g = pd.concat([g.reset_index(drop=True), coded], axis=1)
    w = g.words.clip(lower=1)
    g["D_rate"], g["A_rate"] = 100 * g.D_total / w, 100 * g.A_total / w
    g["digital_rate"] = 100 * g.digital_generic / w
    for c in CATS:
        g[f"{c}_D_rate"] = 100 * g[f"{c}_D"] / w
    g["has_disclaimer"] = (g.disclaimer > 0).astype(int)
    g["has_ctx"] = (g.ctx_mention > 0).astype(int)
    g["grp"] = g.condition.map(GROUP)
    return g


def scen_matrix(df, col, by="grp"):
    return df.groupby(["scenario_id", by])[col].mean().unstack(by)


def primary_contrasts(df):
    D = scen_matrix(df, "D_rate")
    spec = [("high", "none"), ("low", "none"), ("low", "high"), ("spec_loc", "low"), ("spec_only", "low")]
    rows = []
    for x, y in spec:
        if x in D and y in D:
            d = (D[x] - D[y]).dropna()
            try:
                p = wilcoxon(d).pvalue if (d != 0).any() else 1.0
            except ValueError:
                p = 1.0
            ci = boot_ci(d)
            rows.append(dict(contrast=f"{x} - {y}", n=len(d), mean_diff_D=d.mean(), ci=f"[{ci[0]:.2f}, {ci[1]:.2f}]",
                             dz=d.mean() / d.std(ddof=1) if d.std(ddof=1) > 0 else np.nan, p_raw=p))
    if rows:
        for r, q in zip(rows, holm([r["p_raw"] for r in rows])): r["p_holm"] = q
    return pd.DataFrame(rows)


def report_one(tag, split, greedy_only=False, exclude=()):
    out = f"{RES}/{tag}"
    sfx = ("_greedy" if greedy_only else "") + ("_excl_" + "_".join(exclude) if exclude else "")
    meta = json.load(open(f"{out}/meta.json")) if os.path.exists(f"{out}/meta.json") else {}
    g = load_generations(tag, greedy_only, exclude)
    s1 = g[(g.set == "s1") & (g.split == split)]
    dep, ctl = s1[s1.dependent == 1], s1[s1.dependent == 0]
    L = [f"# Results: {tag}  (S1 split = {split})", "", f"Model: {meta.get('model')}  revision: {meta.get('revision')}  date: {meta.get('date')}",
         f"Dependent scenarios: {dep.scenario_id.nunique()}  controls: {ctl.scenario_id.nunique()}  generations: {len(g)}", ""]

    # T1 per condition / T1b per group
    for by, order, title in [("condition", sorted(dep.condition.unique()), "T1a. Per condition"), ("grp", [x for x in GORDER if x in set(dep.grp)], "T1b. Per condition group")]:
        D, A = scen_matrix(dep, "D_rate", by), scen_matrix(dep, "A_rate", by)
        sums = dep.groupby(by)[["A_total", "D_total"]].sum()
        rows = []
        for c in order:
            dc, ac = boot_ci(D[c]), boot_ci(A[c]); sub = dep[dep[by] == c]
            rows.append(dict(**{by: c}, D_rate=D[c].mean(), D_ci=f"[{dc[0]:.2f}, {dc[1]:.2f}]", A_rate=A[c].mean(), A_ci=f"[{ac[0]:.2f}, {ac[1]:.2f}]",
                             adapt_ratio=sums.loc[c, "A_total"] / max(1, sums.loc[c].sum()), digital_rate=sub.digital_rate.mean(), disclaimer=sub.has_disclaimer.mean(),
                             words=sub.words.mean(), truncated=sub.truncated.mean()))
        L += [f"## {title}: dependent tasks, markers per 100 words (D = high-infrastructure, A = adaptation)", md(pd.DataFrame(rows)), ""]

    # T2 categories by group
    cat = dep.groupby("grp")[[f"{c}_D_rate" for c in CATS]].mean().reindex([x for x in GORDER if x in set(dep.grp)]).reset_index()
    L += ["## T2. D rate by category and group", md(cat), ""]

    # T3 primary contrasts (+ per-template robustness)
    L += ["## T3. Primary paired contrasts on D rate (Holm over the set; unit = scenario)", md(primary_contrasts(dep), 4), ""]
    for t in sorted(dep.template.unique()):
        L += [f"### T3-{t}. Same contrasts, template {t} only (robustness, descriptive)", md(primary_contrasts(dep[dep.template == t]).drop(columns=["p_holm"], errors="ignore"), 4), ""]

    # T4 controls
    if len(ctl):
        t4 = ctl.groupby("grp").agg(ctx_mention=("has_ctx", "mean"), D_rate=("D_rate", "mean"), A_rate=("A_rate", "mean"), disclaimer=("has_disclaimer", "mean")).reindex([x for x in GORDER if x in set(ctl.grp)]).reset_index()
        L += ["## T4. Infrastructure-independent controls (spurious injection check)", md(t4), ""]

    # T6 real prompts (S2)
    s2 = g[g.set == "s2"] if split == "test" else g.iloc[0:0]
    if len(s2):
        rows = []
        for dflag, name in [(1, "dependent_heuristic=1"), (0, "dependent_heuristic=0")]:
            sub = s2[s2.dependent == dflag]
            for c in sorted(sub.condition.unique()):
                x = sub[sub.condition == c]
                rows.append(dict(subset=name, condition=c, n_prompts=x.scenario_id.nunique(), D_rate=x.D_rate.mean(), A_rate=x.A_rate.mean(), disclaimer=x.has_disclaimer.mean(), ctx_mention=x.has_ctx.mean()))
        L += ["## T6. Real user prompts (OpenAssistant), exploratory", md(pd.DataFrame(rows)), ""]
        Dm = s2[s2.dependent == 1].groupby(["scenario_id", "condition"]).D_rate.mean().unstack("condition")
        rows = []
        for x, y in [("C04_ouagadougou", "C00_none"), ("C01_boston", "C00_none"), ("C09_constraints_only", "C04_ouagadougou")]:
            if x in Dm and y in Dm:
                d = (Dm[x] - Dm[y]).dropna(); ci = boot_ci(d)
                rows.append(dict(contrast=f"{x} - {y}", n=len(d), mean_diff_D=d.mean(), ci=f"[{ci[0]:.2f}, {ci[1]:.2f}]"))
        if rows: L += ["### T6b. Paired contrasts on dependent real prompts (exploratory)", md(pd.DataFrame(rows), 3), ""]

    # T5 probes
    pf = f"{out}/probes.jsonl"
    if os.path.exists(pf) and split == "test":
        p = pd.read_json(pf, lines=True)
        p["lp_per_token"] = p.logp / p.n_tok.clip(lower=1)
        for key, name in [("logp", "prob_sum"), ("lp_per_token", "prob_per_token")]:
            p[name] = p.groupby(["probe", "condition"])[key].transform(lambda s: np.exp(s - s.max()) / np.exp(s - s.max()).sum())
        cp = p[p.probe != "PR0_default_country"].copy()
        cp["grp"] = cp.condition.map(GROUP)
        mass = cp.groupby(["probe", "condition", "grp", "group"]).prob_sum.sum().unstack("group").fillna(0).reset_index()
        for c in ["H", "L", "N"]:
            if c not in mass: mass[c] = 0.0
        avg = mass.groupby("grp")[["H", "L", "N"]].mean().reindex([x for x in GORDER if x in set(mass.grp)]).reset_index()
        L += ["## T5a. Probe mass by candidate group, averaged over 20 probes and conditions in each group (sum log-prob, renormalised)", md(avg), ""]
        pv = mass.pivot(index="probe", columns="condition", values="H").round(2)
        L += ["## T5b. H mass per probe and condition", md(pv.reset_index()), ""]
        m2 = cp.groupby(["probe", "condition", "grp", "group"]).prob_per_token.sum().unstack("group").fillna(0).reset_index()
        avg2 = m2.groupby("grp")[[c for c in ["H", "L", "N"] if c in m2]].mean().reindex([x for x in GORDER if x in set(m2.grp)]).reset_index()
        L += ["## T5c. Sensitivity: per-token log-prob renormalisation", md(avg2), ""]
        dflt = p[p.probe == "PR0_default_country"].sort_values("prob_sum", ascending=False)[["cand", "group", "prob_sum"]]
        if len(dflt): L += ["## T5d. Default-country probe (no context)", md(dflt), ""]
        fig, ax = plt.subplots(figsize=(10, 6))
        cols = sorted(pv.columns, key=lambda c: list(GROUP).index(c))
        im = ax.imshow(pv[cols].values, vmin=0, vmax=1, cmap="viridis", aspect="auto")
        ax.set_xticks(range(len(cols))); ax.set_xticklabels([c.split("_")[0] for c in cols]); ax.set_yticks(range(len(pv.index))); ax.set_yticklabels(pv.index, fontsize=7)
        plt.colorbar(im, label="mass on high-infrastructure candidates"); plt.title(f"{tag}: next-token probes by context")
        plt.tight_layout(); plt.savefig(f"{out}/fig_probes{sfx}.png", dpi=150); plt.close()

    # figure: markers by group
    fig, ax = plt.subplots(figsize=(8, 4.5)); groups = [x for x in GORDER if x in set(dep.grp)]; x = np.arange(len(groups))
    for off, col, lab, color in [(-0.2, "D_rate", "high-infrastructure markers (D)", "tab:red"), (0.2, "A_rate", "adaptation markers (A)", "tab:green")]:
        M = scen_matrix(dep, col); m = [M[c].mean() for c in groups]; ci = [boot_ci(M[c]) for c in groups]
        ax.bar(x + off, m, 0.4, yerr=[[a - c_[0] for a, c_ in zip(m, ci)], [c_[1] - a for a, c_ in zip(m, ci)]], label=lab, color=color, capsize=3)
    ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylabel("markers per 100 words"); ax.legend(); ax.set_title(f"{tag}: dependent tasks, {split} split (95% CI over scenarios)")
    plt.tight_layout(); plt.savefig(f"{out}/fig_markers_{split}{sfx}.png", dpi=150); plt.close()

    open(f"{out}/tables_{split}{sfx}.md", "w", encoding="utf-8").write("\n".join(L))
    g.drop(columns=["prompt"]).to_csv(f"{out}/coded_generations{sfx}.csv", index=False)
    return "\n".join(L), primary_contrasts(dep).assign(model=tag)


def make_audit(tag):
    g = load_generations(tag)
    d = g[(g.set == "s1") & (g.split == "test") & (g.dependent == 1) & (g.run == "greedy") & (g.template == "A")
          & g.condition.isin(["C00_none", "C01_boston", "C04_ouagadougou", "C08_ouaga_constraints", "C09_constraints_only"])]
    ids = sorted(d.scenario_id.unique())
    pick = list(np.random.default_rng(7).choice(ids, size=24, replace=False))
    s = d[d.scenario_id.isin(pick)][["scenario_id", "condition", "prompt", "response"]].sample(frac=1, random_state=3).reset_index(drop=True)
    s.insert(0, "audit_id", [f"A{i + 1:03d}" for i in range(len(s))])
    os.makedirs("audit", exist_ok=True)
    s[["audit_id", "scenario_id", "condition"]].to_csv("audit/audit_key.csv", index=False)         # key kept apart from the coding view
    blind = s[["audit_id", "response"]].copy()
    for c in ["n_high_infra_steps", "n_accommodations", "generic_disclaimer_only(0/1)", "note"]: blind[c] = ""
    blind.to_csv("audit/audit_blind.csv", index=False)
    print("wrote audit/audit_blind.csv (no condition shown) and audit/audit_key.csv:", len(s))


def audit_eval(tag, path):
    key = pd.read_csv("audit/audit_key.csv")
    cod = pd.read_csv(path).merge(key, on="audit_id")
    g = load_generations(tag)
    g = g[(g.set == "s1") & (g.run == "greedy") & (g.template == "A")][["scenario_id", "condition", "D_total", "A_total"]]
    m = cod.merge(g, on=["scenario_id", "condition"])
    m["manual_flag"] = (m.n_high_infra_steps > 0).astype(int); m["lex_flag"] = (m.D_total > 0).astype(int)
    tp = int(((m.manual_flag == 1) & (m.lex_flag == 1)).sum()); fp = int(((m.manual_flag == 0) & (m.lex_flag == 1)).sum())
    fn = int(((m.manual_flag == 1) & (m.lex_flag == 0)).sum()); tn = int(((m.manual_flag == 0) & (m.lex_flag == 0)).sum())
    n = len(m); po = (tp + tn) / n; pe = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / n ** 2
    kappa = (po - pe) / (1 - pe) if pe < 1 else np.nan
    rho = spearmanr(m.D_total, m.n_high_infra_steps).correlation
    rho_a = spearmanr(m.A_total, m.n_accommodations).correlation
    by = m.groupby("condition").agg(manual_high_infra=("n_high_infra_steps", "mean"), lexicon_D=("D_total", "mean"),
                                    manual_accommodations=("n_accommodations", "mean"), lexicon_A=("A_total", "mean"),
                                    disclaimer_only=("generic_disclaimer_only(0/1)", "mean")).reset_index()
    txt = [f"# Audit: lexicon vs manual coding ({n} responses)", f"response-level D flag: TP={tp} FP={fp} FN={fn} TN={tn}",
           f"precision={tp / max(1, tp + fp):.2f} recall={tp / max(1, tp + fn):.2f} kappa={kappa:.2f}",
           f"Spearman(D_total, manual high-infra steps)={rho:.2f}  Spearman(A_total, manual accommodations)={rho_a:.2f}", "", md(by, 2)]
    open(f"{RES}/{tag}/audit_eval.md", "w", encoding="utf-8").write("\n".join(txt)); print("\n".join(txt))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", required=True)
    ap.add_argument("--split", default="test", choices=["test", "dev"])
    ap.add_argument("--make-audit", action="store_true")
    ap.add_argument("--greedy-only", action="store_true", help="use only greedy runs (comparable across models)")
    ap.add_argument("--audit-eval", default=None)
    ap.add_argument("--exclude", default="", help="comma-separated scenario ids to drop (sensitivity analysis, e.g. G9)")
    a = ap.parse_args()
    excl = tuple(x for x in a.exclude.split(",") if x)
    tags = a.tags.split(",")
    if a.make_audit:
        return make_audit(tags[0])
    if a.audit_eval:
        return audit_eval(tags[0], a.audit_eval)
    allc = []
    for t in tags:
        text, pc = report_one(t, a.split, a.greedy_only, excl); allc.append(pc); print(text, "\n")
    if len(tags) > 1:
        cm = pd.concat(allc)
        open(f"{RES}/cross_model_{a.split}{'_greedy' if a.greedy_only else ''}{'_excl_' + '_'.join(excl) if excl else ''}.md", "w", encoding="utf-8").write("# Primary contrasts across models\n\n" + md(cm, 4))
        print("# Cross-model\n", md(cm, 4))


if __name__ == "__main__":
    main()
