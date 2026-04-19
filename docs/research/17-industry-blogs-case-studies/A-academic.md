# A — Academic & Institutional Case Studies on Humanized AI (Quantitative)

**Research value: high** — Multiple peer-reviewed RCTs, NBER working papers, JAMA studies, and B-school field experiments directly measure outcomes of human-like / empathetic / anthropomorphic AI in enterprise settings (customer support, sales, marketing, healthcare, education), with reproducible effect sizes.

**Scope.** This digest focuses exclusively on academic and institutional case studies (HBS, NBER, MIT Sloan, JAMA, Stanford SCALE, *Journal of Marketing*, *Information Systems Research*, peer-reviewed field experiments). Vendor press and pure marketing blogs are excluded except where they report on a credible institutional study (e.g., Klarna via OpenAI/MIT Sloan, Scotiabank via MIT Sloan ME). All effect sizes are reported as published; see *Patterns & Gaps* for caveats.

---

## Prior Art — 20 Case Studies With Measured Outcomes

### Customer Support

**1. Brynjolfsson, Li & Raymond — "Generative AI at Work"** (NBER WP 31161, 2023; *QJE* forthcoming)
Staggered deployment of a GPT-based conversational assistant to ~5,179 customer-support agents at a Fortune 500 software firm.
- +14% issues resolved / hour on average; **+34% for novice/low-skill agents**; ≈0% for top performers.
- Improved customer sentiment (measured via NLP on transcripts); customers treated AI-assisted agents more politely and escalated to managers less often.
- Higher employee retention in treated group.
- Mechanism: AI disseminated the speech patterns and empathy tactics of top performers — humanization as *pattern diffusion* rather than persona design.

**2. Luo, Qin, Fang & Qu — "Engaging Customers with AI in Online Chats"** (HBS working paper, 2024)
Randomized field experiment with a meal-delivery company; AI-assist vs. unassisted agents.
- Treated agents responded faster, used more empathy words, more information, more solution-orientation.
- Larger lift for low-tenure agents.
- **Failure mode:** Customers primed by a prior chatbot failure *penalized* the human agent's AI-accelerated replies, mistaking them for a bot → net-negative sentiment. Humanization helps only when trust is intact.

**3. Crolic, Thomaz, Hadi & Stephen — "Blame the Bot: Anthropomorphism and Anger in Customer-Chatbot Interactions"** (*Journal of Marketing* 86, 2022, pp. 132–148)
5 studies including n ≈ 35,000 real chats at a European telecom.
- Anthropomorphic cues (name, avatar, human-like language) *reduce* customer satisfaction, firm evaluation, and purchase intent **only when the customer is angry**; no effect when calm.
- Mechanism: expectancy violation — human-like bots imply human-like problem-solving; unmet expectation amplifies disappointment.
- Mitigation (Study 5): explicitly lowering expectations *before* interaction eliminated the penalty.

**4. Adam, Wessel & Benlian — "Estimating the Impact of 'Humanizing' Customer Service Chatbots"** (*Information Systems Research* 32(3), 2021, pp. 736–751)
Retail field experiment manipulating three anthropomorphic features: **humor, typing delays, social presence**.
- Humanization increased transaction conversion.
- Channel: higher willingness to disclose personal info needed to complete transactions.
- Side effect: humanization also increased offer-fairness sensitivity — customers evaluated offers more critically once they treated the bot as a social actor.

**5. Klarna × OpenAI Deployment** (2024; cited in MIT Sloan and practitioner press; methodologically a vendor case, included for scale reference)
Production deployment of an LLM assistant replacing front-line tier-1 support.
- 2.3M conversations / month = work of **~700 FTE agents**.
- Average resolution time: **11 min → <2 min (–82%)**.
- Repeat-inquiry rate dropped ~25%; CSAT on par with human agents.
- 35+ languages; ~$40M est. annual profit impact.
- *Caveat:* no independent academic RCT; reported CSAT parity not externally audited.

**6. Scotiabank Chatbot Transformation** (MIT Sloan Management Review — Middle East, case study 2024)
- Chatbot answer accuracy **35% → 90%** (late-2022 → 2024).
- >40% of customer questions resolved without human escalation.
- **60–70% reduction in agent ramp time** on customer-context via AI summaries — consistent with Brynjolfsson et al.'s novice-bias finding.

### Sales & Marketing

**7. Sahni, Wheeler & Chintagunta — "Personalization in Email Marketing: The Role of Non-Informative Advertising Content"** (Stanford GSB working paper; *Marketing Science*, 2018)
Multi-firm randomized field experiments.
- Adding recipient first name to subject line: open rate 9.05% → 10.80% (**+20%**), sales leads 0.39% → 0.51% (**+31%**), unsubscribes **–17%**.
- Foundational benchmark for how shallow humanization (name insertion) moves commercial metrics without content change.

**8. Stanford SETR ("Sales-Email-Turbo-Ramp") Study** (2024, 214 SDRs/AEs across 5 SaaS firms, 90-day field trial)
- **Ramp time 89 → 58 days (–35%)** for cohort using AI-drafted outreach.
- +42% first-touch emails/hour.
- **Reply-, meeting-held-, and SQL-rates: no statistically significant difference** vs. control.
- 67% of AI users report reduced "blank-page anxiety."
- Implication: humanized AI copy shifts rep throughput and ramp, not buyer response — a scale-side rather than demand-side gain.

**9. Dell'Acqua, McFowland, Mollick et al. — "Navigating the Jagged Technological Frontier"** (HBS Working Paper 24-013, 2023)
Preregistered RCT, **758 BCG consultants**, 18 realistic consulting tasks.
- Inside frontier: +12.2% tasks completed, 25.1% faster, **40% higher quality output**.
- Outside frontier: **–19% correct-solution rate** — humanized fluency of GPT-4 caused consultants to trust confident-sounding wrong answers.
- Relevance: strong warning that fluency (a key humanization attribute) is a *risk factor* when capability is absent.

**10. BCG × D^3 — Data Science Skill Experiment** (Harvard D^3, 2024)
480 BCG consultants on data-science tasks.
- GenAI-augmented non-experts reached **86% of the benchmark performance of data scientists**; up to **49-percentage-point** improvement on out-of-skill coding tasks.
- Less effective on predictive analytics where the tool itself is weaker — again the jagged-frontier shape.

### Healthcare

**11. Ayers et al. — "Comparing Physician and Artificial Intelligence Chatbot Responses to Patient Questions Posted to a Public Social Media Forum"** (*JAMA Internal Medicine*, 2023)
Blinded panel of licensed clinicians evaluated paired physician/ChatGPT answers to 195 r/AskDocs questions.
- **ChatGPT preferred in 78.6%** of comparisons.
- Rated ~3.6× more likely to be "good/very good" quality.
- Rated **9.8× more likely to be "empathetic/very empathetic."**
- Canonical citation for humanized AI exceeding clinicians on perceived empathy.

**12. Chen et al. / Stanford Health Care — "AI-Generated Draft Replies Integrated Into Health Records and Physicians' Electronic Communication"** (*JAMA Network Open*, 2024)
162 clinicians, Epic MyChart integration.
- 20% mean utilization of AI drafts.
- No measurable reduction in reply time.
- Significant reductions in physician task load and self-reported exhaustion (validated scales).
- Interpretation: humanized draft is a *cognitive-load* intervention, not a throughput intervention.

**13. Tai-Seale et al. / UCSD Health** (*JAMA Network Open*, 2024)
First randomized prospective eval of Epic's GenAI inbox drafts (June–Aug 2023).
- +21.8% read time, +17.9% reply length, –5.9% reply time (n.s.).
- Physicians explicitly valued AI for "longer, more compassionate responses, especially at end of long workdays."

**14. UW Health MyChart Pilot** (2023 institutional report)
>3,000 messages drafted across 75 nurses / 30 departments.
- Qualitative-dominant outcomes; adoption curves declining over months (consistent with a Dutch academic-hospital replication showing adoption ≈16.7% and falling).
- Signals a real durability-of-adoption gap.

**15. Cancer-Patient Study** (*npj Digital Medicine*, 2025)
Patients with cancer (not clinicians) rated AI chatbot answers **more empathetic** than oncologist answers to cancer questions.
- Important framing: *patient-rated* empathy, not expert-rated. Humanization benefit is strongest when the judge is the served party.

### Education

**16. Kestin, Miller, Klein et al. — "AI Tutoring Outperforms In-Class Active Learning: an RCT"** (Stanford SCALE / Harvard, 2024)
Harvard physics course, within-subject RCT.
- Students learn **>2× as much in less time** with AI tutor vs. active-learning session — tutor built with same pedagogical scaffolding.
- Higher self-reported engagement & motivation.

**17. Pardos & Bhandari — "ChatGPT-Generated Help Produces Learning Gains Equivalent to Human Tutor-Authored Help"** (Stanford SCALE repository, 2024)
Math-hint randomized comparison.
- No significant difference in learning gains or time-on-task between ChatGPT-authored hints and expert human hints.
- Both ≫ no-help control.

**18. Thomas, Yang, Gupta et al. — "Hybrid Human-AI Tutoring"** (three-study quasi-experimental, Stanford SCALE, 2024)
Low-income urban middle schools.
- Hybrid tutoring positively affects proficiency and engagement.
- Lower-achieving students benefit disproportionately — again the novice-bias pattern.
- Approx. $700 / student / year — first institutional cost-effectiveness anchor.

### Cross-Function / Knowledge Work

**19. Novo Nordisk × Microsoft Copilot** (MIT Sloan Management Review, 2024, "How to Scale GenAI in the Workplace")
20,000-employee deployment.
- 2.17 hours/week saved on average.
- **Key finding:** satisfaction correlated ~3× more strongly with *perceived quality improvement* than with time saved.
- Reframes humanization ROI as craft-uplift, not throughput.

**20. Dell'Acqua, Ayoubi, Lifshitz-Assaf et al. — "The Cybernetic Teammate"** (NBER WP 33641, 2025)
Pre-registered field experiment with 776 P&G professionals on real innovation tasks.
- GenAI lets **individuals match the output quality of traditional 2-person cross-functional teams**.
- Reduces hierarchy- and role-bound differences in output quality.
- Emotional outcomes: higher positive affect, lower frustration — a humanization *of the work experience* even when the user is expert.

---

## Patterns & Trends Across Studies

1. **Novice-bias is the most replicated quantitative finding.** Brynjolfsson et al. (+34% novices), Scotiabank (60–70% ramp cut), Dell'Acqua BCG (49 pp outside-skill lift), Thomas hybrid tutoring, SETR (35% faster ramp), Peng/GitHub (55.8% faster — stronger for juniors). Humanized AI flattens the experience curve; variance across performers compresses.

2. **Perceived empathy is measurably real and often exceeds humans.** JAMA Internal Medicine, npj Digital Medicine, and HBS meal-delivery all find AI-assisted or AI-drafted text rated *more* empathetic than human comparators by the served party. The effect holds across written domains with asymmetric emotional stakes (patient, customer).

3. **Humanization helps only when trust and capability are intact.** Crolic et al. (angry customers), Luo et al. (chatbot-failure priming), and Dell'Acqua "jagged frontier" all show the same structural failure: fluent, human-like AI raises expectations that magnify penalty when capability falls short.

4. **Throughput ≠ quality ≠ satisfaction.** Novo Nordisk and SETR both find satisfaction driven more by quality than time saved; Stanford/UCSD JAMA studies find burnout relief without reply-time change. Measuring humanization ROI only in minutes saved systematically understates value.

5. **The channel is disclosure, not eloquence.** Adam et al. (ISR 2021) and Sahni et al. (name-personalization) show that humanization raises conversion by increasing willingness to disclose / engage, not by persuasion per se. Humanization is best modeled as a trust-signaling intervention.

6. **Hybrid designs dominate pure-human and pure-AI on measured metrics.** Hybrid tutoring (SCALE), AI-edited marketing copy (+26% CTR vs. AI-only +19% vs. human baseline), AI-drafted physician replies. The consistent winner is "AI drafts, human curates."

---

## Gaps in the Academic Literature

1. **"Humanization" is rarely isolated as a variable.** Most enterprise case studies (Klarna, Novo Nordisk, Scotiabank) measure *AI deployment* as a bundle — model, UI, policy, training. Only Crolic et al. and Adam et al. actually vary anthropomorphic cues cleanly. Causal attribution of outcomes to humanization specifically is thin.

2. **Durability over time.** Most RCTs are ≤90 days; UW Health and the Dutch academic-hospital replication suggest *declining* adoption over months. No published long-horizon (>12 month) randomized data on whether humanized AI effects persist or decay.

3. **Cross-cultural humanization.** Klarna advertises 35+ language operation but no academic work measures whether humanization style transfers across cultures. Anthropomorphism norms differ (high-context vs. low-context cultures) and this is unstudied at scale.

4. **Failure-mode quantification.** Crolic et al. is the only large-scale quantification of the anthropomorphism-backfire effect. Healthcare and education case studies don't systematically measure when humanization *hurts* — only when it helps.

5. **Disclosure asymmetry.** Studies rarely manipulate whether the user knows they're interacting with AI. The meal-delivery study hints that users reading AI speed as bot-ness produces negative affect; this remains under-tested.

6. **B2B humanization specifically is thin.** Most rigorous data is B2C (retail, consumer health, customer support). SETR is a rare B2B RCT; Kellogg/Wharton MBA case-study corpus is case-teaching-oriented rather than quantitative.

7. **Voice / multimodal humanization.** All reviewed academic studies measure text. Near-zero peer-reviewed quantitative case studies on humanized *voice* AI (intonation, hesitations, turn-taking) in enterprise deployments as of 2026.

---

## Sources

- Brynjolfsson, Li & Raymond, "Generative AI at Work" — [NBER WP 31161](https://www.nber.org/system/files/working_papers/w31161/w31161.pdf)
- Luo et al., "Engaging Customers with AI in Online Chats" — [HBS Faculty & Research](https://www.hbs.edu/faculty/Pages/item.aspx?num=66860)
- Crolic, Thomaz, Hadi & Stephen, "Blame the Bot" — [*Journal of Marketing* 86 preprint (Oxford ORA)](https://ora.ox.ac.uk/objects/uuid:73d46bba-35d1-465c-be00-aa6f4f4ccb84/download_file?safe_filename=Crolic_et_al_2021_blame_the_bot.pdf&type_of_work=Journal+article)
- Adam, Wessel & Benlian, "Estimating the Impact of 'Humanizing' Customer Service Chatbots" — [*ISR* 32(3), 2021](https://ideas.repec.org/a/inm/orisre/v32y2021i3p736-751.html)
- Dell'Acqua et al., "Navigating the Jagged Technological Frontier" (BCG/HBS) — [HBS WP 24-013](https://hbs.edu/faculty/Pages/item.aspx?num=64700)
- Dell'Acqua et al., "The Cybernetic Teammate" (P&G) — [NBER WP 33641](https://www.nber.org/papers/w33641)
- BCG × Harvard D^3 data-science experiment — [BCG press release](https://www.bcg.com/press/5september2024-generative-ai-knowledge-workers-consultants) and [D^3 summary](https://d3.harvard.edu/a-new-paradigm-for-skill-development-a-large-scale-bcg-experiment/)
- Ayers et al., "Comparing Physician and AI Chatbot Responses" — [*JAMA Internal Medicine* 2023](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2804309)
- Chen et al. / Stanford Health — AI Draft Replies Integrated Into EHR — [*JAMA Network Open* 2024](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2816494)
- Tai-Seale et al. / UCSD Health — [*JAMA Network Open* 2024](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2817615)
- UW Health MyChart pilot report — [Becker's Hospital Review](https://www.beckershospitalreview.com/ehrs/uw-health-ai-pilot-generates-3-000-patient-messages.html)
- Cancer-patient empathy study — [*npj Digital Medicine* 2025](https://www.nature.com/articles/s41746-025-01671-6)
- Kestin et al., "AI Tutoring Outperforms Active Learning" — [Stanford SCALE](https://scale.stanford.edu/publications/ai-tutoring-outperforms-active-learning)
- Pardos & Bhandari, "ChatGPT-Generated Help" — [Stanford SCALE repository](https://scale.stanford.edu/ai/repository/chatgpt-generated-help-produces-learning-gains-equivalent-human-tutor-authored-help)
- Thomas et al., "Hybrid Human-AI Tutoring" — [Stanford SCALE](https://scale.stanford.edu/publications/improving-student-learning-hybrid-human-ai-tutoring-three-study-quasi-experimental)
- Sahni, Wheeler & Chintagunta, "Personalization in Email Marketing" — [Stanford GSB working paper](https://www.gsb.stanford.edu/faculty-research/working-papers/personalization-email-marketing-role-non-informative-advertising)
- Peng et al., GitHub Copilot RCT (Microsoft Research) — [arXiv 2302.06590](https://export.arxiv.org/pdf/2302.06590v1.pdf)
- "How to Scale GenAI in the Workplace" (Novo Nordisk) — [MIT Sloan Management Review](https://sloanreview.mit.edu/article/how-to-scale-genai-in-the-workplace)
- "How Schneider Electric Scales AI" — [MIT Sloan Management Review](https://sloanreview.mit.edu/article/how-schneider-electric-scales-ai-in-both-products-and-processes)
- "How Scotiabank Built an Ethical, Engaged AI Culture" — [MIT Sloan Management Review ME](https://www.mitsloanme.com/article/how-scotiabank-built-an-ethical-engaged-ai-culture)
- Klarna deployment (scale reference only) — [OpenAI customer story](https://openai.com/customer-stories/klarna/)
