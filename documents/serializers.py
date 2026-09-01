from rest_framework import serializers

from .models import Document
from .utils import extract_text_from_docx
#from .vector_store import add_document
from .rag.vector_store import index_document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "content",
            "created_at",
        ]

    def validate_file(self, file):
        if not file.name.lower().endswith(".docx"):
            raise serializers.ValidationError(
                "Only .docx files are supported."
            )

        return file

    def validate(self, attrs):
        if self.instance is None and not attrs.get("file"):
            raise serializers.ValidationError({
                "file": "A DOCX file is required."
            })

        return attrs

    def create(self, validated_data):
        uploaded_file = validated_data["file"]

        # Extract text from the uploaded DOCX file.
        validated_data["content"] = extract_text_from_docx(
            uploaded_file
        )

        # Save the Document in the database.
        document = super().create(validated_data)

        # Create its embedding and store it in Chroma.
        index_document(document)

        return document

    def update(self, instance, validated_data):
        uploaded_file = validated_data.get("file")

        # If a new DOCX file was uploaded, extract its new content.
        if uploaded_file:
            validated_data["content"] = extract_text_from_docx(
                uploaded_file
            )

        # Update the Document in the database.
        document = super().update(
            instance,
            validated_data,
        )

        # Create/update its embedding in Chroma.
        index_document(document)

        return document

