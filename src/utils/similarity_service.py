import math

def dot_product(a: list[float], b: list[float]) -> float:
    if(len(a) != len(b)):
        raise ValueError("Vectors must have same length.")
    
    total = 0.0

    for x, y in zip(a, b):
        total += x*y
    return total

def magnitude(vector: list[float]) -> float:
    sum_square = 0.0

    for v in vector:
        sum_square += v * v
    
    return math.sqrt(sum_square)

def cosine_similarity(a: list[float], b: list[float]) -> float:
    magnitude_a = magnitude(a)
    magnitude_b = magnitude(b)

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cannot calculate cosine similarity for a zero vector.")

    return dot_product(a, b) / (magnitude_a * magnitude_b)