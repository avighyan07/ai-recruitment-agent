from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


vector_store = Chroma(
    collection_name="candidate_resumes",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def add_candidate(
    candidate_id: str,
    resume_text: str,
    candidate_name: str,
    email: str,
    skills: list[str],
    experience: list[str]
):

    vector_store.add_texts(
        texts=[resume_text],

        metadatas=[
            {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "email": email,
                "skills": ", ".join(skills),
                "experience": " | ".join(experience)
            }
        ],

        ids=[candidate_id]
    )


def search_candidates(
    job_description: str,
    k: int = 5
):

    return vector_store.similarity_search_with_score(
        job_description,
        k=k
    )