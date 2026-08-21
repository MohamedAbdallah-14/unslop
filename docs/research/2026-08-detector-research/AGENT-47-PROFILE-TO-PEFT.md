# Agent #47 — Profile-to-PEFT Voice (Hypernetwork LoRA Personalization)

**Topic:** Personal writing profile → PEFT fine-tuning for voice matching — P2P framework, OPPU lineage, StyleTunedLM/TinyStyler comparison, unslop Phase 3 path  
**Prepared:** 2026-08-19  
**Status:** Complete research memo

---

## Executive summary

**Profile-to-PEFT (P2P)** is the ACL 2026 long-paper answer to a scalability problem unslop's `/unslop voice-match` will eventually hit: **prompt + numeric stylometry cannot encode idiolect into model weights**. Tan et al. (*Instant Personalized Large Language Model Adaptation via Hypernetwork*, arXiv 2510.16282, ACL 2026) train a **hypernetwork** that maps a user's **natural-language profile** (history summary + retrieved interactions) to a **full LoRA adapter set** in **one forward pass** — no per-user gradient steps at deployment.

This is **not** a slop stripper or detector evader. It is **parametric personalization infrastructure**: the middle layer between (a) unslop's current `stylometry.py` + `style_memory.py` prompt conditioning and (b) oracle **One-PEFT-Per-User (OPPU)** fine-tuning that Wang et al. (*Catch Me If You Can?*, EMNLP 2025) cite as the practical alternative to prompt-only imitation.

**Headline numbers from the paper:**

| Claim | Number | Context |
|-------|--------|---------|
| Deployment speedup vs OPPU | **33×** | 0.57 s/user vs 20.44 s/user (LoRA OPPU) |
| vs prompt baselines | Beats RAG/PAG/Full History on avg | LaMP + LongLaMP random split |
| vs OPPU (oracle) | **Better average** classification + generation | Despite OPPU training on test-user history |
| OOD users | Strong vs MT-LoRA/OPPU | k-means-isolated user clusters |
| Open-ended gen (LLM judge) | **2.21** (PR random) vs base **1.71** | GPT-4o Prometheus 1–5 scale |
| Training amortization | ~**1,450 users** | One-time hypernetwork cost breaks even vs OPPU |
| User diversity > quantity | F1 **0.508 → 0.560** (OOD) | 10 → 50 user clusters; flat from 20%–100% user count |

**Critical caveat for unslop:** P2P evaluates **preference personalization** (LaMP movie tags, tweet paraphrase, Reddit posts) — **not** Catch Me If You Can's four-metric authorship battery (AA/AV/style model/GPTZero). StyleTunedLM (Liu et al., INLG 2024) is the direct **authorship-PEFT** citation: LoRA on Llama-2-7B reaches **87.9%** BERT authorship classifier accuracy vs **69.3%** 5-shot prompting. P2P generalizes the *deployment pattern*; StyleTunedLM validates the *voice objective*.

**unslop verdict:** Keep voice-match as prompt + numeric profile (Phase 1–2). Treat P2P as the **Phase 3+ architecture spec** for a local hypernetwork that maps `StyleProfile` + sample excerpts → LoRA weights, trained on a diverse author corpus (not shipped in-plugin). Do **not** claim voice-match today equals P2P. Cite P2P + StyleTunedLM + TinyStyler as the evidence stack that specialized adaptation beats prompting on informal personal writing.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **P2P arXiv** | https://arxiv.org/abs/2510.16282 |
| **P2P arXiv HTML** | https://arxiv.org/html/2510.16282 |
| **P2P ACL Anthology** | https://aclanthology.org/2026.acl-long.1081/ |
| **P2P ACL PDF** | https://aclanthology.org/2026.acl-long.1081.pdf |
| **P2P DOI** | https://doi.org/10.18653/v1/2026.acl-long.1081 |
| **Project page** | https://zhaoxuan.info/p2p.github.io/ |
| **GitHub (TamSiuhin/P2P)** | https://github.com/TamSiuhin/P2P |
| **HuggingFace checkpoint** | https://huggingface.co/Zhaoxuan/P2P_ckpt |
| **Built on Text-to-LoRA** | https://github.com/SakanaAI/text-to-lora |

**Authors:** Zhaoxuan Tan, Zixuan Zhang, Haoyang Wen, Zheng Li, Rongzhi Zhang, Pei Chen, Fengran Mo, Zheyuan Liu, Qingkai Zeng, Qingyu Yin, Meng Jiang (Notre Dame + Amazon). **Venue:** ACL 2026 Long Papers, pp. 23557–23580.

### Lineage — same research group

| Paper | URL | Role |
|-------|-----|------|
| **OPPU — Democratizing LLMs via Personalized PEFT** (EMNLP 2024) | https://arxiv.org/abs/2402.04401 · https://aclanthology.org/2024.emnlp-main.372/ · https://github.com/TamSiuhin/OPPU | Oracle baseline: one LoRA per user, trained on user history |
| **Personalized Pieces** (EMNLP 2024) | https://aclanthology.org/2024.emnlp-main.6459/ | Collaborative multi-user PEFT |
| **LaMP benchmark** | https://aclanthology.org/2024.acl-long.7370/ | Primary eval suite |
| **LongLaMP** | https://arxiv.org/abs/2407.11016 | Long-form personalized generation |

### Voice / style PEFT (direct unslop comparables)

| Paper | URL | Relationship |
|-------|-----|--------------|
| **StyleTunedLM — Liu et al.** (INLG 2024) | https://arxiv.org/abs/2409.04574 · https://aclanthology.org/2024.inlg-main.34/ · https://github.com/cauchy221/StyleTunedLM | Per-author LoRA on Llama-2-7B; **87.9%** authorship classifier vs **69.3%** 5-shot |
| **TinyStyler** (EMNLP 2024 Findings) | https://arxiv.org/abs/2406.15586 · https://aclanthology.org/2024.findings-emnlp.781/ · https://github.com/zacharyhorvitz/tinystyler | 800M LM + authorship embeddings; beats GPT-4 on authorship transfer |
| **Catch Me If You Can?** (EMNLP 2025) | https://arxiv.org/abs/2509.14543 · `AGENT-43-CATCH-ME-IF-YOU-CAN.md` | Prompt-only ceiling; cites PEFT as excluded superior path |
| **Text-to-LoRA (T2L)** (ICML 2025) | https://arxiv.org/abs/2506.06105 · https://github.com/SakanaAI/text-to-lora | Task-description → LoRA hypernetwork; P2P codebase fork |
| **HyperLoRA** (EMNLP 2024 Findings) | https://aclanthology.org/2024.findings-emnlp.16376/ | Few-shot → LoRA; cross-task, not user-level |
| **ZeroStylus** | `AGENT-48-ZEROSTYLUS.md` | Zero-shot discourse templates; orthogonal macro layer |

### Practitioner / secondary coverage

| Source | URL | Notes |
|--------|-----|-------|
| Emergent Mind topic page | https://www.emergentmind.com/topics/profile-to-peft-framework | Architecture summary |
| Pivot News (industry) | https://pivotnews.ai/five/profile-to-peft-instant-llm-adaptation | Deployment economics framing |
| PaperNotes ACL2026 | https://en.papernotes.org/ACL2026/llm_safety/instant_personalized_large_language_model_adaptation_via_hypernetwork/ | Concise mechanism note |

**Community debate:** No substantive HN/Reddit thread found (Aug 2026). Discussion is academic + industry-blog only. Skepticism in paper itself: LLM-as-judge on open-ended tasks, no authorship-verification eval, hypernetwork training cost (~27k s one-time on 80G A100).

### unslop internal references

| Resource | Path |
|----------|------|
| Voice-match spec + Known Limitation | `skills/unslop/SKILL.md` §voice-match |
| Stylometry extraction | `unslop/scripts/stylometry.py` |
| Numeric style memory | `unslop/scripts/style_memory.py` |
| Voice targets in LLM prompt | `unslop/scripts/humanize.py` (`_build_voice_block`, `_format_voice_targets`) |
| Voice vs detector axes | `docs/research/2026-08-detector-research/AGENT-52-VOICE-MATCH-STYLOMETRIC-LIMITS.md` |
| Prompt-only ceiling | `docs/research/2026-08-detector-research/AGENT-43-CATCH-ME-IF-YOU-CAN.md` |
| Cat 10 synthesis | `docs/research/10-style-transfer-voice/SYNTHESIS.md` |

---

## Mechanism

### Problem: One-PEFT-Per-User (OPPU) does not scale

OPPU (Tan et al., EMNLP 2024) assigns each user `u` a personal LoRA adapter `ΔW_u`, trained by:

```
ΔW*_u = argmin_{ΔW} L_SFT(Ψ ⊕ ΔW, H^<t_u)
```

Works well for preference tasks (LaMP). Fails at **millions of users** or **real-time preference drift** — every new user or update requires ~20 s of gradient steps and stored adapter weights.

### P2P solution: profile → hypernetwork → LoRA

```
User history H_u
       │
       ├─► Profiler(base LLM) ──► summary s_u
       └─► BM25 retrieve top-k ──► relevant history
                    │
                    ▼
         profile text p_u = s_u || R(x_u, H_u, k)
                    │
                    ▼
         Enc(·) frozen embedder ──► e_u  (Qwen3-Emb-4B default)
                    │
     for each (module m, layer l):
         φ^{m,l}_u = e_u || E_mod[m] || E_dep[l]
                    │
                    ▼
         MLP hypernetwork f_θ(φ) ──► flatten ──► (A^{m,l}_u, B^{m,l}_u)
                    │
                    ▼
         h = W_0 x + B A x     (frozen base + generated LoRA)
```

**Training objective** (population of users `U`):

```
L(θ) = E_{u~U} L_SFT(Ψ ⊕ Gen_θ(p_u), H^≥t_u)
```

At deployment: **single forward pass** through `Gen_θ` for unseen user `u ∉ U_train`. No gradients. Adapters plug into frozen Qwen2.5-7B-Instruct (paper default).

### Profile encoding — what "profile" means here

P2P profiles are **natural-language preference summaries**, not unslop's numeric `StyleProfile`:

| Component | Source | Ablation finding |
|-----------|--------|------------------|
| User summary `s_u` | Base LLM over full history | **Most critical** — summary-only ≈ full profile (Acc 0.562 vs 0.581 OOD) |
| Retrieved history | BM25 top-k (default k=2) | Marginal; performance flat k=0–32 |
| Pre-existing profile | Dataset-provided (PR, EC) | Used when available |

**Implication:** P2P compresses **behavioral preference text** into weights. unslop's numeric contraction rate / sentence-length σ is a **different modality** — would need either (a) NL rendering of `StyleProfile` as hypernetwork input, or (b) a stylometric embedding head parallel to `Enc(p_u)`.

### Position-aware generation

Unlike flat task-level T2L, P2P concatenates **module** and **depth** embeddings so the hypernetwork emits distinct `(A, B)` per transformer site. LoRA rank `r=8` throughout baselines.

---

## Benchmark results (paper numbers)

### LaMP + LongLaMP — random split (Table 1 averages)

| Method | Class. Acc ↑ | Class. F1 ↑ | Gen. R-L ↑ | Infer. ms ↓ |
|--------|-------------|-------------|------------|-------------|
| Base model | 0.505 | 0.496 | 0.207 | 31.97 |
| RAG | 0.507 | 0.472 | 0.216 | 44.58 |
| PAG | 0.565 | 0.564 | 0.214 | 66.85 |
| Full History | 0.575 | 0.566 | 0.224 | **461.83** |
| MT-LoRA | 0.522 | 0.509 | 0.214 | 30.51 |
| OPPU | 0.568 | 0.557 | 0.221 | 35.82 |
| **P2P** | **0.580** | **0.566** | **0.244** | 39.98 |

**Standout generation task:** LaMP-7 Tweet Paraphrase — P2P R-1 **0.442** vs Full History **0.407** (closest LaMP task to "rewrite in my voice").

### OOD split (Table 2 averages)

P2P leads classification (**Acc 0.581**, **F1 0.563**) and generation (**R-L 0.243**). Notably beats OPPU on several tasks despite OPPU training on target-user history — suggests hypernetwork **distills population-level mapping** that generalizes better than per-user overfit in sparse regimes.

### Open-ended — LLM-as-Judge (Table 3, GPT-4o Prometheus 1–5)

| Method | Personal Reddit (random) | Personal Reddit (OOD) | Empathetic Conv. (random) |
|--------|--------------------------|----------------------|---------------------------|
| Base | 1.71 | 1.58 | 1.86 |
| PAG | 1.77 | 1.60 | 1.80 |
| MT-LoRA | 1.98 | 1.96 | 1.62 |
| **P2P** | **2.21** | **2.15** | **2.03** |

Absolute scores remain low (scale tops at 5) — personalization quality is hard; P2P wins relatively, not absolutely.

### Deployment economics (Figure 4)

- OPPU LoRA: **20.44 s/user** (linear cumulative cost)
- P2P: **0.57 s/user** (near-flat)
- One-time hypernetwork training: **27,167 s** (~7.5 h); break-even ~**1,450 users**

### Robustness findings

- **User diversity > count:** 50 clusters beats 10; doubling user count from 20%→100% ≈ flat curves.
- **Sparse history:** Competitive with OPPU across history-length buckets (Figure 5).
- **Embedding backbone:** Qwen3-Emb-4B best; Qwen3-Emb-8B **underperforms** smaller model.
- **3B base model:** Same relative P2P > OPPU trend holds (Appendix B).

---

## StyleTunedLM — the authorship-PEFT baseline P2P does not run

Liu et al. (*Customizing LLM Generation Style via PEFT*, INLG 2024) is the paper Wang et al. cite when excluding fine-tuning from Catch Me If You Can. Directly relevant to **voice matching**:

| Method | BERT authorship classifier ↑ | Lexical MSE ↓ | Syntactic JSD ↓ |
|--------|------------------------------|---------------|-----------------|
| 5-shot prompt | 0.693 | 3.80 | 0.07 |
| 10-shot prompt | 0.680 | 3.31 | 0.06 |
| instruct prompt | 0.263 | 2.67 | 0.15 |
| **StyleTunedLM (LoRA)** | **0.879** | **1.39** | **0.06** |

- **10 Project Gutenberg authors**, Llama-2-7B, ~80k tokens/author, rank-r LoRA, 3 epochs.
- **Content memorization risk:** learns surface style but may memorize named entities; masking variant mitigates.
- **Data floor:** stable attribution needs ~5k–10k words (Eder 2015); 5% of 80k tokens still works partially.
- **Merged LoRA:** style adapter + instruction adapter can coexist.

**Gap:** StyleTunedLM is **one LoRA per author** (OPPU-shaped), not hypernetwork-generated. P2P solves deployment; StyleTunedLM proves **PEFT beats prompting on authorship metrics**.

---

## Comparison matrix — voice-match technology stack

| Approach | Input signal | Weight change | Authorship eval | Deploy cost | unslop today |
|----------|-------------|---------------|-----------------|-------------|--------------|
| **Prompt + few-shot** | Samples in context | None | Catch Me: Blog AV ~17–21% | 1 API call | Partial (voice-match prompt) |
| **Numeric stylometry prompt** | `StyleProfile` deltas | None | Untested vs Wang harness | 1 API call | `stylometry.py` + `style_memory.py` |
| **StyleTunedLM** | Author corpus | Per-author LoRA | **87.9%** BERT classifier | Train once/author | ❌ |
| **TinyStyler** | Few-shot + authorship emb | 800M specialist model | Beats GPT-4 authorship transfer | HF inference | ❌ (cited in SKILL.md) |
| **OPPU** | User history | Per-user LoRA train | LaMP tasks only | ~20 s/user | ❌ |
| **P2P** | NL profile embedding | Hypernet → LoRA | LaMP + LLM judge; **no AA/AV** | **0.57 s/user** | ❌ |
| **ZeroStylus** | Reference docs | None (zero-shot rewrite) | Tri-axial GPT judge +0.20 | Multi-pass LLM | ❌ (Phase 9 blueprint) |

---

## Supporters vs skeptics

### Supporters say

1. **Scalability:** 33× deployment speedup removes OPPU as a production blocker (Pivot News, project page).
2. **Generalization:** Beating OPPU on averages while OPPU sees test-user gradients is surprising — hypernetwork learns transferable profile→weight map.
3. **Privacy narrative:** Local hypernetwork + on-device profile encoding avoids shipping full history every call (vs Full History 462 ms inference).
4. **Lineage credibility:** Same authors as OPPU + LaMP; code on GitHub; checkpoint on HuggingFace; fork of Sakana T2L.

### Skeptics / gaps say

1. **Not authorship-verified:** No AA/AV/style-model/GPTZero battery (Catch Me If You Can). Tweet paraphrase ROUGE ≠ "sounds like me on informal blogs."
2. **LLM-as-judge dependency:** Open-ended wins use GPT-4o Prometheus — same class of evaluator Wang rejected for style imitation (self-preference risk).
3. **Training gate:** Hypernetwork needs diverse multi-user corpus + 80G GPU training — not something a resume writer runs locally today.
4. **Profile = preference, not idiolect:** LaMP tasks optimize **behavioral prediction** (tags, ratings, headlines) more than **implicit prose mannerisms** Catch Me measures.
5. **Adapter reverse-engineering:** Paper's own ethics section — LoRA weights may leak profile information if extracted.
6. **Detector axis unknown:** StyleTunedLM + Jemama show high style fidelity can sit at **low perplexity** (detectable). P2P never tests GPTZero.
7. **Single-task-per-user limitation** (paper §Limitations): real users span genres; hypernetwork trained per LaMP task slice.

---

## Relationship to unslop voice-match

### What unslop does now (Phase 1–2)

```
--voice-sample / style-memory.json
        │
        ▼
  stylometry.analyze() → StyleProfile (19 numeric fields)
        │
        ▼
  humanize.py _format_voice_targets() → LLM prompt band targets
        │
        ▼
  Single-pass rewrite (prompt-bound)
```

This is **explicitly prompt-bound** — the architecture Catch Me If You Can shows fails on informal personal writing (Blog AV ~17–21% vs human 91.4%).

### What Profile-to-PEFT would add (Phase 3+ spec)

```
User writing samples
        │
        ├─► stylometry.analyze() → numeric profile (keep)
        └─► NL profile renderer OR excerpt embedder
                    │
                    ▼
         Hypernetwork Gen_θ (local or service)
                    │
                    ▼
         LoRA adapter ΔW_u (ephemeral or cached)
                    │
                    ▼
         Base model rewrite with plugged adapter
```

**Design choices for a future unslop implementation:**

| Decision | Recommendation | Rationale |
|----------|----------------|-----------|
| Input modality | **Hybrid:** NL summary from samples + numeric `StyleProfile` side-channel | P2P ablation: summary dominates; numerics cover cues NL summary misses (contraction rate, σ) |
| Base model | Match user's host (Qwen/Llama) or small specialist (TinyStyler path) | P2P tied to Qwen2.5-7B; plugin can't assume one base |
| Train vs infer | **Infer-only in plugin; train offline** | 80G A100 training is not installer scope |
| Storage | Ephemeral LoRA in memory; optional encrypted cache | OWASP agentic memory rules; LoRA ≈ compressed profile |
| Evaluation | Adapt Catch Me AV harness on before/after pairs | Only external oracle unslop lacks today |

### Voice-match ≠ anti-detector (keep separate)

Per Agent #52: PEFT voice fidelity does not imply detector evasion. StyleTunedLM lowers perplexity on author text (good for style, bad for Binoculars/GPTZero). Any future P2P integration belongs in **voice-match**, not anti-detector — unless user explicitly opts into sequenced workflow (voice first, then detector defense with σ floors).

### SKILL.md citation fix (cross-ref Agent #43)

Current Known Limitation should cite:

- **Catch Me If You Can** — prompt ceiling
- **StyleTunedLM / Liu 2024** — PEFT authorship gains
- **P2P / Tan 2026** — scalable profile→LoRA deployment path
- **TinyStyler** — small-model authorship embedding alternative

Do **not** say "fine-tuning wins decisively" without naming which paper and metric.

---

## unslop integration plan

### Phase 1 — Documentation (now)

1. Add P2P + StyleTunedLM to `docs/research/10-style-transfer-voice/SYNTHESIS.md` as **Phase 3 parametric voice** row.
2. Extend `SKILL.md` Known Limitation with P2P one-liner: "prompt voice-match is Phase 1; Profile-to-PEFT shows profile→LoRA hypernetworks beat per-user training at scale (Tan ACL 2026)."
3. Cross-link Agent #43, #47, #48, #52 in research index.

### Phase 2 — Evaluation harness (medium)

1. **Adapter script:** Run `deploy_AV_models.py` from Catch Me repo on unslop voice-match before/after pairs (Blog/Reddit subsets).
2. **Telemetry:** Log `StyleProfile.delta()` alongside AV score — test whether numeric prompt conditioning moves AV at all.
3. **Optional:** HF `Zhaoxuan/P2P_ckpt` inference on Personal Reddit subset — compare LLM-judge scores to unslop output (research only, Qwen7B dependency).

### Phase 3 — Prototype parametric voice (long)

1. **Minimal path:** OPPU-style single-user LoRA via StyleTunedLM recipe on user's samples (qlora, local) — no hypernetwork. Validates PEFT lift for one user before scaling.
2. **Scaled path:** Train stylometric hypernetwork on multi-author corpus (Enron + Blog + Reddit from Catch Me data) mapping NL+numeric profile → LoRA.
3. **Merge guard:** Instruction-following LoRA + style LoRA merge (StyleTunedLM §merged modules).

### Phase 4 — Product boundary

- Ship **infer-only** hypernetwork weights for one base model OR document "bring your own LoRA" from external fine-tune.
- Never auto-train on user data without explicit consent.
- Anti-detector remains separate mode; no implied Turnitin evasion from voice LoRA.

---

## Key numbers cheat sheet

| Metric | Value | Source |
|--------|-------|--------|
| P2P deployment time | 0.57 s/user | Tan ACL 2026 |
| OPPU deployment time | 20.44 s/user | Tan ACL 2026 |
| Speedup | 33× | Tan ACL 2026 |
| P2P avg class. Acc (random) | 0.580 | Table 1 |
| OPPU avg class. Acc (random) | 0.568 | Table 1 |
| Tweet paraphrase R-1 | P2P 0.442, best prompt 0.407 | Table 1 |
| PR LLM judge (random) | P2P 2.21, base 1.71 | Table 3 |
| Hypernet training time | 27,167 s | §6 |
| Break-even users vs OPPU | ~1,450 | §6 |
| StyleTunedLM authorship classifier | **87.9%** | Liu INLG 2024 Table 2 |
| 5-shot authorship classifier | 69.3% | Liu INLG 2024 Table 2 |
| Catch Me Blog AV (5-shot LLM) | ~17–21% | Wang EMNLP 2025 |
| Catch Me human Blog AV | 91.4% | Wang EMNLP 2025 |

---

## Bottom line

Profile-to-PEFT is the **production engineering** answer for "how do we personalize LLMs without training a LoRA per user?" It inherits OPPU's insight that **preferences live better in weights than prompts**, and inherits Text-to-LoRA's hypernetwork machinery — but swaps task descriptions for **user profiles**.

For unslop, it defines the **upgrade path** when prompt + `StyleProfile` hits Catch Me's informal-writing ceiling: compress the user's writing into a profile, generate LoRA weights, plug and rewrite. StyleTunedLM proves the voice objective is achievable with PEFT; P2P proves the deployment pattern is scalable; TinyStyler proves small specialists can beat frontier prompting. None of them ship inside unslop today — and none were tested against GPTZero on personal blogs. Phase 3 should close that eval gap before any product claim.

---

## References (BibTeX keys)

```bibtex
@inproceedings{tan2026p2p,
  title={Instant Personalized Large Language Model Adaptation via Hypernetwork},
  author={Tan, Zhaoxuan and Zhang, Zixuan and Wen, Haoyang and others},
  booktitle={ACL 2026},
  url={https://aclanthology.org/2026.acl-long.1081/}
}
@inproceedings{tan2024oppu,
  title={Democratizing Large Language Models via Personalized Parameter-Efficient Fine-tuning},
  author={Tan, Zhaoxuan and Liu, Zheyuan and Jiang, Meng and others},
  booktitle={EMNLP 2024},
  url={https://aclanthology.org/2024.emnlp-main.372/}
}
@inproceedings{liu2024styletunedlm,
  title={Customizing Large Language Model Generation Style using Parameter-Efficient Finetuning},
  author={Liu, Jiahong and others},
  booktitle={INLG 2024},
  url={https://aclanthology.org/2024.inlg-main.34/}
}
@inproceedings{charakorn2025t2l,
  title={Text-to-LoRA: Instant Transformer Adaption},
  author={Charakorn, Rujikorn and others},
  booktitle={ICML 2025},
  url={https://arxiv.org/abs/2506.06105}
}
@inproceedings{horvitz2024tinystyler,
  title={TinyStyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings},
  author={Horvitz, Zachary and others},
  booktitle={Findings of EMNLP 2024},
  url={https://aclanthology.org/2024.findings-emnlp.781/}
}
@inproceedings{wang2025catchme,
  title={Catch Me If You Can? Not Yet: {LLM}s Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors},
  author={Wang, Zhengxiang and others},
  booktitle={Findings of EMNLP 2025},
  url={https://arxiv.org/abs/2509.14543}
}
```
