from django.core.management.base import BaseCommand

from documents.models import Document
from documents.rag.vector_store import index_document


class Command(BaseCommand):
    help = "Re-index all documents in the vector store."

    def handle(self, *args, **options):
        documents = Document.objects.all()

        total = documents.count()

        self.stdout.write(
            f"Found {total} documents."
        )

        for document in documents:
            index_document(document)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Indexed document "
                    f"{document.id}: {document.title}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Re-indexing completed."
            )
        )