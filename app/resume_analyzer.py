from app.llm import llm
from app.schemas import ResumeProfile


structured_llm = llm.with_structured_output(ResumeProfile)


def analyze_resume(resume_text: str) -> ResumeProfile:

    prompt = f"""
You are an expert recruitment resume parser.

Analyze the following resume and extract the candidate's
information accurately.

Rules:
- Do not invent information.
- If information is missing, use an empty string or empty list.
- Extract only information explicitly present in the resume.
- Preserve the candidate's actual skills, experience, education,
  and projects.

Resume:

{resume_text}
"""

    result = structured_llm.invoke(prompt)

    return result