# API Documentation

## 1. Overview

این سند مستندات API سامانه «پرسش از اسناد» است.

API با استفاده از Django REST Framework پیاده‌سازی شده و دو resource اصلی دارد:

- `Documents`: مدیریت اسناد و فایل‌های DOCX
- `Questions`: ثبت پرسش، تولید پاسخ با RAG و مشاهده تاریخچه پرسش و پاسخ

تمام endpointهای API از مسیر پایه زیر در دسترس هستند:

```text
http://127.0.0.1:8000/api/
```

---

## 2. API Documentation Interfaces

### OpenAPI Schema

```http
GET /api/schema/
```

دریافت schema استاندارد OpenAPI.

آدرس:

```text
http://127.0.0.1:8000/api/schema/
```

### Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

Swagger UI امکان مشاهده و آزمایش تعاملی endpointهای API را فراهم می‌کند.

---

## 3. Documents API

مسیر پایه:

```text
/api/documents/
```

`Document` شامل اطلاعات زیر است:

| Field | Type | Description |
|---|---|---|
| `id` | integer | شناسه یکتا |
| `title` | string | عنوان سند |
| `file` | URL/string | مسیر فایل DOCX |
| `content` | string | متن استخراج‌شده کامل سند |
| `created_at` | datetime | زمان ایجاد سند |

فیلدهای `id`، `content` و `created_at` توسط سرور تولید می‌شوند و در درخواست ایجاد یا ویرایش قابل ورود نیستند.

### 3.1 List Documents

```http
GET /api/documents/
```

تمام اسناد موجود را برمی‌گرداند.

#### Response

```http
200 OK
```

نمونه:

```json
[
  {
    "id": 1,
    "title": "Django Basics",
    "file": "http://127.0.0.1:8000/media/documents/django_basics.docx",
    "content": "Django is a Python web framework...",
    "created_at": "2026-09-01T10:00:00Z"
  }
]
```

---

### 3.2 Create Document

```http
POST /api/documents/
```

برای ایجاد سند جدید استفاده می‌شود.

#### Content-Type

```text
multipart/form-data
```

#### Form Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | بله | عنوان سند |
| `file` | file | بله | فایل DOCX |

فقط فایل‌های با پسوند `.docx` پذیرفته می‌شوند.

#### Example

در Postman:

```text
POST http://127.0.0.1:8000/api/documents/
```

Body → `form-data`

```text
title = Django Notes
file  = django_notes.docx
```

#### Processing Flow

پس از دریافت فایل:

```text
DOCX
 ↓
Text Extraction
 ↓
Document.content
 ↓
Database Save
 ↓
Chunking
 ↓
Embedding
 ↓
Chroma Indexing
```

#### Response

```http
201 Created
```

نمونه:

```json
{
  "id": 8,
  "title": "Django Notes",
  "file": "http://127.0.0.1:8000/media/documents/django_notes.docx",
  "content": "Django is a Python web framework...",
  "created_at": "2026-09-01T10:00:00Z"
}
```

#### Errors

##### فایل با پسوند غیرمجاز

```http
400 Bad Request
```

نمونه:

```json
{
  "file": [
    "Only .docx files are supported."
  ]
}
```

##### نبودن فایل

```http
400 Bad Request
```

نمونه:

```json
{
  "file": "A DOCX file is required."
}
```

---

### 3.3 Retrieve Document

```http
GET /api/documents/<id>/
```

یک سند مشخص را بر اساس شناسه دریافت می‌کند.

#### Example

```http
GET /api/documents/8/
```

#### Response

```http
200 OK
```

نمونه:

```json
{
  "id": 8,
  "title": "Django Notes",
  "file": "http://127.0.0.1:8000/media/documents/django_notes.docx",
  "content": "Django is a Python web framework...",
  "created_at": "2026-09-01T10:00:00Z"
}
```

اگر سند وجود نداشته باشد:

```http
404 Not Found
```

---

### 3.4 Full Update Document

```http
PUT /api/documents/<id>/
```

برای به‌روزرسانی کامل resource استفاده می‌شود.

در این پروژه serializer برای ایجاد/ویرایش طوری تنظیم شده است که هنگام update، اگر فایل جدید ارسال شود، متن جدید استخراج و مجدداً index می‌شود.

در صورت ارسال فایل جدید:

```text
New DOCX
 ↓
Text Extraction
 ↓
Replace content
 ↓
Remove old chunks
 ↓
Create new chunks
 ↓
Index new chunks
```

#### Example

```text
PUT http://127.0.0.1:8000/api/documents/8/
Content-Type: multipart/form-data
```

Fields:

```text
title = Updated Django Notes
file  = updated_notes.docx
```

#### Response

```http
200 OK
```

---

### 3.5 Partial Update Document

```http
PATCH /api/documents/<id>/
```

برای تغییر بخشی از اطلاعات سند استفاده می‌شود.

مثلاً تغییر فقط عنوان:

```text
PATCH /api/documents/8/
```

```json
{
  "title": "Updated Title"
}
```

#### Response

```http
200 OK
```

اگر فایل جدید هم ارسال شود، متن استخراج و vector index دوباره ساخته می‌شود.

---

### 3.6 Delete Document

```http
DELETE /api/documents/<id>/
```

سند را از database حذف می‌کند.

قبل/همزمان با حذف، signal مربوط به Document، vectorهای متعلق به آن سند را از Chroma حذف می‌کند.

```text
Document Delete
      ↓
Chroma chunks delete
      ↓
Database record delete
```

#### Response

```http
204 No Content
```

اگر سند وجود نداشته باشد:

```http
404 Not Found
```

---

## 4. Questions API

مسیر پایه:

```text
/api/questions/
```

`Question` شامل:

| Field | Type | Description |
|---|---|---|
| `id` | integer | شناسه یکتا |
| `question` | string | متن پرسش |
| `answer` | string | پاسخ تولیدشده |
| `created_at` | datetime | زمان ثبت پرسش |

فیلدهای `id`، `answer` و `created_at` فقط توسط سرور مدیریت می‌شوند.

---

### 4.1 Ask a Question

```http
POST /api/questions/
```

برای ارسال پرسش و دریافت پاسخ مبتنی بر اسناد استفاده می‌شود.

#### Content-Type

```text
application/json
```

#### Request Body

```json
{
  "question": "Django ORM چیست؟"
}
```

#### Processing Flow

درخواست وارد Django می‌شود و سپس:

```text
Question
   ↓
Question Validation
   ↓
Save Question
   ↓
RAG Service
   ↓
Retriever
   ↓
Chroma Similarity Search
   ↓
Relevant Chunks
   ↓
Context
   ↓
Prompt
   ↓
OpenRouter LLM
   ↓
Generated Answer
   ↓
Save Answer
   ↓
Response
```

#### Response

```http
201 Created
```

نمونه:

```json
{
  "id": 15,
  "question": "Django ORM چیست؟",
  "answer": "Django ORM یک لایه انتزاعی برای کار با پایگاه داده است...",
  "created_at": "2026-09-01T10:20:00Z"
}
```

#### Empty Question

اگر پرسش خالی یا فقط شامل فاصله باشد:

```http
400 Bad Request
```

نمونه:

```json
{
  "question": [
    "Question cannot be empty."
  ]
}
```

#### LLM / RAG Failure

اگر تولید پاسخ با خطا مواجه شود:

```http
503 Service Unavailable
```

نمونه:

```json
{
  "detail": "Unable to generate an answer at this time."
}
```

جزئیات خطای داخلی در server logs ثبت می‌شود و به client نمایش داده نمی‌شود.

---

### 4.2 Get Question History

```http
GET /api/questions/
```

لیست پرسش‌ها و پاسخ‌های قبلی را برمی‌گرداند.

نتایج بر اساس `created_at` به صورت نزولی مرتب می‌شوند؛ جدیدترین پرسش در ابتدا قرار می‌گیرد.

#### Response

```http
200 OK
```

نمونه:

```json
[
  {
    "id": 15,
    "question": "Django ORM چیست؟",
    "answer": "Django ORM یک لایه انتزاعی...",
    "created_at": "2026-09-01T10:20:00Z"
  },
  {
    "id": 14,
    "question": "RAG چیست؟",
    "answer": "RAG مخفف Retrieval-Augmented Generation است...",
    "created_at": "2026-09-01T10:15:00Z"
  }
]
```

---

## 5. HTTP Status Codes

### Success

| Code | Meaning |
|---|---|
| `200` | درخواست با موفقیت پردازش شد |
| `201` | resource با موفقیت ایجاد شد |
| `204` | عملیات موفق بود و body وجود ندارد |

### Client Errors

| Code | Meaning |
|---|---|
| `400` | داده ورودی نامعتبر است |
| `404` | resource موردنظر وجود ندارد |

### Server / Dependency Errors

| Code | Meaning |
|---|---|
| `503` | سامانه نتوانسته پاسخ LLM را تولید کند |

---

## 6. Content Types

### JSON

برای Questions API:

```http
Content-Type: application/json
```

مثال:

```json
{
  "question": "RAG چیست؟"
}
```

### Multipart Form Data

برای Document upload/update:

```http
Content-Type: multipart/form-data
```

مثال:

```text
title = RAG Notes
file  = rag_notes.docx
```

---

## 7. Complete Endpoint Reference

### Documents

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/documents/` | دریافت لیست اسناد |
| `POST` | `/api/documents/` | ایجاد سند جدید |
| `GET` | `/api/documents/<id>/` | دریافت یک سند |
| `PUT` | `/api/documents/<id>/` | ویرایش کامل سند |
| `PATCH` | `/api/documents/<id>/` | ویرایش بخشی از سند |
| `DELETE` | `/api/documents/<id>/` | حذف سند |

### Questions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/questions/` | دریافت تاریخچه پرسش‌ها |
| `POST` | `/api/questions/` | ارسال پرسش و تولید پاسخ |

---

## 8. Example End-to-End Flow

### Step 1 — Upload Document

```http
POST /api/documents/
```

```text
multipart/form-data

title = RAG Notes
file  = rag_notes.docx
```

### Step 2 — Document Indexing

```text
DOCX
 ↓
Extract Text
 ↓
Chunking
 ↓
Embedding
 ↓
Chroma
```

### Step 3 — Ask Question

```http
POST /api/questions/
```

```json
{
  "question": "RAG چیست؟"
}
```

### Step 4 — Retrieval

```text
Question
 ↓
Embedding
 ↓
Chroma Search
 ↓
Relevant Chunks
```

### Step 5 — Generation

```text
Relevant Chunks
 ↓
Context
 +
Question
 ↓
Prompt
 ↓
LLM
 ↓
Answer
```

### Step 6 — History

پرسش و پاسخ در database ذخیره می‌شوند و بعداً از طریق:

```http
GET /api/questions/
```

قابل مشاهده هستند.

---

## 9. Authentication

در نسخه فعلی endpointهای API احراز هویت کاربر ندارند و authentication اختصاصی برای API تعریف نشده است.

رابط Django Admin به سیستم authentication خود Django وابسته است.

---

## 10. File Upload Restrictions

Document API فقط فایل‌های:

```text
.docx
```

را قبول می‌کند.

فایل‌های با پسوندهای دیگر با `400 Bad Request` رد می‌شوند.

متن فایل در زمان ایجاد/به‌روزرسانی استخراج و در فیلد `content` ذخیره می‌شود.

---

## 11. Related Management Commands

اگرچه این دستورات endpoint HTTP نیستند، برای مدیریت داده‌های API/RAG مهم هستند.

### Re-index All Documents

```bash
python manage.py reindex_documents
```

تمام Documentهای موجود در database را مجدداً در Chroma index می‌کند.

### Create Sample Data

```bash
python manage.py seed_sample_data
```

داده‌های نمونه را ایجاد و index می‌کند.

---

## 12. Testing the API

برای تست تعاملی می‌توان از:

- Swagger UI
- Postman
- curl

استفاده کرد.

اجرای تست‌های خودکار:

```bash
python manage.py test
```

در تست‌های automated، فراخوانی واقعی LLM mock می‌شود تا test suite به OpenRouter و rate limitهای provider وابسته نباشد.

---

## 13. Swagger Quick Test

پس از اجرای پروژه:

```text
http://127.0.0.1:8000/api/docs/
```

را باز کنید.

ابتدا:

```text
GET /api/documents/
```

را اجرا کنید.

سپس یک فایل DOCX با:

```text
POST /api/documents/
```

ایجاد کنید.

در نهایت:

```text
POST /api/questions/
```

را با یک سؤال مرتبط با سند اجرا کنید و پاسخ RAG را مشاهده کنید.

---

## 14. Notes

- API اصلی بر مبنای REST طراحی شده است.
- Document upload با `multipart/form-data` انجام می‌شود.
- Question requests با JSON انجام می‌شوند.
- متن کامل سند در SQLite نگهداری می‌شود.
- embeddingها و داده‌های retrieval در Chroma نگهداری می‌شوند.
- LangChain مسئول orchestration جریان RAG و اتصال Retriever، Prompt و LLM است.
- پاسخ نهایی از context بازیابی‌شده از اسناد تولید می‌شود.
- vectorهای یک Document هنگام حذف آن Document از Chroma حذف می‌شوند.
- در صورت تغییر فایل Document، index مربوط به آن Document مجدداً ساخته می‌شود.
