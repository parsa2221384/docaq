from documents.vector_store import search_documents


query = "What is Django?"

results = search_documents(
    query,
    top_k=3,
)

print(results)