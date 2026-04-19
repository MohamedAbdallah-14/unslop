# Research Status — How This Compendium Was Produced

**Project.** Humazier — Humanizing the Output and Thinking of AI Models.
**Date of compilation.** Sunday, 19 April 2026.
**Status.** Complete. 20 categories × 5 angles + 20 category indices + 1 master index = **122 markdown files**.

## Method Summary

This research program was produced by a fleet of **121 specialist subagents** coordinated by a main orchestrating agent, in a three-tier fan-out / fan-in workflow:

1. **Tier 1 — 100 angle researchers.** Each of 20 categories was decomposed into five non-overlapping research angles:
   - `A-academic.md` — peer-reviewed literature, arXiv pre-prints, survey papers, benchmarks.
   - `B-industry.md` — first-party engineering blogs, whitepapers, essays from labs and product teams.
   - `C-opensource.md` — GitHub repositories, cookbooks, skill packs, reference implementations.
   - `D-commercial.md` — commercial products, SaaS tools, case studies, pricing, API surfaces.
   - `E-practical.md` — Reddit, Hacker News, dev.to, YouTube, LinkedIn, and other practitioner discourse.

   One subagent was dispatched per (category × angle) cell, producing a stand-alone deep-dive with cited sources.

2. **Tier 2 — 20 category summarizers.** One subagent per category consumed its five angle files and produced a cross-angle `INDEX.md` with a standard shape: Scope · Executive Summary · Cross-Angle Themes · Top Sources (papers / posts / OSS / commercial / community) · Key Techniques & Patterns · Controversies & Debates · Emerging Trends · Open Questions & Research Gaps · How This Category Fits · Recommended Reading Order · File Index.

3. **Tier 3 — 1 master indexer.** This tier read all 20 `INDEX.md` files and produced the top-level [`README.md`](./README.md) — the cross-category synthesis, mega-themes, humanization stack, top picks, controversies, trends, gaps, practical playbook, full category index, glossary, and reading paths.

All subagent outputs are preserved as-is on disk. The master indexer does not overwrite category-level work; it only cross-cuts.

## File Layout

```
docs/research/
├── README.md                          ← master cross-category synthesis (start here)
├── _STATUS.md                         ← this file
├── 01-prompt-engineering-humanization/
│   ├── INDEX.md                       ← category summary
│   ├── A-academic.md
│   ├── B-industry.md
│   ├── C-opensource.md
│   ├── D-commercial.md
│   └── E-practical.md
├── 02-rlhf-and-alignment/             (same structure)
├── 03-persona-and-character-design/
├── 04-natural-language-quality/
├── 05-ai-text-detection-and-evasion/
├── 06-chain-of-thought-reasoning/
├── 07-emotional-intelligence-empathy/
├── 08-conversational-dialogue-systems/
├── 09-bias-fairness-ethics/
├── 10-style-transfer-voice/
├── 11-theory-of-mind/
├── 12-cognitive-architectures/
├── 13-anthropomorphism-user-perception/
├── 14-creative-writing-storytelling/
├── 15-academic-papers-llm-humanization/
├── 16-github-tools-libraries/
├── 17-industry-blogs-case-studies/
├── 18-commercial-humanizer-tools/
├── 19-agentic-autonomous-thinking/
└── 20-memory-personalization/
```

Each of the 20 category directories is self-contained: read an `INDEX.md` for the category synthesis, then descend into any of its five angle files for the evidence chain.

## How to Navigate

- **First-time readers.** Start with [`README.md`](./README.md) — specifically the *Master Executive Summary*, *Cross-Category Mega-Themes*, and *The Humanization Stack* sections. They are designed to orient a new reader in under 30 minutes.
- **Practitioners with a specific task.** Jump to the *How to Navigate / Reading Paths* section of `README.md`. Six personas are pre-wired: humanized-chatbot builder, detection-evasion researcher, humanizer-SaaS product manager, humanization-harms ethicist, agent builder, creative writing / narrative designer.
- **Readers chasing a specific claim.** Every claim in `README.md` is traceable: mega-themes name the categories they span; top picks name the originating angle file. Follow the link; then follow the source links inside the angle file.
- **Readers doing their own synthesis.** Read the 20 `INDEX.md` files directly — each is 5–15 KB and designed to stand alone. The angle files are the full evidence substrate when deeper verification is needed.

## Known Limitations

- **Cutoff.** Sources cut off at the compilation date (19 April 2026); anything published later is not represented.
- **Self-reported vendor claims.** Commercial case studies and humanizer vendor benchmarks are flagged where independent audits contradict them, but not every claim has been independently verified.
- **English-language bias.** Nearly all primary sources are English; multilingual humanization research is documented but under-represented (named as a gap in Cats 07, 17, 18, 20).
- **Fast-moving subfields.** Agentic autonomy (Cat 19), memory infrastructure (Cat 20), and the humanizer SaaS market (Cat 18) are the three fastest-moving areas; expect meaningful drift on a 3–6-month horizon.

For the substantive synthesis, see [`README.md`](./README.md).
