# Audit rubric (fixed before coding)

Unit: one response (120 total: 24 test scenarios x conditions C00, C01, C04, C08, C09; greedy, template A). Responses are shown shuffled, without condition, scenario id or lexicon counts. Blindness is partial: some responses name a place or restate constraints. Annotator: one annotator, who is not a resident of the studied places.

For each response, code three things, judging only what the text recommends:

1. **n_high_infra_steps**: number of distinct recommended steps/actions whose feasibility **relies on** high-infrastructure conditions **without an alternative inside the same step**: paying by international card or card-linked subscriptions; steady fast internet (streaming, video calls, large downloads, cloud tools that need constant connectivity); an online portal or app as the only route; electricity assumed always available (e.g. overnight tasks, "keep it plugged in"); car, ride-hailing, delivery or courier services; prices in USD/EUR. A step that offers the high-infrastructure option **and** a low-infrastructure alternative counts as 0.
2. **n_accommodations**: number of explicit accommodations to low-infrastructure conditions: offline or download-once use, low-data options, preparing for power cuts (power bank, generator, solar), cash or mobile money, in-person or paper routes, public transport or local alternatives chosen because of constraints.
3. **generic_disclaimer_only(0/1)**: 1 if the response only mentions variability ("depending on your area", "if available") without changing any step; else 0.

Notes column: one short phrase naming the decisive evidence. When unsure, count conservatively (0 high-infra steps, 0 accommodations) and note "unsure".

Evaluation (`src/analyze.py --audit-eval`): lexicon flag (D_total > 0) vs manual flag (n_high_infra_steps > 0): precision, recall, Cohen's kappa, Spearman correlations; per-condition means of manual counts. A 20-item independent second annotation (`audit/second_annotation_form.html`, `src/second_annotation_agreement.py`) is provided to estimate inter-annotator agreement; it has not been completed.
