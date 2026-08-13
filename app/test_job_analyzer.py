from app.job_analyzer import analyze_job_description


job_description = """
We are looking for a Data Scientist to join our AI team.

Requirements:
- 2+ years of experience in Data Science or Machine Learning.
- Strong Python programming skills.
- Strong SQL knowledge.
- Experience with Pandas and Scikit-learn.
- Good understanding of Machine Learning algorithms.

Preferred:
- Experience with AWS.
- Knowledge of Docker.
- Experience with NLP and Generative AI.

Responsibilities:
- Develop and deploy machine learning models.
- Analyze large datasets.
- Build predictive models.
- Collaborate with software engineers and data teams.
"""


job = analyze_job_description(job_description)


print("\n========== JOB ==========")

print("Job Title:", job.job_title)

print("\nMinimum Experience:")
print(job.minimum_experience, "years")

print("\n========== REQUIRED SKILLS ==========")

for skill in job.required_skills:
    print("-", skill)


print("\n========== PREFERRED SKILLS ==========")

for skill in job.preferred_skills:
    print("-", skill)


print("\n========== RESPONSIBILITIES ==========")

for responsibility in job.responsibilities:
    print("-", responsibility)