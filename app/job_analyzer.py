from app.llm import llm
from app.schemas import JobProfile


structured_llm = llm.with_structured_output(JobProfile)


def analyze_job_description(job_description: str) -> JobProfile:

    prompt = f"""
You are an expert recruitment analyst.

Analyze the following job description and extract the
important hiring requirements.

Rules:
- Do not invent requirements.
- Separate required skills from preferred skills.
- Extract the minimum years of experience.
- Extract the main responsibilities.
- If a value is not specified, use an empty list or 0.
- Preserve the terminology used in the job description.

Job Description:

{job_description}
"""

    result = structured_llm.invoke(prompt)

    return result