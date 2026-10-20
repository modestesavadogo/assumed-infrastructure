"""Generation + next-token probes for the infrastructure-assumption audit (design v2, see PREREGISTRATION.md).

Local smoke test:  python src/run_experiment.py --model Qwen/Qwen3-0.6B --smoke --dtype fp32 --batch 3
GPU run:           python src/run_experiment.py --model Qwen/Qwen3-4B-Instruct-2507 --dtype fp16
Outputs (appended as JSONL so a crash keeps partial results): results/<tag>/generations.jsonl, probes.jsonl, meta.json
"""
import argparse, hashlib, json, os, platform, re, time
import pandas as pd
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

DATA = os.environ.get("IAB_DATA", "data")
OUT = os.environ.get("IAB_OUT", "results")
TEMPLATES = {
    "A": "{context}{scenario} Give me a concrete step-by-step plan in under 300 words.",
    "B": "{context}{scenario} How should I go about this? Keep it practical.",
    "R": "{context}{scenario}",  # real user prompts: used as written
}


def build_prompt(template: str, ctx_text: str, scenario: str) -> str:
    c = (ctx_text.strip() + " ") if ctx_text.strip() else ""
    return TEMPLATES[template].format(context=c, scenario=scenario)


def apply_chat(tok, user: str, prefix: str = "") -> str:
    msgs = [{"role": "user", "content": user}]
    # date_string is ignored by templates that do not use it; Llama 3.x templates would otherwise inject today's date
    try:
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False, date_string="26 Jul 2024")
    except TypeError:
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    return text + prefix


def eos_ids(model, tok):
    e = getattr(model.generation_config, "eos_token_id", None)
    e = [e] if isinstance(e, int) else list(e or [])
    return set(e + ([tok.eos_token_id] if tok.eos_token_id is not None else []))


@torch.no_grad()
def generate_batch(model, tok, texts, max_new_tokens, sample, seed):
    enc = tok(texts, return_tensors="pt", padding=True, add_special_tokens=False).to(model.device)
    torch.manual_seed(seed)
    pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    kw = dict(max_new_tokens=max_new_tokens, pad_token_id=pad)
    if sample:
        kw.update(do_sample=True, temperature=0.7, top_p=0.8, top_k=20)
    else:
        kw.update(do_sample=False)
    out = model.generate(**enc, **kw)
    n_in = enc.input_ids.shape[1]
    stops = eos_ids(model, tok)
    res = []
    for o in out:
        gen = o[n_in:].tolist()
        stopped = any(t in stops for t in gen)
        n = next((i for i, t in enumerate(gen) if t in stops), len(gen))
        res.append((tok.decode(gen[:n], skip_special_tokens=True).strip(), n, int(not stopped)))
    return res


@torch.no_grad()
def cand_logprobs(model, tok, user, prefix, cands):
    base = apply_chat(tok, user, prefix)
    base_ids = tok(base, add_special_tokens=False).input_ids
    res = []
    for c in cands:
        full_ids = tok(base + c, add_special_tokens=False).input_ids
        k = 0
        while k < min(len(base_ids), len(full_ids)) and base_ids[k] == full_ids[k]:
            k += 1
        ids = torch.tensor([full_ids], device=model.device)
        logits = model(ids).logits[0].float()
        lp = torch.log_softmax(logits[:-1], -1).gather(1, ids[0, 1:, None]).squeeze(1)
        res.append(dict(logp=float(lp[k - 1:].sum()), n_tok=len(full_ids) - k, boundary_shift=int(k < len(base_ids))))
    return res


def load_model(name, dtype):
    d = {"auto": "auto", "fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[dtype]
    dm = "auto" if torch.cuda.is_available() else None
    try:
        return AutoModelForCausalLM.from_pretrained(name, dtype=d, device_map=dm)
    except TypeError:
        return AutoModelForCausalLM.from_pretrained(name, torch_dtype=d, device_map=dm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--sets", default="s1,s2", help="s1 = controlled scenarios, s2 = real user prompts")
    ap.add_argument("--templates", default="A,B")
    ap.add_argument("--samples", type=int, default=1, help="temperature samples in addition to the greedy run")
    ap.add_argument("--s2-conditions", default="C00_none,C01_boston,C04_ouagadougou,C09_constraints_only")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--max-new-tokens", type=int, default=500)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--dtype", default="auto")
    args = ap.parse_args()

    scen = pd.read_csv(f"{DATA}/scenarios.csv")
    scen["split"] = ["dev" if int(re.search(r"\d+", i).group()) <= 3 else "test" for i in scen.id]
    real = pd.read_csv(f"{DATA}/real_prompts.csv")
    ctxs = {k: v for k, v in json.load(open(f"{DATA}/contexts.json")).items() if not k.startswith("_")}
    probes = json.load(open(f"{DATA}/probes.json"))
    ctx_probes = probes["context_probes"]
    templates = args.templates.split(",")
    s2_conds = args.s2_conditions.split(",")
    if args.smoke:
        scen = scen[scen.id.isin(["L1", "T1", "W1"])]
        real = real.iloc[:2]
        ctxs = {k: ctxs[k] for k in ["C00_none", "C09_constraints_only"]}
        s2_conds = ["C00_none", "C09_constraints_only"]
        templates, ctx_probes = ["A"], ctx_probes[:2]
        args.samples, args.max_new_tokens = 0, 40
    tag = args.tag or args.model.split("/")[-1] + ("_smoke" if args.smoke else "")
    out_dir = os.path.join(OUT, tag)
    os.makedirs(out_dir, exist_ok=True)

    tok = AutoTokenizer.from_pretrained(args.model)
    tok.padding_side = "left"
    if tok.pad_token is None:              # Llama tokenizers ship without a pad token
        tok.pad_token = tok.eos_token
    model = load_model(args.model, args.dtype)
    model.eval()

    items = []
    sets = args.sets.split(",")
    if "s1" in sets:
        for r in scen.itertuples():
            for c, ct in ctxs.items():
                for t in templates:
                    items.append(dict(set="s1", scenario_id=r.id, group=r.group, dependent=int(r.dependent), split=r.split,
                                      condition=c, template=t, prompt=build_prompt(t, ct, r.text)))
    if "s2" in sets:
        for r in real.itertuples():
            for c in s2_conds:
                items.append(dict(set="s2", scenario_id=r.id, group="real", dependent=int(r.dependent_heuristic), split="test",
                                  condition=c, template="R", prompt=build_prompt("R", ctxs[c], r.text)))
    items.sort(key=lambda d: len(d["prompt"]))
    runs = [("greedy", False, 0)] + [(f"sample{i + 1}", True, 1000 + i) for i in range(args.samples)]

    gen_path = os.path.join(out_dir, "generations.jsonl")
    done = set()
    if os.path.exists(gen_path):
        for line in open(gen_path, encoding="utf-8"):
            d = json.loads(line)
            done.add((d["set"], d["scenario_id"], d["condition"], d["template"], d["run"]))
    t0 = time.time()
    with open(gen_path, "a", encoding="utf-8") as f:
        for run, sample, seed in runs:
            # real prompts (s2) are run greedy only; controlled scenarios (s1) get greedy + temperature samples
            todo = [it for it in items if (it["set"], it["scenario_id"], it["condition"], it["template"], run) not in done and (run == "greedy" or it["set"] == "s1")]
            for i in range(0, len(todo), args.batch):
                batch = todo[i:i + args.batch]
                outs = generate_batch(model, tok, [apply_chat(tok, it["prompt"]) for it in batch], args.max_new_tokens, sample, seed + i)
                for it, (o, n, trunc) in zip(batch, outs):
                    f.write(json.dumps(dict(it, run=run, response=o, n_new_tokens=n, truncated=trunc), ensure_ascii=False) + "\n")
                f.flush()
                if (i // args.batch) % 10 == 0:
                    print(f"[{run}] {i + len(batch)}/{len(todo)}  {time.time() - t0:.0f}s", flush=True)

    with open(os.path.join(out_dir, "probes.jsonl"), "w", encoding="utf-8") as f:
        for p in ctx_probes:
            for c, ct in ctxs.items():
                user = (ct.strip() + " " if ct.strip() else "") + p["user"]
                res = cand_logprobs(model, tok, user, p["prefix"], [x[0] for x in p["cands"]])
                for (cand, grp), r in zip(p["cands"], res):
                    f.write(json.dumps(dict(probe=p["id"], condition=c, cand=cand, group=grp, **r)) + "\n")
        if not args.smoke:
            d = probes["default_world_probe"]
            res = cand_logprobs(model, tok, d["user"], d["prefix"], [x[0] for x in d["cands"]])
            for (cand, grp), r in zip(d["cands"], res):
                f.write(json.dumps(dict(probe=d["id"], condition="C00_none", cand=cand, group=grp, **r)) + "\n")

    json.dump(dict(model=args.model, revision=getattr(model.config, "_commit_hash", None), args=vars(args), torch=torch.__version__,
                   transformers=transformers.__version__, platform=platform.platform(), cuda=torch.cuda.is_available(), n_items=len(items),
                   data_hash={fn: hashlib.sha256(open(f"{DATA}/{fn}", "rb").read().replace(b"\r\n", b"\n")).hexdigest()[:12]
                              for fn in ["scenarios.csv", "contexts.json", "probes.json", "real_prompts.csv"]},
                   date=time.strftime("%Y-%m-%d %H:%M:%S"), seconds=round(time.time() - t0)),
              open(os.path.join(out_dir, "meta.json"), "w"), indent=2)
    print("done", out_dir)


if __name__ == "__main__":
    main()
