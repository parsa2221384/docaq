from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL_NAME = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME
)