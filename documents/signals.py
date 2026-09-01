from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Document
from .rag.vector_store import index_document, vector_store


@receiver(post_save, sender=Document)
def index_saved_document(sender, instance, **kwargs):
    index_document(instance)


@receiver(post_delete, sender=Document)
def delete_document_vectors(sender, instance, **kwargs):
    vector_store.delete(
        where={
            "document_id": instance.id,
        }
    )