from minsearch import Index
from gitsource import GithubRepositoryDataReader
from gitsource import chunk_documents


def load_faq_data():
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )
    files = reader.read()
    # Cleaner list comprehension
    documents = [file.parse() for file in files]
    
    return documents


def build_index(documents):
    index = Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    
    index.fit(documents)
    return index
