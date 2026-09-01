from .vector_store import vector_store


retriever = vector_store.as_retriever(
    search_kwargs={"k": 5},
)