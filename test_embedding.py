from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

texts = [
    "Django is a Python web framework.",
    "Django یک فریم‌ورک وب پایتون است.",
    "Football is a popular sport.",
]

embeddings = model.encode(texts)

similarity_01 = model.similarity(
    embeddings[0],
    embeddings[1],
)

similarity_02 = model.similarity(
    embeddings[0],
    embeddings[2],
)

print("Similarity Django/Django:", similarity_01)
print("Similarity Django/Football:", similarity_02)

print("------------------------")

import chromadb


client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    name="documents"
)

results = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

print(results)
print(results)