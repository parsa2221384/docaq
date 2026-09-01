from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from .prompt import prompt
from .retriever import retriever
from .llm import llm


def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

#documents/rag/chain.py
#        │
#        ▼
#documents/rag/retriever.py
#        │
#        ▼
#documents/rag/vector_store.py
#        │
#        ├──────────────► embeddings.py
#        │
#        ▼
#      Chroma