from pathlib import Path

from app.vector_store import search_candidates
from app.resume_parser import extract_resume
from app.resume_analyzer import analyze_resume
from app.job_analyzer import analyze_job_description
from app.matcher import calculate_match


RESUME_DIRECTORY = "resumes"


def get_resume_file(candidate_id: str):

    resume_directory = Path(
        RESUME_DIRECTORY
    )

    index = candidate_id.replace(
        "candidate_",
        ""
    )

    pdf_files = list(
        resume_directory.glob("*.pdf")
    )

    try:

        index = int(index)

        return pdf_files[index - 1]

    except (ValueError, IndexError):

        return None


def load_candidate_profile(
    candidate_id: str
):

    pdf_file = get_resume_file(
        candidate_id
    )

    if pdf_file is None:
        return None

    documents = extract_resume(
        str(pdf_file)
    )

    resume_text = "\n".join(
        document.page_content
        for document in documents
    )

    candidate = analyze_resume(
        resume_text
    )

    return candidate


def run_recruitment_pipeline(
    job_description: str,
    top_k: int = 5
):

    # --------------------------------
    # Step 1: Analyze Job Description
    # --------------------------------

    job = analyze_job_description(
        job_description
    )

    # --------------------------------
    # Step 2: Retrieve candidates
    # --------------------------------

    retrieved_candidates = (
        search_candidates(
            job_description,
            k=top_k
        )
    )

    final_candidates = []

    # --------------------------------
    # Step 3: Detailed matching
    # --------------------------------

    for document, distance in (
        retrieved_candidates
    ):

        candidate_id = (
            document.metadata[
                "candidate_id"
            ]
        )

        candidate = load_candidate_profile(
            candidate_id
        )

        if candidate is None:
            continue

        match_result = calculate_match(
            candidate,
            job
        )

        final_candidates.append({

            "candidate_id":
                candidate_id,

            "candidate_name":
                candidate.name,

            "email":
                candidate.email,

            "vector_distance":
                distance,

            "required_skill_score":
                match_result[
                    "required_skill_score"
                ],

            "semantic_skill_score":
                match_result[
                    "semantic_skill_score"
                ],

            "preferred_skill_score":
                match_result[
                    "preferred_skill_score"
                ],

            "experience_score":
                match_result[
                    "experience_score"
                ],

            "final_score":
                match_result[
                    "final_score"
                ]
        })

    # --------------------------------
    # Step 4: Final ranking
    # --------------------------------

    final_candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    # Add ranking
    for index, candidate in enumerate(
        final_candidates,
        start=1
    ):

        candidate["rank"] = index

    return final_candidates