from langchain_community.document_loaders import PyPDFLoader


def extract_resume(file_path: str):

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents