# Lexicon changelog (freeze protocol, step 2)

All changes were decided from the **dev split of S1 only** (27 dependent scenarios, 9 controls). No test-split, real-prompt or probe output was inspected before the freeze. The frozen version is the commit tagged `lexicon-frozen`.

## Changes from the pre-registered v1 lexicon
1. **Negation-aware D counting.** In the dev outputs under constraint conditions the model often restates the stated constraint ("No international credit card", "avoid platforms that need credit cards"). These were counted as high-infrastructure dependence. A D match is now ignored when a negation or avoidance cue (no, not, without, avoid, don't, instead of, rather than, lack, unable, can't, cannot, free of...) occurs in the 50 characters before it. On dev, the payment D rate under constraints-only fell from 0.417 to 0.089 per 100 words.
2. **"online payment" next to "mobile money".** If the match is within 80 characters of "mobile money" (restating "online payments are only possible through mobile money"), it is ignored.
3. **Added D terms** that the dev outputs showed were missing: `wi-fi` (network), `LinkedIn / Indeed / Glassdoor / job boards` and booking hotels or tickets (online services), `flight(s) / airline(s) / car rentals` (transport).
4. **Secondary metric `digital_generic`** (online, internet, website, app, email, virtual, download, portal), reported descriptively as "digital intensity". It is **not** part of `D_total` and not used in primary contrasts.
5. **Unit tests** (`tests/test_coding.py`), including a check against control characters in `src/coding.py`. A character-escaping error introduced during editing had turned `\b` into backspace characters in two regular expressions; it was found by inspecting the file bytes before any analysis, repaired, and is now guarded by the test.

## Known limitations left unchanged
- Explicit power-related dependence is almost never written out by the model (near-zero `power_D` in every condition), so the lexicon cannot measure it; the probes and the blind audit are the evidence for power.
- A markers cover explicit low-infrastructure accommodations only. Localisation (naming local markets, cooperatives) is not counted as adaptation.
- Counting is lexical: it cannot judge whether a mentioned service is used reliance or a side remark; this is what the blind audit measures.
- Responses to template B and to real prompts are mostly truncated at 500 tokens, so rates describe roughly the first 350 words.
