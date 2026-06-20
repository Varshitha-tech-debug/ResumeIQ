"""Pure Python set-based skill matching — no AI."""

import re

from resumeiq.constants import ROLE_KEYWORDS

# Keywords that need alias patterns (avoids false positives like java vs javascript).
KEYWORD_ALIASES: dict[str, list[str]] = {
    "r programming": [r"\br\b", r"\br programming\b", r"\brstudio\b"],
    "node": [r"\bnode\.?js\b", r"\bnode\b"],
    "rest api": [r"\brest\s+api\b", r"\brestful\s+api\b"],
    "ci/cd": [r"\bci\s*/\s*cd\b", r"\bcontinuous integration\b"],
    "a/b testing": [r"\ba\s*/\s*b testing\b", r"\bab testing\b"],
    "hugging face": [r"\bhugging\s*face\b", r"\btransformers\b"],
    "next.js": [r"\bnext\.?js\b"],
    "c++": [r"\bc\+\+\b"],
    "scikit-learn": [r"\bscikit[\-\s]?learn\b", r"\bsklearn\b"],
}


def _compile_pattern(keyword: str) -> re.Pattern[str]:
    """Build a word-boundary-safe regex for a role keyword."""
    lower = keyword.lower().strip()

    if lower in KEYWORD_ALIASES:
        combined = "|".join(f"(?:{alias})" for alias in KEYWORD_ALIASES[lower])
        return re.compile(combined, re.IGNORECASE)

    if " " in lower or "/" in lower or "." in lower or "+" in lower:
        escaped = re.escape(lower)
        escaped = escaped.replace(r"\ ", r"\s+")
        return re.compile(escaped, re.IGNORECASE)

    return re.compile(rf"\b{re.escape(lower)}\b", re.IGNORECASE)


_PATTERN_CACHE: dict[str, re.Pattern[str]] = {}


def get_pattern(keyword: str) -> re.Pattern[str]:
    if keyword not in _PATTERN_CACHE:
        _PATTERN_CACHE[keyword] = _compile_pattern(keyword)
    return _PATTERN_CACHE[keyword]


def keyword_in_text(keyword: str, text: str) -> bool:
    """Return True only when keyword appears as a distinct token/phrase."""
    return bool(get_pattern(keyword).search(text))


def count_keyword_mentions(keyword: str, text: str) -> int:
    """Count distinct occurrences using the same boundary rules as matching."""
    return len(get_pattern(keyword).findall(text))


def match_skills(keywords: list[str], text: str) -> tuple[list[str], list[str]]:
    """
    Set-based skill matching: matched = keywords ∩ present, missing = keywords − present.
    Preserves the original keyword list order.
    """
    keyword_set = set(keywords)
    present = {kw for kw in keyword_set if keyword_in_text(kw, text)}
    matched = [kw for kw in keywords if kw in present]
    missing = [kw for kw in keywords if kw not in present]
    return matched, missing


def score_signal_hits(signals: list[str], text_lower: str) -> int:
    """Count how many signal words appear in text (set intersection size)."""
    signal_set = set(signals)
    return len({s for s in signal_set if s in text_lower})


def pct(matched: int, total: int) -> int:
    return min(int((matched / total) * 100), 100) if total else 0


def validate_role(role: str) -> str:
    """Return normalized role or raise ValueError."""
    normalized = role.strip()
    if normalized not in ROLE_KEYWORDS:
        supported = ", ".join(sorted(ROLE_KEYWORDS.keys()))
        raise ValueError(f"Unsupported role '{role}'. Supported roles: {supported}")
    return normalized
