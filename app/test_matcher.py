from app.resume_parser import extract_resume
from app.resume_analyzer import analyze_resume

from app.job_analyzer import analyze_job_description
from app.matcher import calculate_match


# -----------------------------
# 1. Load Resume
# -----------------------------

PDF_PATH = "uploads/Avighyan_Chakraborty_CSE_Resume.pdf"

documents = extract_resume(PDF_PATH)

resume_text = "\n".join(
    document.page_content
    for document in documents
)

candidate = analyze_resume(resume_text)


# -----------------------------
# 2. Job Description
# -----------------------------

job_description = """
We are looking for a Data Scientist to join our AI team.

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
- Analyze datasets.
- Build predictive models.
"""


job = analyze_job_description(job_description)


# -----------------------------
# 3. Calculate Match
# -----------------------------

result = calculate_match(
    candidate,
    job
)


# -----------------------------
# 4. Display Result
# -----------------------------

print("\n========== CANDIDATE ==========")

print("Name:", candidate.name)

print("\n========== MATCH RESULT ==========")

print(
    "Required Skill Match:",
    result["required_skill_score"],
    "%"
)

print(
    "Preferred Skill Match:",
    result["preferred_skill_score"],
    "%"
)

print(
    "Experience Match:",
    result["experience_score"],
    "%"
)

print(
    "FINAL MATCH SCORE:",
    result["final_score"],
    "%"
)

print(
    "Semantic Skill Match:",
    result["semantic_skill_score"],
    "%"
)