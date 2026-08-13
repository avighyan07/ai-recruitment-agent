from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):

    return model.encode(
        text,
        normalize_embeddings=True
    )


def calculate_similarity(
    text1: str,
    text2: str
) -> float:

    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)

    similarity = np.dot(
        embedding1,
        embedding2
    )

    return round(float(similarity), 4)