from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "question",
            "answer",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "answer",
            "created_at",
        ]

    def validate_question(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Question cannot be empty."
            )

        return value