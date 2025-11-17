from abydos.phonetic import BeiderMorse
from abydos.distance import Levenshtein

def compute_name_similarity(name1, name2, match_mode='approx'):
    """
    Compute similarity between two full names using Beider-Morse phonetic encoding.
    
    Args:
        name1: First name string
        name2: Second name string
        match_mode: 'approx' for approximate, 'exact' for exact matching
    
    Returns:
        float: Similarity score between 0 and 1
    """
    bm = BeiderMorse(match_mode=match_mode)
    lev = Levenshtein()
    
    # Tokenize names into components
    tokens1 = name1.lower().split()
    tokens2 = name2.lower().split()
    
    # Handle different length names
    max_len = max(len(tokens1), len(tokens2))
    min_len = min(len(tokens1), len(tokens2))
    
    total_similarity = 0
    
    # Compare each token position
    for i in range(max_len):
        if i < len(tokens1) and i < len(tokens2):
            token1 = tokens1[i]
            token2 = tokens2[i]
            
            # Get phonetic encodings
            encodings1 = set(bm.encode(token1).split())
            encodings2 = set(bm.encode(token2).split())
            
            # Method 1: Check for exact phonetic overlap
            if encodings1.intersection(encodings2):
                token_sim = 1.0
            else:
                # Method 2: Find best similarity among all encoding pairs
                max_sim = 0
                for e1 in encodings1:
                    for e2 in encodings2:
                        sim = lev.sim(e1, e2)
                        max_sim = max(max_sim, sim)
                token_sim = max_sim
            
            total_similarity += token_sim
        else:
            # Penalty for missing tokens
            total_similarity += 0
    
    # Average similarity across all token positions
    # Penalize for length mismatch
    length_penalty = min_len / max_len
    avg_similarity = (total_similarity / max_len) * length_penalty
    
    return avg_similarity


# Example usage
name1 = "anjane s varkey"
name2 = "anjana s marimuthu"

similarity = compute_name_similarity(name1, name2)
print(f"Name 1: {name1}")
print(f"Name 2: {name2}")
print(f"Similarity Score: {similarity:.4f}")
print()

# Show token-by-token comparison
bm = BeiderMorse()
tokens1 = name1.lower().split()
tokens2 = name2.lower().split()

print("Token-by-token phonetic encodings:")
print("-" * 60)
for i in range(max(len(tokens1), len(tokens2))):
    if i < len(tokens1):
        enc1 = bm.encode(tokens1[i])
        print(f"Token {i+1} (Name 1): '{tokens1[i]}' -> {enc1}")
    if i < len(tokens2):
        enc2 = bm.encode(tokens2[i])
        print(f"Token {i+1} (Name 2): '{tokens2[i]}' -> {enc2}")
    print()

# Test with more examples
print("\n" + "="*60)
print("Additional Examples:")
print("="*60)

test_cases = [
    ("anjane s varkey", "anjana s marimuthu"),
    ("john smith", "jon smyth"),
    ("christopher brown", "kristopher browne"),
    ("robert johnson", "roberto gonzalez"),
]

for n1, n2 in test_cases:
    sim = compute_name_similarity(n1, n2)
    print(f"\n'{n1}' vs '{n2}'")
    print(f"Similarity: {sim:.4f}")
