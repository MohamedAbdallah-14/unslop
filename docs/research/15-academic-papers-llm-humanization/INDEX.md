# Category 15 — Academic Papers on LLM Humanization

This category covers the academic and industry literature on making LLM output read as human — from detector-evasion attacks and stylometric studies to the preference-optimization canon by which frontier labs train personality and voice. It spans peer-reviewed papers, commercial-lab whitepapers, open-source implementations, and practitioner discussion threads, weighted toward 2023–2026.

**Last updated: April 2026.** New papers added in this update: TempParaphraser (EMNLP 2025), DivEye / Diversity Boosts Detection (TMLR 2026, arXiv:2509.18880), SHIELD / Beyond Easy Wins benchmark (arXiv:2507.15286), Interpretable Stylistic Variation across Genres (arXiv:2604.14111), Humanizing Machines / Multi-Level Anthropomorphism Framework (EMNLP 2025, arXiv:2508.17573), Humanizing LLMs psychological survey (arXiv:2505.00049), Why AI-Generated Text Detection Fails / XAI analysis (arXiv:2603.23146), and Kalemaj et al. encoder-decoder style transfer details updated with contraction-rate finding.

## Angle files

- [A-academic.md](./A-academic.md) — Core academic survey: canonical humanization/evasion attacks (DIPPER, RADAR, Adversarial Paraphrasing, RAFT, MASH, StealthRL, AuthorMist, TempParaphraser), detection baselines (including DivEye surprisal-variance, SHIELD hardness-aware), benchmarks, stylometric studies (including Rallapalli et al. 2026 cross-genre analysis), and reproducibility grades for every entry.
- [B-industry.md](./B-industry.md) — Industry and whitepaper summaries: Anthropic, OpenAI, Hugging Face blogs, Sebastian Raschka, Nathan Lambert, Lilian Weng, Jay Alammar, em-dash/"AI slop" practitioner discourse, plus Humanizing Machines (EMNLP 2025) and the Dong et al. psychological-alignment survey.
- [C-opensource.md](./C-opensource.md) — Papers-with-code repositories: 27 repos across four camps — humanizers (including TempParaphraser), style-obfuscation tools, humanness metrics (MAUVE, HUSE), and detection/benchmark suites (including DivEye) — with star counts, licenses, and headline numbers.
- [D-commercial.md](./D-commercial.md) — Commercial research lab publications: 24 papers from Anthropic, OpenAI, AI2, Cohere For AI, EleutherAI, LAION, Scale AI, NVIDIA, Databricks, and Meta FAIR, documenting the RLHF → RLAIF → RLVR → Rule-Based Rewards drift.
- [E-practical.md](./E-practical.md) — Paper-discussion threads: 17 threads from Hacker News, Reddit ML, LessWrong, Anthropic/HF paper pages, and practitioner reports, covering watermarking debates, register-detection framing, sycophancy, institutional detection retreat, and the folk humanizer pipelines that practitioners already ship.

## Synthesis and legacy files

- [SYNTHESIS.md](./SYNTHESIS.md) — The distilled synthesis across all five angles: executive summary, cross-angle themes, top sources, key techniques, controversies, emerging trends, open questions, and a recommended reading order.
- [INDEX.md](./INDEX.md) — Legacy category summary — superseded by SYNTHESIS.md, preserved for traceability.
