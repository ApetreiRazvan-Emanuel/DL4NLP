import math

S1 = "The man saw a car in the park"
S2 = "I saw the man park the car"

def euclidean_distance(v1, v2):
    squared_sum = sum((v1[i] - v2[i])**2 for i in range(len(v1)))
    return math.sqrt(squared_sum)

def cosine_similarity(v1, v2):
    dot_product = sum(v1[i] * v2[i] for i in range(len(v1)))
    norm_v1 = math.sqrt(sum(x**2 for x in v1))
    norm_v2 = math.sqrt(sum(x**2 for x in v2))
    return dot_product / (norm_v1 * norm_v2)

def jaccard_similarity(s1, s2):
    intersection = s1 & s2
    union = s1 | s2
    return len(intersection) / len(union)

def overlap_coefficient(s1, s2):
    intersection = s1 & s2
    return len(intersection) / min(len(s1), len(s2))

s1_tokens = S1.lower().split()
s2_tokens = S2.lower().split()

vocab = sorted(set(s1_tokens + s2_tokens))

v1 = [s1_tokens.count(word) for word in vocab]
v2 = [s2_tokens.count(word) for word in vocab]

set1 = set(s1_tokens)
set2 = set(s2_tokens)

print("S1:", S1)
print("S2:", S2)
print()
print("Vocabulary:", vocab)
print()
print("Vector S1:", v1)
print("Vector S2:", v2)
print()
print("Set S1:", set1)
print("Set S2:", set2)
print()

euc_dist = euclidean_distance(v1, v2)
euc_sim = 1 / (1 + euc_dist)
print(f"a) Euclidean distance: {euc_dist:.4f}")
print(f"   Euclidean similarity: {euc_sim:.4f}")
print()

cos_sim = cosine_similarity(v1, v2)
print(f"b) Cosine similarity: {cos_sim:.4f}")
print()

jac_sim = jaccard_similarity(set1, set2)
print(f"c) Jaccard similarity: {jac_sim:.4f}")
print()

ovr_coef = overlap_coefficient(set1, set2)
print(f"d) Overlap coefficient: {ovr_coef:.4f}")