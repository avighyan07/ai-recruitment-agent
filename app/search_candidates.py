from app.vector_store import search_candidates


def search_for_candidates(
    job_description: str,
    top_k: int = 5
):

    results = search_candidates(
        job_description,
        k=top_k
    )

    candidates = []

    for document, score in results:

        candidates.append({
            "candidate_id": document.metadata[
                "candidate_id"
            ],
            "candidate_name": document.metadata[
                "candidate_name"
            ],
            "resume_text": document.page_content,
            "similarity_score": score
        })

    return candidates