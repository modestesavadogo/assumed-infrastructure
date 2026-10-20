"""Builds data/real_prompts.csv: real user prompts sampled from OpenAssistant/oasst1 (Apache-2.0, human-written).

Documented filter (fixed): English initial prompts by users; 60-500 characters; practical help-seeking intent
("how can I", "I want to", "I need to", "help me", "how to", "best way to", "any tips"); excludes coding, creative
writing, role-play, and prompts naming a country/city/region. The whole filtered pool is kept (no sampling), sorted by message_id.
'dependent_heuristic' is a keyword flag on the PROMPT only (never on model output) and is used for exploratory splits.
"""
import hashlib
import re
import sys
import pandas as pd
from huggingface_hub import hf_hub_download

# source pinned for reproducibility: dataset revision and file hash (the script stops if the file differs)
OASST1_REVISION = "fdf72ae0827c1cda404aff25b6603abec9e3399b"
PARQUET_SHA256 = "bbfadf5ed1278ba2208c837fdcad865adf65f5df55d80abadab2745db13fcb5e"
OUT = sys.argv[1] if len(sys.argv) > 1 else "data/real_prompts.csv"

path = hf_hub_download("OpenAssistant/oasst1", "data/train-00000-of-00001-b42a775f407cee45.parquet", repo_type="dataset", revision=OASST1_REVISION)
assert hashlib.sha256(open(path, "rb").read()).hexdigest() == PARQUET_SHA256, "source parquet differs from the pinned file"
df = pd.read_parquet(path)
df = df[(df.role == "prompter") & df.parent_id.isna() & (df.lang == "en")].copy()
df["text"] = df.text.str.strip()
df = df[df.text.str.len().between(60, 500)]

intent = re.compile(r"\b(how (can|do|should|would|could) i|i want to|i need to|i would like to|help me|how to|best way to|any (tips|advice)|what should i)\b", re.I)
bad = re.compile(r"```|\b(python|javascript|typescript|java|c\+\+|c#|rust|golang|sql|regex|html|css|api|bash|linux|function|algorithm|code|script|pytorch|tensorflow|github|stack ?overflow)\b|\b(write|compose|continue) (me )?(a|an|the)\b|\b(story|poem|essay|novel|lyrics|song|roleplay|role-play|pretend|character|dnd|d&d)\b", re.I)
places = re.compile(r"\b(usa|u\.s\.|united states|america|american|canada|canadian|mexico|brazil|argentina|uk|united kingdom|england|london|scotland|ireland|france|paris|germany|berlin|spain|madrid|italy|rome|netherlands|sweden|norway|denmark|finland|poland|russia|ukraine|turkey|china|beijing|shanghai|japan|tokyo|korea|seoul|india|delhi|mumbai|pakistan|bangladesh|dhaka|indonesia|philippines|vietnam|thailand|australia|sydney|new zealand|africa|african|nigeria|lagos|kenya|nairobi|ghana|egypt|morocco|south africa|ethiopia|europe|european|asia|asian|middle east|california|texas|new york|florida|ohio|my country|my city|my state)\b", re.I)
df = df[df.text.str.contains(intent) & ~df.text.str.contains(bad) & ~df.text.str.contains(places)]
df = df.drop_duplicates("text")
dep_kw = re.compile(r"\b(online|internet|website|app|apps|buy|purchase|pay|payment|money|bank|loan|invest|business|course|laptop|phone|computer|software|cloud|travel|trip|flight|visa|doctor|hospital|medicine|job|apply|startup|shop|store|deliver|delivery|subscription|download|stream|video|email|account|savings|budget|insurance|tax|taxes|car|commute)\b", re.I)
df["dependent_heuristic"] = df.text.str.contains(dep_kw).astype(int)
n_pool = len(df)
out = df.sort_values("message_id")[["message_id", "text", "dependent_heuristic"]].reset_index(drop=True)   # keep the whole filtered pool: no sampling
out.insert(0, "id", [f"R{i + 1:03d}" for i in range(len(out))])
out.to_csv(OUT, index=False, lineterminator="\n")
print("pool after filter:", n_pool, "| kept:", len(out), "| dependent_heuristic share:", round(out.dependent_heuristic.mean(), 2))
print(out.text.str.len().describe()[["mean", "min", "max"]].round(0).to_dict())
