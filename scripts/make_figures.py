"""Cross-model summary figures from the released outputs.

python scripts/make_figures.py        (run from the repository root; reads results/ and audit/, writes figures/)

fig_probe_shift.png : next-token probability mass on high-infrastructure candidates, by context group, per model
fig_audit.png       : blind manual audit, high-infrastructure steps and accommodations per response, per model
Palette: reference categorical slots 1-4 (validated for adjacent pairs, light and dark); models are also told apart by marker
shape and by direct labels, because slots 3-4 are below 3:1 contrast on a light surface.
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, "src")
from analyze import boot_ci, GROUP

RES = os.environ.get("IAB_OUT", "results")
OUT = "figures"
os.makedirs(OUT, exist_ok=True)

SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
MODELS = [("Qwen3-4B-Instruct-2507", "Qwen3-4B", "#2a78d6", "o"), ("Phi-4-mini-instruct", "Phi-4-mini", "#eb6834", "s"),
          ("Llama-3.2-3B-Instruct", "Llama-3.2-3B", "#1baf7a", "^"), ("Qwen3-1.7B", "Qwen3-1.7B", "#eda100", "D")]
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "DejaVu Sans"], "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})


def style(ax):
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(AXIS); ax.spines["bottom"].set_color(AXIS)
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)


# ---------------- figure 1: probe shift ----------------
GROUPS = ["none", "high", "low", "spec_loc", "spec_only"]
LABELS = ["no\ncontext", "high-infra.\ncity", "low-infra.\nplace", "place +\nconstraints", "constraints\nonly"]
fig, ax = plt.subplots(figsize=(8.2, 4.6), dpi=160)
rows = {}
ends = []
for tag, short, col, mk in MODELS:
    p = pd.read_json(f"{RES}/{tag}/probes.jsonl", lines=True)
    p = p[p.probe != "PR0_default_country"].copy()
    p["prob"] = p.groupby(["probe", "condition"]).logp.transform(lambda s: np.exp(s - s.max()) / np.exp(s - s.max()).sum())
    h = p[p.group == "H"].groupby(["probe", "condition"]).prob.sum().reset_index()
    h["grp"] = h.condition.map(GROUP)
    # mean over probes within each condition, then over the conditions of the group (same rule as analyze.py T5a)
    y = h.groupby(["grp", "condition"]).prob.mean().groupby("grp").mean().reindex(GROUPS)
    rows[short] = y.values
    ax.plot(range(5), y.values, color=col, marker=mk, ms=7, lw=2, mec=SURFACE, mew=1.2, zorder=3)
    ends.append((y.values[-1], short, col))
# direct labels at the right end, spaced at least 0.065 apart so they never collide
ends.sort(key=lambda t: t[0])
ypos = []
for yv, _, _ in ends:
    ypos.append(yv if not ypos else max(yv, ypos[-1] + 0.065))
for (yv, name, col), yl in zip(ends, ypos):
    ax.plot([4.04, 4.14], [yv, yl], color=col, lw=1, zorder=2)
    ax.text(4.18, yl, name, color=INK, va="center", fontsize=9.5)
style(ax)
ax.set_xticks(range(5)); ax.set_xticklabels(LABELS, fontsize=9)
ax.set_ylim(0, 1); ax.set_xlim(-0.2, 5.1); ax.set_ylabel("probability mass on high-infrastructure options", fontsize=9.5)
ax.set_title("Next-token probes: what the model reaches for, by stated context", loc="left", fontsize=12, color=INK, pad=12)
fig.text(0.01, 0.01, "Mean over 20 probes (sum log-probability, renormalised over candidates). Pre-registered normalisation; 3 probes are degenerate (see RESULTS).", fontsize=7.6, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{OUT}/fig_probe_shift.png"); plt.close(fig)
pd.DataFrame(rows, index=GROUPS).round(3).to_csv(f"{OUT}/fig_probe_shift_data.csv")

# ---------------- figure 2: manual audit ----------------
k4 = pd.read_csv("audit/audit_key.csv"); c4 = pd.read_csv("audit/audit_coded.csv").merge(k4, on="audit_id")
c4 = c4[c4.condition.isin(["C00_none", "C09_constraints_only"])].assign(model="Qwen3-4B-Instruct-2507")
cr = pd.read_csv("audit/audit_rep_coded.csv").merge(pd.read_csv("audit/audit_rep_key.csv"), on="audit_id")
cl = pd.read_csv("audit/audit_llama_coded.csv").merge(pd.read_csv("audit/audit_llama_key.csv"), on="audit_id")
cols = ["model", "scenario_id", "condition", "n_high_infra_steps", "n_accommodations"]
allc = pd.concat([c4[cols], cr[cols], cl[cols]], ignore_index=True)
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4), dpi=160, sharex=True)
data_rows = []
for ax, (meas, title) in zip(axes, [("n_high_infra_steps", "High-infrastructure steps per response"), ("n_accommodations", "Accommodations per response")]):
    style(ax)
    for i, (tag, short, col, mk) in enumerate(MODELS):
        for j, (cond, lab) in enumerate([("C00_none", "no context"), ("C09_constraints_only", "constraints only")]):
            v = allc[(allc.model == tag) & (allc.condition == cond)].groupby("scenario_id")[meas].mean().values
            m, (lo, hi) = v.mean(), boot_ci(v)
            x = i + (-0.19 if j == 0 else 0.19)
            filled = j == 1
            ax.bar(x, m, 0.34, color=col if filled else SURFACE, edgecolor=col, linewidth=1.6, zorder=2)
            ax.plot([x, x], [lo, hi], color=INK2, lw=1.2, zorder=3)
            ax.text(x, hi + 0.08, f"{m:.2f}", ha="center", va="bottom", fontsize=8.2, color=INK)
            data_rows.append(dict(measure=meas, model=short, condition=lab, mean=round(m, 3), ci_lo=round(lo, 3), ci_hi=round(hi, 3), n=len(v)))
    ax.set_xticks(range(4)); ax.set_xticklabels([m[1] for m in MODELS], fontsize=9)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=10)
axes[0].set_ylim(0, 3.6); axes[1].set_ylim(0, 5.6)
handles = [plt.Rectangle((0, 0), 1, 1, fc=SURFACE, ec=MUTED, lw=1.6), plt.Rectangle((0, 0), 1, 1, fc=MUTED, ec=MUTED, lw=1.6)]
fig.legend(handles, ["no context (outline)", "constraints only (filled)"], loc="upper left", bbox_to_anchor=(0.01, 0.915), ncol=2, frameon=False, fontsize=9)
fig.suptitle("Blind manual audit: explicit constraints add accommodations; only Qwen3-4B drops high-infrastructure reliance", x=0.01, ha="left", fontsize=11.5, y=0.985)
fig.text(0.01, 0.01, "Bars: mean over 24 test scenarios, 95% bootstrap CI. Single annotator; condition hidden during coding (partly leaks through content).", fontsize=7.6, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 0.86)); fig.savefig(f"{OUT}/fig_audit.png"); plt.close(fig)
pd.DataFrame(data_rows).to_csv(f"{OUT}/fig_audit_data.csv", index=False)
print("figures written:", sorted(os.listdir(OUT)))
