from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template(
    """
You are a document question-answering assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context,
say that the information is not available in the documents.

Context:
{context}

Question:
{question}
"""
)