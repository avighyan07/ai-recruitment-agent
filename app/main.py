from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid

from app.schemas import JobRequest

from app.recruitment_graph import (
    recruitment_graph
)

from app.resume_parser import (
    extract_resume
)

from app.resume_analyzer import (
    analyze_resume
)

from app.vector_store import (
    add_candidate
)


# =====================================
# FASTAPI APPLICATION
# =====================================

app = FastAPI(
    title="AI Recruitment Agent",
    description=(
        "GenAI powered resume screening, "
        "candidate matching and ranking system"
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =====================================
# DIRECTORIES
# =====================================

UPLOAD_DIRECTORY = Path("uploads")

UPLOAD_DIRECTORY.mkdir(
    exist_ok=True
)


# =====================================
# HOME
# =====================================

# =====================================
# SERVE FRONTEND
# =====================================

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# =====================================
# UPLOAD MULTIPLE RESUMES
# =====================================
@app.post("/test-upload")
async def test_upload(
    files: list[UploadFile] = File(...)
):
    return {
        "count": len(files),
        "files": [file.filename for file in files]
    }
@app.post("/upload-resumes")
async def upload_resumes(
    files: List[UploadFile] = File(...)
):
    uploaded_candidates = []

    # =================================
    # Process every uploaded file
    # =================================

    for file in files:

        # ---------------------------------
        # Validate PDF
        # ---------------------------------

        if not file.filename.lower().endswith(".pdf"):

            uploaded_candidates.append({

                "filename":
                    file.filename,

                "success":
                    False,

                "error":
                    "Only PDF files are allowed."
            })

            continue

        try:

            # ---------------------------------
            # Generate unique candidate ID
            # ---------------------------------

            candidate_id = str(
                uuid.uuid4()
            )

            # ---------------------------------
            # Save PDF
            # ---------------------------------

            file_path = (
                UPLOAD_DIRECTORY
                / f"{candidate_id}.pdf"
            )

            with open(
                file_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            print(
                f"\nProcessing resume: "
                f"{file.filename}"
            )

            # ---------------------------------
            # Extract resume text
            # ---------------------------------

            documents = extract_resume(
                str(file_path)
            )

            resume_text = "\n".join(
                document.page_content
                for document in documents
            )

            # ---------------------------------
            # Analyze resume using LLM
            # ---------------------------------

            candidate = analyze_resume(
                resume_text
            )

            print(
                f"Candidate detected: "
                f"{candidate.name}"
            )

            # ---------------------------------
            # Store candidate in ChromaDB
            # ---------------------------------

            add_candidate(

                candidate_id=
                    candidate_id,

                resume_text=
                    resume_text,

                candidate_name=
                    candidate.name,

                email=
                    candidate.email,

                skills=
                    candidate.skills,

                experience=[
                    exp.duration
                    for exp
                    in candidate.experience
                ]
            )

            print(
                f"Successfully indexed: "
                f"{candidate.name}"
            )

            # ---------------------------------
            # Successful response
            # ---------------------------------

            uploaded_candidates.append({

                "filename":
                    file.filename,

                "success":
                    True,

                "candidate_id":
                    candidate_id,

                "candidate_name":
                    candidate.name,

                "email":
                    candidate.email,

                "skills":
                    candidate.skills
            })

        except Exception as e:

            print(
                f"Error processing "
                f"{file.filename}: {e}"
            )

            uploaded_candidates.append({

                "filename":
                    file.filename,

                "success":
                    False,

                "error":
                    str(e)
            })

    # =================================
    # Calculate statistics
    # =================================

    successful = sum(
        1
        for candidate
        in uploaded_candidates
        if candidate["success"]
    )

    failed = (
        len(uploaded_candidates)
        - successful
    )

    # =================================
    # Final response
    # =================================

    return {

        "success":
            True,

        "total_files":
            len(files),

        "successful":
            successful,

        "failed":
            failed,

        "candidates":
            uploaded_candidates
    }


# =====================================
# RECRUIT CANDIDATES
# =====================================

@app.post("/recruit")
def recruit_candidates(
    request: JobRequest
):

    try:

        print(
            "\nStarting recruitment process..."
        )

        # ---------------------------------
        # Initial LangGraph state
        # ---------------------------------

        initial_state = {

    "job_description":
        request.job_description,

    "threshold":
        request.threshold,

    "job_profile":
        None,

    "retrieved_candidates":
        [],

    "ranked_candidates":
        [],

    "recruiter_analysis":
        [],

    "final_report":
        ""
}

        # ---------------------------------
        # Run LangGraph
        # ---------------------------------

        result = recruitment_graph.invoke(
            initial_state
        )

        # ---------------------------------
        # Return result
        # ---------------------------------

        return {
                    "success": True,

                    "job_profile": result["job_profile"],

                    "candidates": result["ranked_candidates"],

                    "recruiter_analysis": result["recruiter_analysis"],

                    "report": result["final_report"]
                }

    except Exception as e:

        print(
            f"Recruitment error: {e}"
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )