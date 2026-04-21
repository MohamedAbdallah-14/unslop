# Category 02 — RLHF and Alignment

How post-training shapes what an LLM sounds like. This category covers the full arc from proof-of-concept preference learning (2017) through the modern simplified pipeline (SFT -> DPO and its reference-free cousins), including the 2025 verifiable-reward GRPO wave and the February 2026 formal characterization of sycophancy amplification. The through-line: why the canonical RLHF voice sounds the way it does, and what levers exist to change it. Five angles cover the academic literature, industry engineering posts, open-source tooling and datasets, commercial vendors, and practitioner/forum discourse.

Last updated: April 2026.

## Angle Files

- [A-academic.md](A-academic.md) — 26 peer-reviewed and arXiv papers (2017-2026), from Christiano et al.'s proof-of-concept through InstructGPT, Constitutional AI, the full DPO family (DPO/IPO/KTO/ORPO/SimPO), the DPO variant survey (arXiv 2503.11701), DAPO, VAPO, scaling laws for overoptimization in direct alignment algorithms (arXiv 2406.02900), and the sycophancy amplification paper (arXiv 2602.01002).
- [B-industry.md](B-industry.md) — 20 industry posts and essays from Hugging Face, Chip Huyen, Nathan Lambert, Lilian Weng, Anthropic, OpenAI, DeepMind, and AI2; covers the five mechanisms that destroy voice during post-training, the GPT-4o sycophancy incident, Anthropic's deliberate character training stage, Claude's new 2026 constitution (23,000 words, CC0), the OpenAI Model Spec updates (February and December 2025), Anthropic's subliminal learning and reward-hacking-generalization findings (2025), and Nathan Lambert's RLHF Book.
- [C-opensource.md](C-opensource.md) — 17 repos and datasets covering trainer libraries (TRL v1 March 2026, OpenRLHF, veRL, Axolotl, LLaMA-Factory), alignment recipes (alignment-handbook, Safe-RLHF, DPO reference impl), and preference datasets (UltraFeedback, HelpSteer3, oasst2, LIMA, HH-RLHF, claude-constitution). Includes GRPO/DAPO/VAPO algorithm coverage and the subliminal learning risk for RLAIF pipelines.
- [D-commercial.md](D-commercial.md) — 23 vendors: preference-data providers (Scale AI — now 49% Meta-owned, June 2025; Surge AI — $1.2B+ revenue, seeking $1B raise at $15–25B valuation; Mercor, Contra Labs, Invisible Technologies), fine-tuning platforms (OpenPipe, Together, Fireworks, OpenAI DPO API), and alignment-as-a-service offerings; includes the Scale/Meta deal impact on market structure and antitrust scrutiny.
- [E-practical.md](E-practical.md) — 23 practitioner and forum sources: mode-collapse canon (Janus, Gwern), the shoggoth-and-mask framing (Scott Alexander), Karpathy's skeptical take on RLHF, the GPT-4o post-mortem, abliteration, activation steering, the Kulhari humanization tutorial, Unsloth preference docs, YouTube explainers, the LocalLLaMA creative-writing model consensus, the Shapira et al. sycophancy amplification paper (arXiv 2602.01002), Nathan Lambert's RLHF Book, and DeepSeek-R1/GRPO community resources.

## Synthesis

- [SYNTHESIS.md](SYNTHESIS.md) — the distilled synthesis across all five angles
- [INDEX.md](INDEX.md) — legacy category summary, superseded by SYNTHESIS.md, preserved for traceability
