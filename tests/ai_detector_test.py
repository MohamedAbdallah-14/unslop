"""Run state-of-the-art AI detection models on original vs humanized text.

Models:
  1. TMR AI Text Detector (Oxidane/tmr-ai-text-detector)
     - 99.28% AUROC on RAID benchmark (672K test samples)
     - Trained on GPT-4, ChatGPT, Llama 2, Mistral, Cohere, MPT output
     - RoBERTa-base, 125M params, MIT license

  2. Desklib AI Text Detector v1.01 (desklib/ai-text-detector-v1.01)
     - RAID leaderboard top entry, DeBERTa-v3-large, 304M params
"""

import sys
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel, AutoConfig
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file as load_safetensors

ORIGINAL = (
    "Great question! I'd be happy to help you understand machine learning. "
    "When delving into this topic, it's important to note that there are "
    "several factors to consider. Certainly, the landscape of machine "
    "learning is vast and ever-evolving.\n\n"
    "Firstly, it's worth mentioning that machine learning is a pivotal "
    "technology in today's digital landscape. Furthermore, it leverages "
    "data to create robust and seamless solutions. Additionally, the realm "
    "of artificial intelligence is expanding at a cutting-edge pace.\n\n"
    "At its core, machine learning embodies a testament to human ingenuity. "
    "However, it's important to note that the journey of learning ML can be "
    "challenging. However, with the right resources, proper tutorials, "
    "online courses, mentorship programs, you'll navigate this landscape "
    "effectively.\n\n"
    "Generally speaking, machine learning algorithms can be categorized "
    "into three paradigms: supervised learning, unsupervised learning, and "
    "reinforcement learning. In essence, each paradigm offers a unique "
    "approach to problem-solving.\n\n"
    "To summarize, machine learning is a comprehensive field that requires "
    "dedication, however, the rewards are holistic and far-reaching. The "
    "seamless integration of ML into modern applications is a testament to "
    "the robust foundation laid by researchers and practitioners alike."
)

HUMANIZED = (
    "When looking at this topic, there are several factors to consider. "
    "The world of machine learning is vast and ever-evolving.\n\n"
    "Machine learning is a key technology in today's digital landscape. "
    "It uses data to create solid and smooth solutions. The world of "
    "artificial intelligence is expanding at a modern pace.\n\n"
    "Machine learning shows human ingenuity. The path of learning ML can "
    "be challenging. With the right resources, proper tutorials, online "
    "courses, mentorship programs, you'll work through this landscape "
    "effectively.\n\n"
    "Machine learning algorithms can be categorized into three paradigms: "
    "supervised learning, unsupervised learning, and reinforcement "
    "learning. Each paradigm offers a unique approach to problem-solving.\n\n"
    "Machine learning is a complete field that requires dedication. The "
    "rewards are complete and far-reaching. The smooth integration of ML "
    "into modern applications shows the robust foundation laid by "
    "researchers and practitioners alike."
)


def chunk_text(text, tokenizer, max_length=512, stride=256):
    """Split long text into overlapping chunks for 512-token models."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    if len(tokens) <= max_length - 2:
        return [text]

    chunks = []
    for start in range(0, len(tokens), stride):
        chunk_tokens = tokens[start:start + max_length - 2]
        decoded = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(decoded)
        if start + max_length - 2 >= len(tokens):
            break
    return chunks


def run_tmr(text, tokenizer, model):
    """TMR detector: returns P(AI-generated). Label index 1 = AI."""
    chunks = chunk_text(text, tokenizer)
    scores = []
    for chunk in chunks:
        inputs = tokenizer(
            chunk, return_tensors="pt", truncation=True,
            max_length=512, padding=True,
        )
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = F.softmax(logits, dim=-1)
        scores.append(probs[0][1].item())
    return sum(scores) / len(scores)


class DesklibDetector(nn.Module):
    """Mean-pooling + linear classifier matching Desklib's training setup."""

    def __init__(self, encoder, hidden_size, num_labels=1):
        super().__init__()
        self.encoder = encoder
        self.classifier = nn.Linear(hidden_size, num_labels)

    def forward(self, input_ids, attention_mask=None, **kwargs):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        token_embs = outputs.last_hidden_state
        mask = attention_mask.unsqueeze(-1).float()
        pooled = (token_embs * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
        return self.classifier(pooled)


def run_desklib(text, tokenizer, model):
    """Desklib detector: sigmoid on single logit from mean-pooled encoder."""
    chunks = chunk_text(text, tokenizer)
    scores = []
    for chunk in chunks:
        inputs = tokenizer(
            chunk, return_tensors="pt", truncation=True,
            max_length=512, padding=True,
        )
        with torch.no_grad():
            logits = model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
            )
            prob = torch.sigmoid(logits)
        scores.append(prob[0][0].item())
    return sum(scores) / len(scores)


def main():
    print("=" * 70)
    print("STATE-OF-THE-ART AI DETECTION TEST")
    print("Original vs Humanized (deterministic mode)")
    print("=" * 70)
    print()

    # --- TMR ---
    print("Loading TMR AI Text Detector (Oxidane/tmr-ai-text-detector)...")
    print("  RAID: 99.28% AUROC | GPT-4, ChatGPT, Llama2, Mistral")
    print()

    tmr_tok = AutoTokenizer.from_pretrained("Oxidane/tmr-ai-text-detector")
    tmr_mod = AutoModelForSequenceClassification.from_pretrained(
        "Oxidane/tmr-ai-text-detector"
    )
    tmr_mod.eval()

    orig_tmr = run_tmr(ORIGINAL, tmr_tok, tmr_mod)
    hum_tmr = run_tmr(HUMANIZED, tmr_tok, tmr_mod)
    tmr_delta = orig_tmr - hum_tmr
    tmr_pct = (tmr_delta / orig_tmr * 100) if orig_tmr > 0 else 0

    print("  TMR Results:")
    print("    Original:   {:.1%} AI probability".format(orig_tmr))
    print("    Humanized:  {:.1%} AI probability".format(hum_tmr))
    print("    Reduction:  {:.0f}%".format(tmr_pct))
    print()

    # free memory before loading next model
    del tmr_mod, tmr_tok
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    # --- Desklib ---
    print("-" * 70)
    print()
    print("Loading Desklib AI Text Detector (desklib/ai-text-detector-v1.01)...")
    print("  RAID leaderboard top entry | DeBERTa-v3-large, 304M params")
    print()

    orig_desk = None
    hum_desk = None
    desk_pct = 0

    try:
        desk_id = "desklib/ai-text-detector-v1.01"
        desk_tok = AutoTokenizer.from_pretrained(desk_id)

        # Load the raw DeBERTa encoder (no classification head)
        config = AutoConfig.from_pretrained(desk_id)
        encoder = AutoModel.from_config(config)

        # Build custom model: mean-pool + linear(1024, 1)
        desk_mod = DesklibDetector(encoder, config.hidden_size, num_labels=1)

        # Load checkpoint and remap keys
        weights_path = hf_hub_download(desk_id, "model.safetensors")
        state = load_safetensors(weights_path)

        renamed = {}
        for k, v in state.items():
            new_k = re.sub(r"^model\.", "encoder.", k)
            renamed[new_k] = v

        info = desk_mod.load_state_dict(renamed, strict=False)
        loaded_count = len(state) - len(info.unexpected_keys)
        print("  Loaded {}/{} weight tensors".format(loaded_count, len(state)))
        if info.missing_keys:
            print("  Missing keys: {}".format(len(info.missing_keys)))
        desk_mod.eval()

        orig_desk = run_desklib(ORIGINAL, desk_tok, desk_mod)
        hum_desk = run_desklib(HUMANIZED, desk_tok, desk_mod)
        desk_delta = orig_desk - hum_desk
        desk_pct = (desk_delta / orig_desk * 100) if orig_desk > 0 else 0

        print("  Desklib Results:")
        print("    Original:   {:.1%} AI probability".format(orig_desk))
        print("    Humanized:  {:.1%} AI probability".format(hum_desk))
        print("    Reduction:  {:.0f}%".format(desk_pct))
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print("  Desklib failed: {}".format(exc))

    # --- Summary ---
    print()
    print("=" * 70)
    print("COMBINED RESULTS")
    print("=" * 70)
    print()
    row = "{:<35} {:>10} {:>10} {:>10}"
    print(row.format("Detector", "Original", "Humanized", "Reduction"))
    print("-" * 70)
    print(row.format(
        "TMR (RAID 99.28% AUROC)",
        "{:.1%}".format(orig_tmr),
        "{:.1%}".format(hum_tmr),
        "{:.0f}%".format(tmr_pct),
    ))
    if orig_desk is not None:
        print(row.format(
            "Desklib (RAID #1)",
            "{:.1%}".format(orig_desk),
            "{:.1%}".format(hum_desk),
            "{:.0f}%".format(desk_pct),
        ))
    print()
    print("Manual online testing (user-verified):")
    print(row.format("QuillBot AI Detector", "100%", "0%", "100%"))
    print(row.format("ZeroGPT", "100%", "36%", "64%"))
    print(row.format("BrandWell / Content at Scale", "100%", "FAIL", "--"))
    print()


if __name__ == "__main__":
    main()
