from app.schemas import ResumeProfile, JobProfile
from app.embeddings import calculate_similarity
import re


def calculate_skill_match(
    candidate_skills: list[str],
    required_skills: list[str]
) -> float:

    if not required_skills:
        return 0.0

    candidate_skills_normalized = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    required_skills_normalized = {
        skill.lower().strip()
        for skill in required_skills
    }

    matched_skills = (
        candidate_skills_normalized
        & required_skills_normalized
    )

    score = (
        len(matched_skills)
        / len(required_skills_normalized)
    ) * 100

    return round(score, 2)


def calculate_preferred_match(
    candidate_skills: list[str],
    preferred_skills: list[str]
) -> float:

    if not preferred_skills:
        return 0.0

    candidate_skills_normalized = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    preferred_skills_normalized = {
        skill.lower().strip()
        for skill in preferred_skills
    }

    matched_skills = (
        candidate_skills_normalized
        & preferred_skills_normalized
    )

    score = (
        len(matched_skills)
        / len(preferred_skills_normalized)
    ) * 100

    return round(score, 2)


def calculate_experience_match(
    candidate: ResumeProfile,
    job: JobProfile
) -> float:

    required_years = job.minimum_experience

    if required_years <= 0:
        return 100.0

    candidate_years = 0.0

    for experience in candidate.experience:

        duration = experience.duration.lower()

        # Look for values such as:
        # "2 years"
        # "2+ years"
        # "1.5 years"
        match = re.search(
            r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
            duration
        )

        if match:
            candidate_years += float(match.group(1))

    if candidate_years >= required_years:
        return 100.0

    score = (
        candidate_years / required_years
    ) * 100

    return round(score, 2)


def calculate_semantic_skill_match(
    candidate_skills: list[str],
    required_skills: list[str]
) -> float:

    if not candidate_skills or not required_skills:
        return 0.0

    matched_scores = []

    for required_skill in required_skills:

        best_similarity = 0.0

        for candidate_skill in candidate_skills:

            similarity = calculate_similarity(
                candidate_skill,
                required_skill
            )

            if similarity > best_similarity:
                best_similarity = similarity

        matched_scores.append(best_similarity)

    average_similarity = (
        sum(matched_scores)
        / len(matched_scores)
    )

    return round(
        average_similarity * 100,
        2
    )


def calculate_match(
    candidate: ResumeProfile,
    job: JobProfile
):

    required_score = calculate_skill_match(
        candidate.skills,
        job.required_skills
    )

    preferred_score = calculate_preferred_match(
        candidate.skills,
        job.preferred_skills
    )

    experience_score = calculate_experience_match(
        candidate,
        job
    )

    semantic_score = calculate_semantic_skill_match(
        candidate.skills,
        job.required_skills
    )

    # Final weighted score
    final_score = (
        required_score * 0.50
        + semantic_score * 0.30
        + preferred_score * 0.10
        + experience_score * 0.10
    )

    return {
        "required_skill_score": required_score,
        "semantic_skill_score": semantic_score,
        "preferred_skill_score": preferred_score,
        "experience_score": experience_score,
        "final_score": round(final_score, 2)
    }