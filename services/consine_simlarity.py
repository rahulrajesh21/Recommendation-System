import math

def consine_simlarity(target_embedding:list[float],candidate_embedding:list[float]) -> float:

    dot_product = 0
    mag_a = 0
    mag_b = 0
    for i in range(len(target_embedding)):
        dot_product += target_embedding[i]*candidate_embedding[i]
        mag_a += math.pow(target_embedding[i],2)
        mag_b += math.pow(candidate_embedding[i],2)
    mag_a = math.sqrt(mag_a)
    mag_b = math.sqrt(mag_b)

    cosine_sim = dot_product/(mag_a * mag_b)

    return cosine_sim

    