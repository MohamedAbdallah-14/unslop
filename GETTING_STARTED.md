# Getting started with humanizer

## What is this, in one paragraph

When you ask ChatGPT or Claude to write something for you, the reply tends to have a specific smell. It opens with a compliment. It stacks three-item lists. It uses words like "delve" and "navigate" and "holistic". Readers notice, and so do AI-detection tools. `humanizer` is a small add-on you turn on inside your AI assistant, and it tells the assistant to drop those habits and write like a person who's tired at the end of a workday. You use it when the writing itself is what you're being judged on: cover letters, college essays, bios, LinkedIn posts, anything a human is about to read and react to.

## Who this is for

- A college student polishing the first paragraph of an application essay.
- A job seeker rewriting a cover letter that sounds like every other cover letter.
- A marketing manager drafting a LinkedIn "About" section that doesn't read like a press release.
- A history teacher writing a parent newsletter that shouldn't sound like a chatbot.
- A freelancer answering cold-outreach emails without the "I'd be happy to assist!" opener.
- A non-native English speaker whose real writing keeps getting flagged by AI detectors at school.

## The easiest way to try it (60 seconds)

Pick Claude Code. It's the smoothest on-ramp, and you don't need to touch any settings.

Open a terminal and run these three commands:

```bash
git clone https://github.com/MohamedAbdallah-Hu/humanizer.git
cd humanizer
bash hooks/install.sh
```

On Windows, use PowerShell instead:

```powershell
pwsh hooks/install.ps1
```

Now open any Claude Code chat. Type:

```
/humanizer
```

That's it. You'll see a small badge at the bottom of the screen that reads `[humanizer:BALANCED]`. From this point on, everything Claude writes back to you in this session comes out in a human voice. Paste in a cover letter, ask for edits, and watch the reply. If you ever want the old Claude back, type `stop humanizer` and the badge goes away.

If you use Cursor or Windsurf instead, the plugin loads automatically when you open the project folder. No install step. Just type `/humanizer` in the chat panel.

## What it actually does to your writing

Here's a real-world example: a cover letter opener.

**Before (standard AI output):**

> I am writing to express my profound enthusiasm for the Marketing Coordinator position at Acme Corp. With over five years of experience navigating the dynamic landscape of digital marketing, I am confident that my comprehensive skill set and passion for innovation make me a robust candidate. I am particularly drawn to Acme's cutting-edge approach, and I would welcome the opportunity to delve into how my background aligns with your team's goals.

**After (humanizer on, balanced mode):**

> Five years in digital marketing, most of it in small teams where nobody else writes the landing pages, so I end up doing it. I saw your Marketing Coordinator posting yesterday. The part about running campaigns end-to-end instead of handing them off to an agency is what pulled me in — that's the work I actually like.

What changed, in plain terms:

- The opener stopped thanking the company and stopped announcing itself ("I am writing to express..."). It just starts.
- The three-item brag stack ("comprehensive skill set and passion for innovation") is gone. One specific detail replaced it.
- No "delve", no "landscape", no "cutting-edge". The voice now sounds like a person, not a brochure.

Same facts. Different voice. A hiring manager reads the second version without wincing.

## When to use which mode

| Mode | When to use it | Real-world example |
|------|----------------|--------------------|
| `subtle` | You like your draft. You just want the AI fingerprints cleaned off. Keep the length and shape. | You wrote a LinkedIn post yourself, ran it through Claude for typo check, and don't want the voice smoothed away. |
| `balanced` | The default. Use this when you don't know which to pick. Cuts the slop, varies the rhythm, sounds like you had a decent night's sleep. | Cover letter, bio, product description, thank-you note. |
| `full` | You want the AI to actually rewrite, not just trim. Opinions allowed. Paragraphs restructured. | A blog post opener that needs a real point of view, or a personal statement that's been sanded into nothing. |
| `voice-match` | You paste in a sample of your own writing (or a writer you admire) and ask the AI to match that cadence. | You have five old emails that sound like you. You want the sixth one to sound the same. |
| `anti-detector` | The reader is going to run the text through GPTZero, Turnitin, or a similar tool. Slower. Rougher output on purpose. | An ESL student whose honest essays keep getting falsely flagged. A resume going through an ATS known to use detectors. |

## When NOT to use it

Turn humanizer off (or don't turn it on) for any of these:

- **Medical or health advice.** Precision matters more than voice. You want the boring, exact version.
- **Legal documents, contracts, compliance text.** A "more human" lease agreement is a worse lease agreement.
- **Code.** The plugin already leaves code blocks alone, but don't ask it to "humanize a function". That's not what it does.
- **Runbooks, step-by-step operational instructions, deployment guides.** If somebody has to do something in order, you want flat and literal.
- **Security warnings and irreversible actions.** "You are about to delete this account" shouldn't be charming.
- **Anything where a wrong number, wrong date, or wrong name causes a real problem.** The rewrite can smooth over a fact you misremembered and make the wrong version sound confident. Verify the numbers yourself afterward.

A good rule: if a reader needs to *follow* the text exactly, keep it robotic. If a reader needs to *like* the text, humanize it.

## Three questions people always ask

**Does it make the AI stop being useful?**

No. It changes how the reply sounds, not what the reply says. If you ask for a cover letter draft, you still get a cover letter draft. If you ask for feedback on your essay, you still get feedback. The facts, the advice, the answer — all still there. Just without the "Certainly! What a fantastic question!" around them.

**Will it hide my text from AI detectors?**

Mostly, but not always, and nobody honest will tell you otherwise. The research the project is built on is clear: AI detectors are noisy. They falsely flag real human writing too, especially from non-native English speakers (one study found over half of TOEFL essays flagged as AI-generated). `anti-detector` mode does the things that are known to work — varying sentence length, adding specific details, roughening predictable structure — and that drops most detector scores. But a single pass through any tool is never a guarantee. For the strongest result, run the output through a second AI from a different company (Claude → ChatGPT, or ChatGPT → Gemini) and then read it yourself before sending.

**Do I need to know what a regex is, or how to code?**

No. If you can type `/humanizer` into a chat, you have everything you need. The installation is three copy-pasted commands, once, and then you're done forever.

## If you get stuck

Type `/humanizer-help` inside any AI chat where the plugin is installed. It shows every mode and every command on one screen.

To turn it off, type `stop humanizer` or `normal mode`. The badge disappears and the AI goes back to its default voice. Turn it back on any time with `/humanizer`.

If something's broken, or you're a developer who wants the technical details (hooks, file rewriter, deterministic mode, test suite), the full [README](./README.md) covers all of it.
