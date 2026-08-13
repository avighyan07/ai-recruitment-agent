from pydantic import BaseModel, Field
from typing import List


class Experience(BaseModel):
    company: str = Field(description="Company name")
    role: str = Field(description="Job title or role")
    duration: str = Field(description="Duration of employment")
    responsibilities: List[str] = Field(
        description="Main responsibilities"
    )


class Education(BaseModel):
    institution: str = Field(description="Educational institution")
    degree: str = Field(description="Degree or qualification")
    field_of_study: str = Field(description="Field of study")
    duration: str = Field(description="Study duration")
    grade: str = Field(description="CGPA, GPA, percentage, or grade")


class Project(BaseModel):
    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    technologies: List[str] = Field(
        description="Technologies used"
    )


class ResumeProfile(BaseModel):
    name: str = Field(description="Candidate full name")
    email: str = Field(description="Candidate email address")
    phone: str = Field(description="Candidate phone number")

    skills: List[str] = Field(
        description="Technical and professional skills"
    )

    experience: List[Experience] = Field(
        description="Professional experience"
    )

    education: List[Education] = Field(
        description="Educational background"
    )

    projects: List[Project] = Field(
        description="Projects mentioned in the resume"
    )
    
    
class JobProfile(BaseModel):
    job_title: str = Field(
        description="Job title"
    )

    required_skills: List[str] = Field(
        description="Skills explicitly required for the job"
    )

    preferred_skills: List[str] = Field(
        description="Skills mentioned as preferred, optional, or nice-to-have"
    )

    minimum_experience: float = Field(
        description="Minimum years of experience required"
    )

    responsibilities: List[str] = Field(
        description="Main responsibilities of the role"
    )    
    
from pydantic import BaseModel


from pydantic import BaseModel, Field


class JobRequest(BaseModel):

    job_description: str

    threshold: float = Field(
        default=30.0,
        ge=0,
        le=100
    )  
    
from pydantic import BaseModel, Field
from typing import List


class RecruiterAnalysis(BaseModel):

    recommendation: str = Field(
        description="Hiring recommendation such as Strong Hire, Consider, or Reject"
    )

    strengths: List[str] = Field(
        description="Candidate strengths relevant to the job"
    )

    gaps: List[str] = Field(
        description="Missing or weak areas relevant to the job"
    )

    summary: str = Field(
        description="Concise recruiter-style explanation"
    )    