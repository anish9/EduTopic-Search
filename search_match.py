# pip install python-Levenshtein
import re
from Levenshtein import ratio as lev_ratio  # similarity in [0, 1]


def _norm_tokens(s: str):
    """
    Normalize string -> tokens:
    - lowercase
    - split letters/digits (no23 -> no 23)
    - remove non [a-z0-9 ] chars
    - collapse spaces
    """
    s = (s or "").lower()
    s = re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])', ' ', s)
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.split() if s else []


def name_similarity(a: str, b: str) -> int:
    """
    Return similarity 0–100 between two names/addresses.
    - ignores word order
    - numeric logic:
        * if both have numbers and NONE match -> 0
        * if some numbers match -> adjust score based on match ratio
    """
    t1 = _norm_tokens(a)
    t2 = _norm_tokens(b)

    if not t1 and not t2:
        return 0

    set1, set2 = set(t1), set(t2)

    # numeric tokens
    nums1 = {t for t in t1 if t.isdigit()}
    nums2 = {t for t in t2 if t.isdigit()}
    common_nums = nums1 & nums2

    # hard mismatch: both have numbers but no common ones
    if nums1 and nums2 and not common_nums:
        return 0

    # exact same tokens (order may differ)
    if set1 and set1 == set2:
        return 100

    # base similarity (order-insensitive: sort tokens first)
    s1 = " ".join(sorted(t1))
    s2 = " ".join(sorted(t2))
    base = lev_ratio(s1, s2)  # 0..1

    # adjust based on numeric overlap
    if nums1 and nums2:
        # ratio of common numbers to max count on either side
        num_ratio = len(common_nums) / max(len(nums1), len(nums2))
        # weight in [0.5, 1.0]:
        #   0.5 when only some numbers match,
        #   1.0 when all numbers match
        weight = 0.5 + 0.5 * num_ratio
        final = base * weight
    else:
        final = base

    return int(round(final * 100))


def classify_match(score: int) -> str:
    """
    Map similarity score (0–100) into 3 buckets:
    - 'high'    : almost certainly same entity
    - 'partial' : maybe same, needs review
    - 'none'    : treat as not same
    """
    if score >= 85:
        return "high"      # highly correct
    elif score >= 60:
        return "partial"   # may be partially correct
    else:
        return "none"      # no confidence they are same
