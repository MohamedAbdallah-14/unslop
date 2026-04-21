# Category 01 — Prompt Engineering for Humanization

This category covers how prompts alone can shape LLM outputs to sound and reason more like a human, without fine-tuning the base model. It spans natural-language style instructions, persona and role prompting, few-shot exemplars, voice calibration from user writing samples, system-prompt style contracts ("anti-slop"), multi-stage humanization pipelines, detector-evasion paraphrase chains, and the measurement of "humanness." The category sits at the intersection of academic style-transfer research, industry voice engineering, community anti-GPTism practice, and the commercial humanizer arms race with AI detectors.

## Angle Files

- [A-academic.md](./A-academic.md) — Peer-reviewed and pre-print literature on prompt-based style transfer (Reif et al. ACL 2022, TinyStyler EMNLP 2024), persona/role prompting and its costs (Gupta et al. ICLR 2024, Hu & Collier ACL 2024, Zheng et al.), adversarial paraphrase humanizers (DIPPER NeurIPS 2023, CoPA EMNLP 2025, Adversarial Paraphrasing 2025, MASH arXiv 2601.08564 January 2026), stylometric fingerprints (Sun et al. arXiv 2502.12150), humanness measurement (HumT/DumT, Cheng et al. 2025), and cognitive modeling of human expression (HumanLLM arXiv 2601.10198, Humanizing LLMs survey arXiv 2505.00049).
- [B-industry.md](./B-industry.md) — Engineering blogs, lab cookbooks, and individual essayists (Simon Willison, Eugene Yan, Gwern, Katie Parrott at Every.to, OpenAI Prompt Personalities cookbook, Anthropic's prompt library) on voice engineering, style guides as versioned artifacts, anti-slop system prompts, the shift from prompt engineering to context engineering, and the ethics of letting LLMs speak in a human's first person.
- [C-opensource.md](./C-opensource.md) — GitHub humanizer skills (`blader/humanizer` ~14.7K★, `adenaufal/anti-slop-writing`, `aaaronmiller/humanize-writing`), anti-slop CI/PR gating (`peakoss/anti-slop` GitHub Action 2026), detector-evasion tooling (Unicode space attacks, Spanish round-trips, keystroke simulation), persona libraries (`f/awesome-chatgpt-prompts` ~160K★), prompt optimization frameworks (DSPy, Guidance, LMQL, promptfoo), and frontier-model system-prompt leak archives (38.6K★ and 14.5K★).
- [D-commercial.md](./D-commercial.md) — Paid humanizer SaaS (Undetectable.ai, StealthGPT, StealthWriter, Deceptioner, Phrasly, and others; 2026 performance leaders: Ryter Pro at 97% GPTZero bypass, Humaniser at 93% composite), Turnitin's February 2026 update adding AI-paraphrased detection, mainstream writing-suite humanizer sub-features (Grammarly Humanizer Agent, Jasper Brand Voice, QuillBot, Writesonic), prompt marketplaces (PromptBase at $2.99–$6.99/prompt), and LLMOps platforms used to version and evaluate humanization prompts in production (PromptLayer, LangSmith, Humanloop, Vellum, Braintrust).
- [E-practical.md](./E-practical.md) — Reddit (r/ChatGPT, r/ChatGPTPromptGenius, r/LocalLLaMA), Hacker News, dev.to, and practitioner GitHub corpora on anti-slop ban-lists, the minimalist single-directive counterposition, the 2026 shift toward context engineering framing, voice-sample ingestion ("Frankenstein method"), burstiness engineering, sycophancy breakers (the "Bernardo" frame, blunt-persona assignment), and inference-time sampling as a fallback when prompt-only humanization fails.

## Full Synthesis

- [SYNTHESIS.md](./SYNTHESIS.md) — The distilled synthesis across all five angles: cross-cutting themes, top sources, key techniques, controversies, emerging trends, and open research gaps.

## Legacy Summary

- [INDEX.md](./INDEX.md) — Legacy category summary — superseded by SYNTHESIS.md, preserved for traceability.
