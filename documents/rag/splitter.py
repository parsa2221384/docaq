from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangChainDocument

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

def split_document(document):
    langchain_document = LangChainDocument(
        page_content=document.content,
        metadata={
            "document_id": document.id,
            "title": document.title,
        },
    )

    chunks = text_splitter.split_documents(
        [langchain_document]
    )

    for chunk_index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = chunk_index

    return chunks

#Django Document
#       ↓
#LangChain Document