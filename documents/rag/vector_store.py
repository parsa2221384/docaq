
from langchain_chroma import Chroma

from .embeddings import embeddings
from .splitter import split_document
import os
import logging

logger = logging.getLogger(__name__)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    "vector_db",
)

vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory=VECTOR_DB_PATH,
)


def index_document(document):
    logger.info(
        "Indexing document %s.",
        document.id,
    )

    chunks = split_document(document)

    vector_store.delete(
        where={
            "document_id": document.id,
        }
    )

    if not chunks:
        return

    vector_store.add_documents(chunks)
    logger.info(
        "Document %s indexed successfully.",
        document.id,
    )

