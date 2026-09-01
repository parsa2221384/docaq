# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# torch نسخهٔ CPU، جدا و اول — حدود ۲ گیگ صرفه‌جویی
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=600 \
        torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=600 -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]