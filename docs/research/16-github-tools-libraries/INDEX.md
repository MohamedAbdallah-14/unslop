# Category 16 — GitHub Tools and Libraries

This category maps the open-source tooling layer of AI-text humanization: GitHub repos with accompanying academic papers, Claude Code / OpenCode skill packs, commercial API competitors, and the practitioner discussion around all of them. It covers the landscape from NeurIPS-published attack systems to 14k-star Claude skills to self-hosted paraphrasers, including honest assessments of what actually moves detector scores versus what is README marketing.

## Angle files

- [A-academic.md](./A-academic.md) — ~23 research-grade repos with peer-reviewed papers (DIPPER, HMGC, HUMPA, StealthRL, AuthorMist, GradEscape, SICO, RAFT, CoPA, MASH, ANTISLOP, StyleRemix, TH-Bench, MGTBench, DAMAGE); mechanism lineage 2023–2026 and evaluation scaffolding. New 2025–2026 additions: MASH (arXiv 2601.08564), ANTISLOP (ICLR 2026 arXiv 2510.15061), BART/Mistral style corpus (arXiv 2604.11687), DAMAGE (arXiv 2501.03437).
- [B-industry.md](./B-industry.md) — Blog, listicle, and tutorial coverage: curated lists, HuggingFace T5/Pegasus tutorials, critical reviews, and how the market splits between pipeline engines, Claude skills, and thin API wrappers. Updated with Turnitin August 2025 anti-humanizer announcement, Walter Writes surge, AuraWrite emergence.
- [C-opensource.md](./C-opensource.md) — Tiered catalog of ~42 named "humanize AI text" repos, from the dominant `blader/humanizer` (~14.7k stars) through hackathon apps and watermark-evasion scripts to historical stylometry tools. New 2025–2026 additions: jpeggdev/humanize-writing, lguz/humanize-writing-skill, aaaronmiller/humanize-writing, sam-paech/auto-antislop, antislop-vllm. Aboudjem/humanizer-skill updated to 37 patterns; StealthHumanizer now corpus-trained on 10K papers.
- [D-commercial.md](./D-commercial.md) — Commercial SaaS and self-hostable alternatives: Undetectable.ai, WriteHuman, StealthGPT, HumanizerPro, AI Humanizer API, Humaniser, Apify, Deceptioner, OSS counterparts. **New 2025–2026:** Walter Writes, AuraWrite AI, updated pricing for StealthGPT. Critical new context: Turnitin August 2025 anti-humanizer update disrupted existing bypass-rate claims.
- [E-practical.md](./E-practical.md) — Reddit threads (r/LocalLLaMA, r/BypassAiDetect, r/SEO), Hacker News launches, dev.to tutorials, and the `blader/humanizer` issue #82 engineering debate about whether prompt-only humanization is statistically self-defeating. Updated with ANTISLOP ICLR 2026 formalization and post-Turnitin market context.

## Synthesis and legacy

- [SYNTHESIS.md](./SYNTHESIS.md) — The distilled synthesis across all five angles.
- [INDEX.md](./INDEX.md) — Legacy category summary — superseded by SYNTHESIS.md, preserved for traceability.
