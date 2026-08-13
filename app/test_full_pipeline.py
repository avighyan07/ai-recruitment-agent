from app.resume_loader import load_candidates
from app.job_analyzer import analyze_job_description
from app.ranker import rank_candidates


# =====================================
# 1. Load all resumes
# =====================================

candidates = load_candidates(
    "resumes"
)


# =====================================
# 2. Job Description
# =====================================

job_description = """
We are looking for a Data Scientist
to join our AI team.

Requirements:

- Strong Python programming skills.
- Strong SQL knowledge.
- Experience with Pandas.
- Experience with Scikit-learn.
- Experience with Machine Learning.

Preferred:

- AWS
- Docker
- NLP
- Generative AI

Responsibilities:

- Develop machine learning models.
- Analyze large datasets.
- Build predictive models.
- Collaborate with software engineers.
"""


job = analyze_job_description(
    job_description
)


# =====================================
# 3. Rank candidates
# =====================================

ranked_candidates = rank_candidates(
    candidates,
    job
)


# =====================================
# 4. Display ranking
# =====================================

print(
    "\n\n========== FINAL CANDIDATE RANKING ==========\n"
)


for candidate in ranked_candidates:

    print(
        f"Rank {candidate['rank']}"
    )

    print(
        f"Candidate: "
        f"{candidate['candidate_name']}"
    )

    print(
        f"Match Score: "
        f"{candidate['match_score']}%"
    )

    print(
        f"Required Skills: "
        f"{candidate['required_skill_score']}%"
    )

    print(
        f"Semantic Match: "
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