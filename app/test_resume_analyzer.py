from app.resume_parser import extract_resume
from app.resume_analyzer import analyze_resume


PDF_PATH = "uploads/Avighyan_Chakraborty_CSE_Resume.pdf"


documents = extract_resume(PDF_PATH)


resume_text = "\n".join(
    document.page_content
    for document in documents
)


profile = analyze_resume(resume_text)


print("\n========== CANDIDATE ==========")
print("Name:", profile.name)
print("Email:", profile.email)
print("Phone:", profile.phone)


print("\n========== SKILLS ==========")

for skill in profile.skills:
    print("-", skill)


print("\n========== EXPERIENCE ==========")

for experience in profile.experience:

    print("\nCompany:", experience.company)
    print("Role:", experience.role)
    print("Duration:", experience.duration)

    for responsibility in experience.responsibilities:
        print("-", responsibility)


print("\n========== EDUCATION ==========")

for education in profile.education:

    print("\nInstitution:", education.institution)
    print("Degree:", education.degree)
    print("Field:", education.field_of_study)
    print("Duration:", education.duration)
    print("Grade:", education.grade)


print("\n========== PROJECTS ==========")

for project in profile.projects:

    print("\nProject:", project.name)
    print("Description:", project.description)

    print("Technologies:")

    for technology in project.technologies:
        print("-", technology)