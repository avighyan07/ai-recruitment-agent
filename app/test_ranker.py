from app.resume_parser import extract_resume
from app.resume_analyzer import analyze_resume

from app.job_analyzer import analyze_job_description
from app.ranker import rank_candidates


# -----------------------------
# Load resume
# -----------------------------

PDF_PATH = "uploads/Avighyan_Chakraborty_CSE_Resume.pdf"

documents = extract_resume(PDF_PATH)

resume_text = "\n".join(
    document.page_content
    for document in documents
)

candidate = analyze_resume(resume_text)


# -----------------------------
# Job Description
# -----------------------------

job_description = """
We are looking for a Data Scientist.

Requirements:
- Python
- SQL
- Pandas
- Scikit-learn
- Machine Learning

Preferred:
- AWS
- Docker
- NLP
- Generative AI

Responsibilities:
- Develop machine learning models.
- Analyze datasets.
- Build predictive models.
"""

job = analyze_job_description(
    job_description
)


# -----------------------------
# Candidates
# -----------------------------

candidates = [
    candidate,
    candidate,
    candidate
]


# -----------------------------
# Ranking
# -----------------------------

ranked = rank_candidates(
    candidates,
    job
)


# -----------------------------
# Display
# -----------------------------

print("\n========== CANDIDATE RANKING ==========\n")

for candidate in ranked:

    print(
        f"Rank {candidate['rank']}: "
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

    print("-" * 40)