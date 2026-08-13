from app.embeddings import calculate_similarity


pairs = [
    (
        "NLP",
        "Natural Language Processing"
    ),
    (
        "Python programming",
        "Python development"
    ),
    (
        "Machine Learning",
        "Cooking recipes"
    ),
    (
        "AWS cloud",
        "Amazon Web Services"
    )
]


for text1, text2 in pairs:

    similarity = calculate_similarity(
        text1,
        text2
    )

    print(
        f"\n{text1} <-> {text2}"
    )

    print(
        "Similarity:",
        similarity
    )