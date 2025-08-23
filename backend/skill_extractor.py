import re
from collections import defaultdict
from rapidfuzz import fuzz, process
from typing import Dict, List, Tuple
from skill_lexicon import SKILLS, ALIASES

# Build canonical list
CANONICAL = sorted({s for cat in SKILLS.values() for s in cat})
CANONICAL_LOWER = [s.lower() for s in CANONICAL]

# Normalize resume text (keep + and # for C++/C#)
def normalize_text(t: str) -> str:
    t = t.replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    return t

def exact_and_alias_match(text: str) -> Dict[str, float]:
    """
    Returns dict {canonical_skill: confidence(0-1)}
    """
    t = text.lower()
    found = defaultdict(float)

    # Exact phrase match for canonical skills
    for skill, skill_l in zip(CANONICAL, CANONICAL_LOWER):
        # handle symbols in skills (C++, C#) by plain substring check (case-insensitive)
        if skill_l in t:
            found[skill] = max(found[skill], 1.0)

    # Alias hits
    for alias, canonical in ALIASES.items():
        if alias.lower() in t and canonical in CANONICAL:
            found[canonical] = max(found[canonical], 0.9)

    return dict(found)

def fuzzy_topups(text: str, current: Dict[str, float], threshold: int = 90) -> Dict[str, float]:
    """
    Optional fuzzy matching (helps catch minor typos like 'Javscript').
    """
    t = text.lower()
    # Create candidate chunks (words + common 2-grams)
    tokens = re.findall(r"[a-zA-Z+#.]+", t)
    grams = set(tokens)
    for i in range(len(tokens) - 1):
        grams.add(tokens[i] + " " + tokens[i+1])

    for g in grams:
        match, score, _ = process.extractOne(g, CANONICAL_LOWER, scorer=fuzz.partial_ratio)
        if score >= threshold:
            canonical = CANONICAL[CANONICAL_LOWER.index(match)]
            # only boost if not already a strong (>=0.9) match
            if current.get(canonical, 0) < 0.9:
                current[canonical] = max(current.get(canonical, 0), 0.7)

    return current

def extract_skills(text: str, use_fuzzy: bool = True) -> List[Tuple[str, float]]:
    """
    Returns a sorted list of (skill, confidence)
    """
    norm = normalize_text(text)
    hits = exact_and_alias_match(norm)
    if use_fuzzy:
        hits = fuzzy_topups(norm, hits)

    # sort by confidence desc, then alphabetically
    return sorted(hits.items(), key=lambda x: (-x[1], x[0]))