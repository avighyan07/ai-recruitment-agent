from pathlib import Path

from app.resume_parser import extract_resume
from app.resume_analyzer import analyze_resume
from app.vector_store import add_candidate


RESUME_DIRECTORY = "resumes"


def index_resumes():

    resume_directory = Path(RESUME_DIRECTORY)

    pdf_files = list(
        resume_directory.glob("*.pdf")
    )

    print(
        f"Found {len(pdf_files)} resume(s).\n"
    )

    for index, pdf_file in enumerate(
        pdf_files,
        start=1
    ):

        print(
            f"Processing {pdf_file.name}..."
        )

        try:

            # Extract PDF text
            documents = extract_resume(
                str(pdf_file)
            )

            resume_text = "\n".join(
                document.page_content
                for document in documents
            )

            # Convert resume into structured profile
            candidate = analyze_resume(
                resume_text
            )

            # Store in ChromaDB
            add_candidate(
                candidate_id=f"candidate_{index}",
                resume_text=resume_text,
                candidate_name=candidate.name,
                email=candidate.email,
                skills=candidate.skills,
                experience=[
                    exp.duration
                    for exp in candidate.experience
                ]
            )

            print(
                f"✓ Added {candidate.name}"
            )

        except Exception as e:

            print(
                f"✗ Failed: {pdf_file.name}"
            )

            print(
                f"  Error: {e}"
            )

    print(
        "\nResume indexing completed."
    )


if __name__ == "__main__":
    index_resumes()