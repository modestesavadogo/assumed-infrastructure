# Third-party material and licenses

This is a practical summary, not legal advice. Check the original licenses before reuse.

## Created for this study
Scenarios, context sentences, probes, manual codes, figures, tables and documents: **CC BY 4.0** (https://creativecommons.org/licenses/by/4.0/). Source code: **MIT** (see `LICENSE`).

## OpenAssistant Conversations (oasst1)
`data/real_prompts.csv` contains 274 user prompts selected from `OpenAssistant/oasst1` (https://huggingface.co/datasets/OpenAssistant/oasst1), released under **Apache-2.0**. Reference: Köpf et al., "OpenAssistant Conversations - Democratizing Large Language Model Alignment", 2023. Prompts are included unchanged with their `message_id`; this attribution applies to that file, which stays under Apache-2.0.

## Models whose outputs are included
Model outputs (`generations.jsonl`, `probes.jsonl`) were produced by:
| model | license | source |
|---|---|---|
| Qwen/Qwen3-4B-Instruct-2507 | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 |
| Qwen/Qwen3-1.7B | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-1.7B |
| microsoft/Phi-4-mini-instruct | MIT | https://huggingface.co/microsoft/Phi-4-mini-instruct |
| Llama-3.2-3B-Instruct | Llama 3.2 Community License | official Meta weights via Kaggle Models (`metaresearch/llama-3.2`, Transformers, 3b-instruct, v1) |

**Built with Llama.** Llama 3.2 is licensed under the Llama 3.2 Community License, Copyright (c) Meta Platforms, Inc. All Rights Reserved. The Llama 3.2 license and Acceptable Use Policy apply to the use of Llama materials and may impose conditions on how Llama outputs are used (for example when used to improve other models). Review https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/LICENSE before reusing the Llama outputs for training. No model weights are distributed here.

## Tools and libraries
Python, pandas, NumPy, SciPy, matplotlib, Hugging Face Transformers, PyTorch, Accelerate (each under its own permissive license).

## Content warning on model outputs
Responses contain model errors and hallucinations (invented institutions, apps, prices, URLs). They were not fact-checked and must not be used as advice.
