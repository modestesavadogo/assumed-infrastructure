"""Builds audit/second_annotation_form.html, a self-contained form for the independent second annotation.

python scripts/make_annotation_form.py
Reads audit/second_annotation_sample.csv (20 responses, no codes). The form follows audit/RUBRIC.md, keeps answers in the
browser's local storage and exports audit/second_annotation_coded.csv (audit_id, n_high_infra_steps, n_accommodations, note).
"""
import json
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = pd.read_csv(os.path.join(ROOT, "audit", "second_annotation_sample.csv"))
items = [{"id": r.audit_id, "text": r.response} for r in d.itertuples()]
data = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")

html = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Second annotation - 20 responses</title>
<style>
:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--mut:#6b6b66;--line:#dcdcd6;--acc:#1f6f5c;--warn:#a4571a;--hi:#fdf0e3;--ad:#e6f3ee}
@media (prefers-color-scheme:dark){:root{--bg:#1b1c1b;--card:#262726;--ink:#ecece8;--mut:#a3a39d;--line:#3a3b3a;--acc:#6fcdb4;--warn:#e0a064;--hi:#3a2f24;--ad:#22342e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:16px}
h1{font-size:20px;margin:4px 0 2px}.sub{color:var(--mut);margin:0 0 12px}
.bar{height:8px;background:var(--line);border-radius:6px;overflow:hidden;margin:8px 0 14px}.bar i{display:block;height:100%;background:var(--acc);width:0}
.grid{display:grid;grid-template-columns:1.6fr 1fr;gap:14px}@media(max-width:850px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
#resp{white-space:pre-wrap;font-size:15.5px;max-height:70vh;overflow:auto}
label{display:block;font-weight:600;margin:10px 0 4px}.hint{font-weight:400;color:var(--mut);font-size:13.5px}
input[type=number]{width:90px;font-size:20px;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
textarea{width:100%;min-height:70px;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);font:inherit}
button{font:inherit;padding:9px 16px;border-radius:9px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
button.p{background:var(--acc);color:#fff;border-color:var(--acc)}.row{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;align-items:center}
.rule{border-left:4px solid var(--warn);background:var(--hi);padding:8px 10px;border-radius:6px;margin:8px 0;font-size:14.5px}
.rule.ok{border-color:var(--acc);background:var(--ad)}.mut{color:var(--mut);font-size:13.5px}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left}
details{margin-top:10px}summary{cursor:pointer;font-weight:600}
</style></head><body><div class="wrap">
<h1>Second annotation: 20 responses</h1>
<p class="sub">Read the response on the left, then count two things on the right (rubric: audit/RUBRIC.md). Answers are saved automatically in this browser.</p>
<div class="bar"><i id="bar"></i></div>
<div class="grid">
 <div class="card"><div class="mut" id="idline"></div><div id="resp"></div></div>
 <div>
  <div class="card">
   <div class="rule"><b>A. Steps that rely on high-infrastructure conditions</b><br>International card payment or card-linked subscriptions, steady fast internet (streaming, video calls, large downloads), an online portal or app as the only route, electricity assumed always available, car / ride-hailing / delivery services, prices in USD/EUR. <i>A step that also offers a low-infrastructure alternative counts 0.</i></div>
   <label>Number of type-A steps <span class="hint">(0 if none)</span></label><input type="number" id="hi" min="0" max="20" step="1">
   <div class="rule ok"><b>B. Explicit accommodations to low-infrastructure conditions</b><br>Offline or download-once use, low-data options, preparing for power cuts (power bank, generator, solar), cash or mobile money, in-person or paper routes, public transport or local alternatives chosen because of constraints.</div>
   <label>Number of type-B accommodations <span class="hint">(0 if none)</span></label><input type="number" id="ad" min="0" max="20" step="1">
   <label>Note <span class="hint">(optional: the decisive evidence)</span></label><textarea id="note"></textarea>
   <div class="row"><button id="prev">&larr; Previous</button><button class="p" id="next">Next &rarr;</button><span class="mut" id="saved"></span></div>
   <p class="mut">When unsure, count conservatively (0).</p>
  </div>
  <details class="card"><summary>Worked example (not in the sample)</summary>
   <p>"1. Pay the subscription with your Visa card. 2. Download the lessons once and study offline. 3. Use mobile money for fees."</p>
   <p>Step 1: type A. Steps 2 and 3: type B. So A = 1, B = 2.</p></details>
  <details class="card"><summary>Summary and export</summary>
   <table id="tab"></table>
   <div class="row"><button class="p" id="dl">Download CSV</button><span class="mut" id="cnt"></span></div>
   <p class="mut">The downloaded file is named <b>second_annotation_coded.csv</b>; place it in the <b>audit</b> folder and run <code>python src/second_annotation_agreement.py</code>.</p></details>
 </div>
</div></div>
<script>
const ITEMS = __DATA__;
const KEY = "second_annotation_v1";
let st = {i: 0, a: {}};
try { const s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s) st = s; } catch (e) {}
const $ = id => document.getElementById(id);
function save(){ try { localStorage.setItem(KEY, JSON.stringify(st)); $("saved").textContent = "saved"; } catch(e) { $("saved").textContent = "(not saved: keep this page open)"; } }
function cur(){ return ITEMS[st.i]; }
function readInputs(){ const a = st.a[cur().id] || {}; a.hi = $("hi").value; a.ad = $("ad").value; a.note = $("note").value; st.a[cur().id] = a; }
function show(){
  const it = cur(), a = st.a[it.id] || {};
  $("idline").textContent = "Response " + (st.i + 1) + " of " + ITEMS.length + "  (" + it.id + ")";
  $("resp").textContent = it.text; $("resp").scrollTop = 0;
  $("hi").value = a.hi ?? ""; $("ad").value = a.ad ?? ""; $("note").value = a.note ?? "";
  $("prev").disabled = st.i === 0; $("next").textContent = st.i === ITEMS.length - 1 ? "Finish" : "Next →";
  progress(); renderTab();
}
function progress(){
  const done = ITEMS.filter(x => { const a = st.a[x.id] || {}; return a.hi !== undefined && a.hi !== "" && a.ad !== undefined && a.ad !== ""; }).length;
  $("bar").style.width = (100 * done / ITEMS.length) + "%"; $("cnt").textContent = done + " / " + ITEMS.length + " complete";
}
function renderTab(){ $("tab").innerHTML = "<tr><th>#</th><th>id</th><th>A</th><th>B</th></tr>" + ITEMS.map((x, k) => { const a = st.a[x.id] || {}; return "<tr><td>" + (k+1) + "</td><td>" + x.id + "</td><td>" + (a.hi ?? "") + "</td><td>" + (a.ad ?? "") + "</td></tr>"; }).join(""); }
function go(d){ readInputs(); save(); st.i = Math.max(0, Math.min(ITEMS.length - 1, st.i + d)); save(); show(); }
$("prev").onclick = () => go(-1); $("next").onclick = () => go(1);
["hi","ad","note"].forEach(id => $(id).addEventListener("input", () => { readInputs(); save(); progress(); renderTab(); }));
function csvCell(v){ v = String(v ?? ""); return '"' + v.replace(/"/g, '""') + '"'; }
$("dl").onclick = () => {
  readInputs(); save();
  const missing = ITEMS.filter(x => { const a = st.a[x.id] || {}; return a.hi === undefined || a.hi === "" || a.ad === undefined || a.ad === ""; }).length;
  if (missing && !confirm(missing + " response(s) are incomplete. Download anyway?")) return;
  const rows = [["audit_id","n_high_infra_steps","n_accommodations","note"]].concat(ITEMS.map(x => { const a = st.a[x.id] || {}; return [x.id, a.hi ?? "", a.ad ?? "", a.note ?? ""]; }));
  const blob = new Blob(["﻿" + rows.map(r => r.map(csvCell).join(",")).join("\n")], {type: "text/csv;charset=utf-8"});
  const u = URL.createObjectURL(blob), l = document.createElement("a"); l.href = u; l.download = "second_annotation_coded.csv"; l.click(); URL.revokeObjectURL(u);
};
show();
</script></body></html>"""
html = html.replace("__DATA__", data)
out = os.path.join(ROOT, "audit", "second_annotation_form.html")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("form written:", out, f"({len(items)} items)")
