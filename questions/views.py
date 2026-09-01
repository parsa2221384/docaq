import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question
from .serializers import QuestionSerializer
from .services import answer_question


logger = logging.getLogger(__name__)


class QuestionListCreateAPIView(APIView):
    def get(self, request):
        questions = Question.objects.all().order_by(
            "-created_at"
        )

        serializer = QuestionSerializer(
            questions,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = QuestionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        question = serializer.save()

        try:
            answer = answer_question(
                question.question
            )

        except Exception:
            logger.exception(
                "Failed to generate answer."
            )

            return Response(
                {
                    "detail": (
                        "Unable to generate an answer "
                        "at this time."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        question.answer = answer
        question.save(
            update_fields=["answer"]
        )

        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )