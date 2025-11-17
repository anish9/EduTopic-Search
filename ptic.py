from abydos.phonetic import BeiderMorse          # Phonetic encoder (Beider-Morse)
from abydos.distance import Levenshtein          # Levenshtein distance with .sim() in [0,1]


def compute_name_similarity(name1, name2, match_mode='approx'):
    bm = BeiderMorse(match_mode=match_mode)      # Create a Beider-Morse encoder with chosen mode
    lev = Levenshtein()                          # Create a Levenshtein similarity object

    tokens1 = name1.split()                      # Assume name1 is already preprocessed; split into tokens
    tokens2 = name2.split()                      # Same for name2; split into tokens

    max_len = max(len(tokens1), len(tokens2))    # Max token count; used as denominator later
    if max_len == 0:                             # If both names are empty
        return 0.0                               # Return 0 similarity for empty input

    total_similarity = 0.0                       # Accumulator for per-position token similarities

    for i in range(max_len):                     # Iterate over each token position up to the longest name
        if i < len(tokens1) and i < len(tokens2):    # Only compare if both names have a token at this index
            t1, t2 = tokens1[i], tokens2[i]      # Current token pair at position i

            enc1 = set(bm.encode(t1).split())    # Phonetic encodings for token1 as a set of codes
            enc2 = set(bm.encode(t2).split())    # Phonetic encodings for token2 as a set of codes

            if enc1 and enc2:                    # Only compute overlap if both sets are non-empty
                inter = enc1 & enc2              # Intersection of phonetic code sets
                union = enc1 | enc2              # Union of phonetic code sets
                overlap_score = len(inter) / len(union)  # Jaccard-like overlap of phonetic sets
            else:
                overlap_score = 0.0              # If one side has no encodings, no overlap

            max_sim = 0.0                        # Best Levenshtein similarity between any encoding pair
            for e1 in enc1:                      # Loop over all encodings from token1
                for e2 in enc2:                  # Loop over all encodings from token2
                    max_sim = max(max_sim, lev.sim(e1, e2))  # Keep the highest similarity seen

            token_sim = max(overlap_score * 1.2, max_sim)    # Prefer exact/strong phonetic overlap (boosted)
            token_sim = min(token_sim, 1.0)      # Cap token similarity at 1.0
            total_similarity += token_sim        # Add this token’s contribution to the total
        # If only one side has a token at this index, we add nothing (implicit 0 similarity for that slot)

    avg_similarity = total_similarity / max_len  # Average over max_len positions (extra tokens count as 0)
    return avg_similarity                        # Final 0–1 similarity score for the two full names




from abydos.phonetic import BeiderMorse


def compute_name_similarity(name1: str, name2: str, match_mode: str = "approx") -> float:
    """Simple BM-based name similarity using only encoding overlaps."""
    bm = BeiderMorse(match_mode=match_mode)      # Beider–Morse encoder

    tokens1 = name1.split()                      # assume already lowercased + sorted upstream
    tokens2 = name2.split()
    len1, len2 = len(tokens1), len(tokens2)

    if len1 == 0 and len2 == 0:                  # no names at all
        return 0.0

    max_tokens = max(len1, len2)                 # how many token positions the longer name has
    min_tokens = min(len1, len2)                 # how many positions we can actually compare

    total = 0.0                                  # sum of per-token similarities

    for i in range(min_tokens):                  # compare only slots both names have
        t1, t2 = tokens1[i], tokens2[i]

        enc1 = bm.encode(t1).split()             # list of BM encodings for token1
        enc2 = bm.encode(t2).split()             # list of BM encodings for token2

        if not enc1 and not enc2:                # no encodings on both sides
            token_sim = 0.0
        else:
            set1, set2 = set(enc1), set(enc2)    # treat as sets (duplicates removed)
            matches = len(set1 & set2)           # how many encodings are exactly shared
            max_len = max(len(set1), len(set2))  # size of the "bigger" encoding list
            token_sim = matches / max_len if max_len > 0 else 0.0

        total += token_sim                       # accumulate token similarity

    # Extra tokens on the longer name are implicitly 0 similarity
    return total / max_tokens                    # average over all token slots of the longer name

