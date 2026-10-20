"""Lexicon coding of model responses (fixed before any run; see PREREGISTRATION.md).

D markers  = reliance on high-infrastructure services/assumptions.
A markers  = adaptation to low-infrastructure conditions.
Coarse by design: validated afterwards against a manual audit of a stratified sample.
"""
import re

F = re.IGNORECASE

LEX = {
    # ---- high-infrastructure dependence (D) ----
    "pay_D": r"\b(credit|debit)[- ]cards?\b|\bvisa\b|\bmastercard\b|\bpaypal\b|\bstripe\b|\bapple pay\b|\bgoogle pay\b|\bvenmo\b|\bzelle\b|\bdirect debit\b|\bonline payments?\b",
    "net_D": r"\bstable (internet|connection|wi-?fi)\b|\bhigh[- ]speed\b|\bbroadband\b|\bfib(er|re)\b|\bstream(ing)?\b|\bzoom\b|\bgoogle meet\b|\bmicrosoft teams\b|\byoutube\b|\bnetflix\b|\bgoogle drive\b|\bdropbox\b|\bicloud\b|\bonedrive\b|\bcloud (storage|backup|service)s?\b|\baws\b|\bazure\b|\bgoogle cloud\b|\bcolab\b|\bkaggle\b|\bcoursera\b|\budemy\b|\bedx\b|\bkhan academy\b|\bvideo (call|conference)s?\b|\bwi-?fi\b",
    "power_D": r"\bovernight\b|\bleave (it|your \w+) (running|on|plugged)\b|\bkeep (it|your \w+) (running|plugged)\b|\bplugged in\b|\b24/7\b",
    "trans_D": r"\buber\b|\blyft\b|\bride[- ]?shar(e|ing)\b|\brent(ing)? a car\b|\bcar rental\b|\bsubway\b|\bmetro\b|\bamazon\b|\bdoordash\b|\binstacart\b|\bdelivery app\b|\bfedex\b|\busps\b|\bdhl\b|\bdrive (your|a) (own )?car\b|\bairbnb\b|\bflights?\b|\bairlines?\b|\bcar rentals\b",
    "cost_D": r"\$\s?\d|\busd\b|\bdollars?\b|€\s?\d|\beuros?\b|£\s?\d",
    "online_D": r"\bonline (form|portal|booking|appointment|application|store|shop|banking|bank)s?\b|\bbook (it |an appointment )?online\b|\bmobile app\b|\bapp store\b|\bgoogle maps\b|\blinkedin\b|\bindeed\b|\bglassdoor\b|\bjob boards?\b|\bbook(ing)? (a |your |the )?(hotels?|tickets?)\b",
    # ---- adaptation to low-infrastructure conditions (A) ----
    "pay_A": r"\bmobile money\b|\borange money\b|\bmoov money\b|\bcash\b|\bprepaid\b|\btontine\b|\bvouchers?\b",
    "net_A": r"\boffline\b|\bdownload(ed|ing)? (it |them |the \w+ )?once\b|\blow[- ]bandwidth\b|\bdata (bundle|plan|package)s?\b|\bcyber ?caf[eé]s?\b|\binternet caf[eé]s?\b|\boff[- ]peak\b|\blite (version|mode)\b|\bsd card\b|\busb (drive|stick|flash)\b|\bflash drive\b",
    "power_A": r"\bpower (cuts?|outages?|failures?)\b|\bblackouts?\b|\bload[- ]shedding\b|\bpower banks?\b|\bgenerators?\b|\bsolar\b|\bbackup battery\b|\binverter\b|\bsurge protector\b|\bwhen (the )?(electricity|power) (is|comes)\b",
    "trans_A": r"\bbus(es)?\b|\bminibus\b|\bbush taxi\b|\bmotorbikes?\b|\bmotorcycle taxi\b|\bmoped\b|\bscooter\b|\bshared taxi\b|\bon foot\b|\bwalk(ing)?\b|\bcarpool\b|\bbicycle\b",
    "cost_A": r"\bfcfa\b|\bcfa\b|\bxof\b|\blocal currency\b|\bfrancs?\b",
    "offline_A": r"\bin person\b|\bprinted\b|\bpaper (copy|copies|form|forms)\b|\bphysical (copy|copies)\b|\bvisit (the|a) (local )?(office|clinic|branch|shop|bank)\b|\bgo to the (office|clinic|bank|shop)\b",
    # ---- secondary: generic digital intensity (descriptive, NOT part of D_total) ----
    "digital_generic": r"\bonline\b|\binternet\b|\bwebsites?\b|\bapps?\b|\be-?mails?\b|\bvirtual\b|\bdownload\w*\b|\bportals?\b",
    # ---- meta ----
    "disclaimer": r"\b(depending on|depends on) (your )?(location|region|country|availability|where you live)\b|\bmay vary\b|\bvaries by (location|region|country)\b|\bcheck (local )?availability\b|\bwhere you live\b|\bin your (area|region|country|city)\b",
    "ctx_mention": r"\bburkina\b|\bouagadougou\b|\bboston\b|\bseoul\b|\bkorea\b|\bunited states\b|\bvillage\b|\brural\b|\bafrica\b|\bpower cuts?\b|\bmobile money\b|\blimited (internet|connectivity|data)\b|\bslow (internet|connection)\b|\bgiven (your|the) (situation|constraints?|context)\b",
}
_RX = {k: re.compile(v, F) for k, v in LEX.items()}
D_KEYS = [k for k in LEX if k.endswith("_D")]
A_KEYS = [k for k in LEX if k.endswith("_A")]


NEG = re.compile(r"\b(no|not|without|avoid\w*|don'?t|doesn'?t|do not|never|skip\w*|instead of|rather than|lack\w*|unable|can'?t|cannot|need(?:s|ed)? no|free of)\b", F)
MM = re.compile(r"mobile money", F)


def _count_d(text: str, rx) -> int:
    """Count D matches, ignoring mentions that restate or avoid the marker (negation in the 50 characters before,
    or 'online payment' in the same clause as mobile money)."""
    n = 0
    for m in rx.finditer(text):
        if NEG.search(text[max(0, m.start() - 50): m.start()]):
            continue
        if m.group(0).lower().startswith("online payment") and MM.search(text[max(0, m.start() - 80): m.end() + 80]):
            continue
        n += 1
    return n


def code_text(text: str) -> dict:
    out = {k: (_count_d(text, rx) if k in D_KEYS else len(rx.findall(text))) for k, rx in _RX.items()}
    out["words"] = len(re.findall(r"\w+", text))
    out["D_total"] = sum(out[k] for k in D_KEYS)
    out["A_total"] = sum(out[k] for k in A_KEYS)
    return out


if __name__ == "__main__":
    demo = "No international credit card, so no online subscriptions. Use Wi-Fi, LinkedIn and book flights. Use a credit card on Coursera, stream the lectures overnight. Depending on your location it may vary. Or pay by mobile money and download once for offline use."
    print(code_text(demo))
