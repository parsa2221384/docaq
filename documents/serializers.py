from rest_framework import serializers

from .models import Document
from .utils import extract_text_from_docx


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
        if not attrs.get("file"):
            raise serializers.ValidationError({
                "file": "A DOCX file is required."
            })

        return attrs

    def create(self, validated_data):
        uploaded_file = validated_data["file"]

        validated_data["content"] = extract_text_from_docx(
            uploaded_file
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        uploaded_file = validated_data.get("file")

        if uploaded_file:
            validated_data["content"] = extract_text_from_docx(
                uploaded_file
            )

        return super().update(instance, validated_data)