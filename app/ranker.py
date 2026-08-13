from app.schemas import ResumeProfile, JobProfile
from app.matcher import calculate_match


def rank_candidates(
    candidates: list[ResumeProfile],
    job: JobProfile
):

    ranked_candidates = []

    for candidate in candidates:

        match_result = calculate_match(
            candidate,
            job
        )

        ranked_candidates.append({
            "candidate_name": candidate.name,
            "email": candidate.email,
            "match_score": match_result["final_score"],
            "required_skill_score": match_result["required_skill_score"],
            "semantic_skill_score": match_result["semantic_skill_score"],
            "preferred_skill_score": match_result["preferred_skill_score"],
            "experience_score": match_result["experience_score"]
        })

    # Highest score first
    ranked_candidates.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    # Add rank
    for index, candidate in enumerate(
        ranked_candidates,
        start=1
    ):
        candidate["rank"] = index

    return ranked_candidates