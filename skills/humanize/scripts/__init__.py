"""Tools to humanize natural-language Markdown — strip AI-isms, engineer burstiness,
preserve every code block, URL, and heading exactly. Two modes: deterministic (regex)
and LLM (Anthropic SDK or `claude --print` fallback)."""

__all__ = ["cli", "humanize", "detect", "validate"]
__version__ = "0.1.0"
