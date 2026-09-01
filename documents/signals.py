from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Document
from .rag.vector_store import vector_store


@receiver(post_delete, sender=Document)
def delete_document_vectors(sender, instance, **kwargs):
    vector_store.delete(
        where={
            "document_id": instance.id,
        }
    )