import logging

from documents.rag.chain import rag_chain


logger = logging.getLogger(__name__)


def answer_question(question: str) -> str:
    logger.info("Starting RAG pipeline.")

    try:
        answer = rag_chain.invoke(question)

        logger.info(
            "RAG pipeline completed successfully."
        )

        return answer

    except Exception:
        logger.exception(
            "RAG pipeline failed."
        )
        raise