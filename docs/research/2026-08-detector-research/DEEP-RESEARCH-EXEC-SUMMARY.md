# Deep Research Executive Summary — August 2026

**Source:** parallel-cli ultra-fast run `trun_31fbe3dec0e84a84b4ad73233f46994a`  
**Completed:** ~6 minutes  
**Full metadata + citations:** [`ai-detection-landscape-aug2026.json`](./ai-detection-landscape-aug2026.json)  
**Monitor URL:** https://platform.parallel.ai/play/deep-research/trun_31fbe3dec0e84a84b4ad73233f46994a

---

## Key findings (aligned with sub-agent review)

1. **DivEye / temporal features** — Adding temporal dynamics to static surprisal stats raises accuracy 74.25%→78.15% and AUROC 0.82→0.88. Detectors should evaluate variability and higher-order features, not average perplexity alone.

2. **AdaDetectGPT** — Reports 12.5–37% AUC advantage over Fast-DetectGPT. Report held-out domains, models, and thresholds — not one pooled score.

3. **Binoculars** — Strong on GPT-3/4 in paper eval, but authors note gaps on larger models and bypass studies. Treat benchmark numbers as conditional.

4. **Adversarial paraphrasing** — 98.96% T@1%FPR reduction vs Fast-DetectGPT; ~87.88% average across detector set. Red-team at fixed low FPR.

5. **SIRA watermarking** — ~100% attack success on seven schemes at ~$0.88/M tokens, black-box. Watermarks are not unassailable proof.

6. **StealthRL** — 99.9% ASR at 1% FPR but lower semantic quality. Measure meaning preservation, not evasion alone.

7. **ESL fairness** — ~61% false-positive rate on TOEFL essays (Liang). Never make punitive authorship decisions from detector score alone.

8. **Turnitin July 20, 2026** — English AI-writing report changed; paraphrase/bypasser detection retained. Record product version and language.

9. **EU AI Act Art. 50** — Effective 2 August 2026; grace until 2 December 2026 for certain pre-existing marking obligations.

10. **Ethical framing** — Legitimate: clearer, more specific, recognizably yours. Not legitimate: optimizing to conceal AI authorship or defeat assessment controls.

---

*Feeds into [`UPDATE-PLAN-2026-08.md`](./UPDATE-PLAN-2026-08.md).*
