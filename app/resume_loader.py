from pathlib import Path

from app.resume_parser import extract_resume
from app.resume_analyzer import analyze_resume


def load_candidates(
    resume_directory: str
):

    resume_path = Path(resume_directory)

    candidates = []

    pdf_files = list(
        resume_path.glob("*.pdf")
    )

    print(
        f"Found {len(pdf_files)} resume(s)."
    )

    for pdf_file in pdf_files:

        print(
            f"\nProcessing: {pdf_file.name}"
        )

        try:

            documents = extract_resume(
                str(pdf_file)
            )

            resume_text = "\n".join(
                document.page_content
                for document in documents
            )

            candidate = analyze_resume(
                resume_text
            )

            candidates.append(candidate)

            print(
                f"Successfully processed: "
                f"{candidate.name}"
            )

        except Exception as e:

            print(
                f"Failed to process "
                f"{pdf_file.name}: {e}"
            )

    return candidates