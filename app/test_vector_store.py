from app.vector_store import (
    add_candidate,
    search_candidates
)


# --------------------------------
# Add candidates
# --------------------------------

add_candidate(
    candidate_id="candidate_1",
    candidate_name="Avighyan",
    resume_text="""
    Python developer with experience in
    Machine Learning, Deep Learning,
    FastAPI, LangChain and NLP.
    """
)


add_candidate(
    candidate_id="candidate_2",
    candidate_name="Rahul",
    resume_text="""
    Java developer with experience in
    Spring Boot, Java, SQL and REST APIs.
    """
)


add_candidate(
    candidate_id="candidate_3",
    candidate_name="Priya",
    resume_text="""
    Data Scientist experienced in Python,
    Pandas, Scikit-learn, Machine Learning,
    SQL and Data Analysis.
    """
)


# --------------------------------
# Search
# --------------------------------

job_description = """
Looking for a Data Scientist with
Python, Machine Learning, SQL and
Scikit-learn experience.
"""


results = search_candidates(
    job_description,
    k=3
)


# --------------------------------
# Display
# --------------------------------

print("\n========== SEARCH RESULTS ==========\n")


for document, score in results:

    print(
        "Candidate:",
        document.metadata["candidate_name"]
    )

    print(
        "ID:",
        document.metadata["candidate_id"]
    )

    print(
        "Score:",
        score
    )

    print(
        "Resume:",
        document.page_content
    )

    print("-" * 50)