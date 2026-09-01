from unittest.mock import patch

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Question


class QuestionModelTests(TestCase):
    def test_create_question(self):
        question = Question.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
        )

        self.assertEqual(
            question.question,
            "What is Django?",
        )

        self.assertEqual(
            question.answer,
            "Django is a web framework.",
        )

        self.assertIsNotNone(
            question.created_at,
        )


class QuestionAPITests(APITestCase):
    @patch("questions.views.answer_question")
    def test_create_question(
        self,
        mock_answer_question,
    ):
        mock_answer_question.return_value = (
            "Django is a Python web framework."
        )

        response = self.client.post(
            "/api/questions/",
            {
                "question": "What is Django?",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Question.objects.count(),
            1,
        )

        question = Question.objects.first()

        self.assertEqual(
            question.question,
            "What is Django?",
        )

        self.assertEqual(
            question.answer,
            "Django is a Python web framework.",
        )

        mock_answer_question.assert_called_once_with(
            "What is Django?"
        )

    def test_empty_question_rejected(self):
        response = self.client.post(
            "/api/questions/",
            {
                "question": "   ",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_question_history(self):
        Question.objects.create(
            question="Question 1",
            answer="Answer 1",
        )

        Question.objects.create(
            question="Question 2",
            answer="Answer 2",
        )

        response = self.client.get(
            "/api/questions/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )