"""Evidence extraction — strict, resume-text only, zero hallucination."""

import re

from resumeiq.constants import MIN_EVIDENCE_LENGTH, WEAK_CONTEXT_WORDS
from resumeiq.matcher import count_keyword_mentions, get_pattern, keyword_in_text


def _sentence_chunks(text: str) -> list[str]:
    """Split resume text into sentence-like chunks."""
    return [chunk.strip() for chunk in re.split(r"[\n.!?;]", text) if chunk.strip()]


def find_evidence(text: str, keyword: str) -> str | None:
    """
    Extract the most descriptive sentence containing the keyword.
    Returns None if no quotable evidence exists — skill must not be counted.
    """
    if not keyword_in_text(keyword, text):
        return None

    pattern = get_pattern(keyword)
    candidates: list[str] = []

    for chunk in _sentence_chunks(text):
        if len(chunk) < MIN_EVIDENCE_LENGTH:
            continue
        if pattern.search(chunk):
            candidates.append(chunk)

    if not candidates:
        return None

    best = max(candidates, key=len)
    best = best[0].upper() + best[1:] if best else best
    return (best[:130] + "…") if len(best) > 130 else best


def get_skill_strength(text: str, keyword: str) -> str:
    """
    Classify skill strength as 'strong', 'moderate', or 'weak'.
    Based on mention count and weak-context word detection in evidence sentences.
    """
    count = count_keyword_mentions(keyword, text)
    if count == 0:
        return "weak"

    pattern = get_pattern(keyword)
    text_lower = text.lower()

    for chunk in _sentence_chunks(text_lower):
        if pattern.search(chunk):
            for weak_word in WEAK_CONTEXT_WORDS:
                if weak_word in chunk:
                    return "weak"

    if count >= 3:
        return "strong"
    if count >= 2:
        return "moderate"
    return "moderate"


def build_skill_evidence(
    text: str, candidate_keywords: list[str]
) -> tuple[list[dict], list[str]]:
    """
    Build evidence for candidate keywords.
    Only keywords with quotable evidence are returned as verified matches.
    """
    evidence: list[dict] = []
    verified: list[str] = []

    for keyword in candidate_keywords:
        quote = find_evidence(text, keyword)
        if quote is None:
            continue
        strength = get_skill_strength(text, keyword)
        verified.append(keyword)
        evidence.append({
            "skill": keyword,
            "evidence": quote,
            "strength": strength,
        })

    return evidence, verified
