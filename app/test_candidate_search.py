from app.search_candidates import search_for_candidates


job_description = """
We are hiring a Data Scientist.

Required skills:

Python
SQL
Pandas
Scikit-learn
Machine Learning

Preferred skills:

NLP
Generative AI
AWS
Docker

The candidate should have experience
developing machine learning models and
working with data.
"""


results = search_for_candidates(
    job_description,
    top_k=5
)


print(
    "\n========== TOP CANDIDATES ==========\n"
)


for index, candidate in enumerate(
    results,
    start=1
):

    print(
        f"Rank {index}"
    )

    print(
        "Candidate:",
        candidate["candidate_name"]
    )

    print(
        "Candidate ID:",
        candidate["candidate_id"]
    )

    print(
        "Vector Distance:",
        candidate["similarity_score"]
    )

    print(
        "-" * 50
    )