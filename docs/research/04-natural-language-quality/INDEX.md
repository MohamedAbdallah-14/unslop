# Category 04 — Natural Language Quality

This category covers the mechanics of making LLM output read like human writing and not like machine text. It spans decoding algorithms (how tokens are sampled), training-time causes of "AI voice" (RLHF, likelihood objectives), distributional evaluation metrics (MAUVE, BERTScore, HLB), detection signals (perplexity curvature, burstiness), adversarial humanization techniques, and the commercial and community tooling built around all of the above.

## Angle Files

- [A-academic.md](A-academic.md) — 20 papers from arXiv/ACL/EMNLP/ICLR/NeurIPS/ICML/TACL/TMLR/Computational Linguistics covering decoding theory (nucleus, typical, min-p, contrastive, mirostat), training-time interventions (unlikelihood), evaluation metrics (MAUVE, BERTScore, HLB), AI-text detection (DetectGPT, Ghostbuster), adversarial humanization (Cheng et al. 2025), and LLM-judge bias (CALM framework, Gao et al. 2025)
- [B-industry.md](B-industry.md) — 19 engineering blog posts and essays from Hugging Face, OpenAI, Anthropic, Thoughtworks, European Commission, and independent researchers (Willison, Weng, Raschka, Alammar, Labonne, Reiter) on decoding tutorials, RLHF as the root cause of "AI voice," sycophancy postmortems, character training, Custom Styles (Anthropic 2025), the "slop" discourse, and EU AI Act watermarking requirements (Article 50, effective August 2026)
- [C-opensource.md](C-opensource.md) — GitHub repos and PRs covering the full OSS sampler stack (llama.cpp, ExLlamaV2, vLLM, Aphrodite, SGLang, text-generation-webui, KoboldCPP), named sampling algorithms (DRY, XTC, top-nσ, dynamic temperature), humanization-specific tooling (antislop-sampler + auto-antislop, ICLR 2026 accepted), published antislop fine-tuned models, and the evaluation stack (MAUVE lib, EQ-Bench Creative Writing v3 with Slop/Repetition columns + longform leaderboard, lmscan)
- [D-commercial.md](D-commercial.md) — 15 commercial products categorized into three humanization archetypes: voice-capture/style-example tools (Sudowrite, Jasper, Lex, Notion, Grammarly, Anyword), vertical fine-tunes (Sudowrite Muse, BrandWell, Jamba), and post-hoc detection-bypass rewriters (Undetectable.ai, HIX Bypass, QuillBot, StealthGPT); includes EU AI Act compliance exposure for bypass tools (effective August 2026) and frontier model creative writing quality comparisons (Claude Opus 4.6 vs GPT-5.4 vs Gemini 2.5)
- [E-practical.md](E-practical.md) — Community guides, Reddit field reports, HN threads, and PR design arguments from r/LocalLLaMA, r/accelerate, kalomaze, AlpinDale, smcleod, and SillyTavern preset authors; converges on a three-sampler naturalness recipe (min-p + DRY + temperature-last) with concrete parameter tables; updated with top-nσ disabled-by-default caveat and auto-antislop pipeline

## Synthesis & Legacy

- [SYNTHESIS.md](SYNTHESIS.md) — the distilled synthesis across all five angles
- [INDEX.md](INDEX.md) — legacy category summary — superseded by SYNTHESIS.md, preserved for traceability
