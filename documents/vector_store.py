import chromadb
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL_NAME = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


chroma_client = chromadb.PersistentClient(
    path="vector_db"
)

collection = chroma_client.get_or_create_collection(
    name="documents"
)

def add_document(document):
    embedding = embedding_model.encode(
        document.content
    ).tolist()

    collection.upsert(
        ids=[str(document.id)],
        embeddings=[embedding],
        documents=[document.content],
        metadatas=[
            {
                "document_id": document.id,
                "title": document.title,
            }
        ],
    )


def search_documents(query, top_k=5):
    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results





#Python code
#    ↓
#chromadb Python API
#    ↓
#Client
#    ↓
#Chroma storage