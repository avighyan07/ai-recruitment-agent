from typing import TypedDict


class RecruitmentState(TypedDict):

    job_description: str

    threshold: float

    job_profile: object

    retrieved_candidates: list

    ranked_candidates: list

    recruiter_analysis: list

    final_report: str