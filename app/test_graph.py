from app.recruitment_graph import (
    recruitment_graph
)


job_description = """
We are hiring a Data Scientist.

Required Skills:

Python
SQL
Pandas
Scikit-learn
Machine Learning

Preferred Skills:

NLP
Generative AI
AWS
Docker

Responsibilities:

Develop machine learning models,
analyze datasets and build predictive
models.
"""


initial_state = {
    "job_description": job_description,

    "job_profile": None,

    "retrieved_candidates": [],

    "ranked_candidates": [],

    "final_report": ""
}


result = recruitment_graph.invoke(
    initial_state
)


print("\n")
print(result["final_report"])