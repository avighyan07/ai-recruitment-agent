from app.recruitment_pipeline import (
    run_recruitment_pipeline
)


job_description = """
We are hiring a Data Scientist.

Required Skills:

- Python
- SQL
- Pandas
- Scikit-learn
- Machine Learning

Preferred Skills:

- NLP
- Generative AI
- AWS
- Docker

Responsibilities:

- Develop machine learning models.
- Analyze datasets.
- Build predictive models.
- Work with data science teams.
"""


results = run_recruitment_pipeline(
    job_description,
    top_k=5
)


print(
    "\n========================================"
)

print(
    "       FINAL CANDIDATE RANKING"
)

print(
    "========================================\n"
)


for candidate in results:

    print(
        f"Rank: {candidate['rank']}"
    )

    print(
        f"Name: {candidate['candidate_name']}"
    )

    print(
        f"Email: {candidate['email']}"
    )

    print(
        f"Final Score: "
        f"{candidate['final_score']}%"
    )

    print(
        f"Required Skills: "
        f"{candidate['required_skill_score']}%"
    )

    print(
        f"Semantic Skills: "
        f"{candidate['semantic_skill_score']}%"
    )

    print(
        f"Preferred Skills: "
        f"{candidate['preferred_skill_score']}%"
    )

    print(
        f"Experience: "
        f"{candidate['experience_score']}%"
    )

    print(
        "-" * 50
    )