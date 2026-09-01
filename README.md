# سامانه پرسش و پاسخ از اسناد

یک سامانه مبتنی بر Django برای پرسش و پاسخ از اسناد که از معماری **Retrieval-Augmented Generation (RAG)** استفاده می‌کند.

این سامانه امکان دریافت و مدیریت فایل‌های DOCX، استخراج و ذخیره متن کامل اسناد، جست‌وجوی معنایی، بازیابی محتوای مرتبط، تولید پاسخ با استفاده از مدل زبانی، نگهداری تاریخچه پرسش و پاسخ، ارائه REST API و اجرای پروژه با Docker را فراهم می‌کند.

---

## قابلیت‌ها

* افزودن، مشاهده، ویرایش و حذف اسناد
* آپلود فایل‌های DOCX
* استخراج خودکار متن از فایل‌های DOCX
* ذخیره متن کامل اسناد
* تقسیم اسناد به chunkهای کوچک‌تر
* تولید embedding با Sentence Transformers
* جست‌وجوی معنایی با Chroma
* بازیابی Top-K بخش‌های مرتبط
* پیاده‌سازی Retrieval-Augmented Generation
* تولید پاسخ با استفاده از مدل زبانی
* ذخیره تاریخچه پرسش‌ها و پاسخ‌ها
* رابط کاربری با Django Admin
* ارائه REST API
* ارائه OpenAPI Schema
* ارائه Swagger UI
* امکان بازسازی مجدد Vector Index
* حذف خودکار vectorهای مربوط به اسناد حذف‌شده
* اجرای پروژه با Docker
* تست‌های خودکار

---

## فناوری‌های استفاده‌شده

| فناوری                | کاربرد                                  |
| --------------------- | --------------------------------------- |
| Python                | زبان برنامه‌نویسی                       |
| Django                | فریم‌ورک اصلی Backend                   |
| Django REST Framework | پیاده‌سازی REST API                     |
| python-docx           | استخراج متن و ساخت فایل‌های DOCX        |
| LangChain             | طراحی و اجرای جریان RAG و ارتباط با LLM |
| Sentence Transformers | تولید embedding                         |
| Chroma                | ذخیره‌سازی و جست‌وجوی vector            |
| OpenRouter            | ارائه API مدل زبانی                     |
| drf-spectacular       | تولید OpenAPI و Swagger                 |
| SQLite                | پایگاه داده اصلی برنامه                 |
| Docker                | اجرای containerized پروژه               |

---

# معماری سامانه

سامانه از دو جریان اصلی تشکیل شده است:

1. پردازش و index کردن اسناد
2. پاسخ‌گویی به پرسش‌ها

## جریان پردازش سند

```text
DOCX
  ↓
آپلود از API یا Django Admin
  ↓
Document Model
  ↓
استخراج متن
  ↓
ذخیره متن کامل در SQLite
  ↓
تقسیم متن به Chunk
  ↓
تولید Embedding
  ↓
ذخیره در Chroma
```

## جریان پاسخ‌گویی

```text
پرسش کاربر
  ↓
REST API
  ↓
Question Model
  ↓
Retriever
  ↓
جست‌وجوی معنایی در Chroma
  ↓
بخش‌های مرتبط سند
  ↓
ساخت Context
  ↓
Prompt
  ↓
OpenRouter LLM
  ↓
پاسخ
  ↓
ذخیره تاریخچه
  ↓
Response
```

---

# ساختار پروژه

```text
mini_document_api/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── documents/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       ├── reindex_documents.py
│   │       └── seed_sample_data.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── splitter.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   ├── llm.py
│   │   └── chain.py
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   ├── utils.py
│   ├── admin.py
│   └── tests.py
│
├── questions/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── data/
│   ├── media/
│   └── vector_db/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── manage.py
└── README.md
```

---

# تنظیم متغیرهای محیطی


فایل نمونه را کپی کنید:

    cp .env.example .env

در ویندوز (PowerShell):

    Copy-Item .env.example .env

سپس یک کلید رایگان از https://openrouter.ai/keys دریافت کرده و مقدار
`OPENROUTER_API_KEY` را در فایل `.env` قرار دهید.

محتوای `.env.example`:
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openrouter/free

VECTOR_DB_PATH=./data/vector_db
```

## توضیح متغیرها

### `DJANGO_SECRET_KEY`

کلید امنیتی Django.

### `DJANGO_DEBUG`

فعال یا غیرفعال بودن حالت Debug.

### `DJANGO_ALLOWED_HOSTS`

لیست hostهای مجاز برای اجرای Django.

### `OPENROUTER_API_KEY`

کلید API مورد استفاده برای ارتباط با OpenRouter.

### `OPENROUTER_MODEL`

مدل یا Router مورد استفاده برای تولید پاسخ.

تنظیم فعلی:

```text
openrouter/free
```

### `VECTOR_DB_PATH`

مسیر ذخیره‌سازی پایدار Vector Database.

> کلید واقعی API را داخل repository یا فایل ZIP قرار ندهید.

---

# اجرای پروژه با Docker

روش پیشنهادی اجرای پروژه استفاده از Docker است.

## ۱. ساخت Image

```bash
docker compose build
```

## ۲. اجرای پروژه

```bash
docker compose up
```

برنامه روی آدرس زیر در دسترس خواهد بود:

```text
http://127.0.0.1:8000/
```

## ۳. اجرای Migration

در یک terminal دیگر:

```bash
docker compose exec web python manage.py migrate
```

## ۴. ساخت کاربر Admin

```bash
docker compose exec web python manage.py createsuperuser
```

## ۵. ساخت داده نمونه

```bash
docker compose exec web python manage.py seed_sample_data
```

## ۶. بازسازی Vector Index

```bash
docker compose exec web python manage.py reindex_documents
```

---

# Django Admin

رابط کاربری اصلی سامانه با Django Admin پیاده‌سازی شده است.

آدرس:

```text
http://127.0.0.1:8000/admin/
```

از طریق پنل Admin می‌توان:

* اسناد را مدیریت کرد
* فایل‌های DOCX را مشاهده و مدیریت کرد
* پرسش‌ها را مشاهده کرد
* پاسخ‌های تولیدشده را مشاهده کرد
* تاریخچه پرسش و پاسخ را بررسی کرد

ایجاد یا به‌روزرسانی سند باعث index شدن آن در Vector Store می‌شود.

همچنین با حذف سند، vectorهای مرتبط با آن از Chroma حذف می‌شوند.

---

# REST API

## API اسناد

### دریافت لیست اسناد

```http
GET /api/documents/
```

### ایجاد سند

```http
POST /api/documents/
```

فرمت درخواست:

```text
multipart/form-data
```

فیلدها:

```text
title
file
```

مثال:

```text
title = Django Notes
file = django_notes.docx
```

فقط فایل‌های `.docx` پذیرفته می‌شوند.

### دریافت یک سند

```http
GET /api/documents/<id>/
```

### ویرایش کامل

```http
PUT /api/documents/<id>/
```

### ویرایش بخشی

```http
PATCH /api/documents/<id>/
```

### حذف سند

```http
DELETE /api/documents/<id>/
```

---

# API پرسش‌ها

## ارسال پرسش

```http
POST /api/questions/
```

نمونه:

```json
{
  "question": "Django ORM چیست؟"
}
```

سیستم مراحل زیر را انجام می‌دهد:

1. تبدیل پرسش به embedding
2. جست‌وجوی vectorهای مرتبط
3. بازیابی chunkهای مرتبط
4. ساخت context
5. ساخت prompt
6. ارسال درخواست به مدل زبانی
7. دریافت پاسخ
8. ذخیره پاسخ در تاریخچه
9. بازگرداندن نتیجه به کاربر

نمونه پاسخ:

```json
{
  "id": 1,
  "question": "Django ORM چیست؟",
  "answer": "Django ORM ...",
  "created_at": "2026-09-01T10:00:00Z"
}
```

## دریافت تاریخچه پرسش‌ها

```http
GET /api/questions/
```

این endpoint پرسش‌ها و پاسخ‌های قبلی را برمی‌گرداند.

---

# مستندات API

## OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

## Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

Swagger UI امکان مشاهده و تست interactive تمام endpointهای API را فراهم می‌کند.

---

# Pipeline مربوط به RAG

RAG سامانه از دو بخش اصلی تشکیل شده است.

## Indexing

هنگام ایجاد یا به‌روزرسانی یک سند:

```text
Document
   ↓
استخراج متن
   ↓
Chunking
   ↓
تولید Embedding
   ↓
ذخیره در Chroma
```

برای هر chunk اطلاعاتی مانند موارد زیر ذخیره می‌شود:

```json
{
  "document_id": 7,
  "title": "Example Document",
  "chunk_index": 3
}
```

این metadata امکان تشخیص منبع هر chunk را فراهم می‌کند.

---

# Retrieval

هنگام دریافت پرسش:

```text
Question
   ↓
Question Embedding
   ↓
Chroma Similarity Search
   ↓
Top-K Relevant Chunks
```

chunkهای بازیابی‌شده به عنوان Context در اختیار مدل زبانی قرار می‌گیرند.

---

# Generation

```text
Context + Question
        ↓
LangChain Prompt
        ↓
OpenRouter
        ↓
LLM
        ↓
Answer
```

Prompt به مدل دستور می‌دهد که پاسخ را بر اساس context بازیابی‌شده تولید کند و در صورتی که اطلاعات لازم در اسناد وجود نداشته باشد، آن را اعلام کند.

---

# Vector Store

در این پروژه Chroma به عنوان Vector Store استفاده می‌شود.

داده‌های سامانه به شکل زیر تفکیک شده‌اند:

```text
SQLite
├── اطلاعات سند
├── اطلاعات فایل
├── متن کامل سند
└── تاریخچه پرسش و پاسخ

Chroma
├── Embeddingهای chunkها
├── متن chunkها
├── شناسه chunkها
└── Metadata
```

SQLite پایگاه داده اصلی application است و Chroma برای جست‌وجوی معنایی مورد استفاده قرار می‌گیرد.

---

# مدل Embedding

برای تولید embedding از مدل زیر استفاده می‌شود:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

این مدل متن را به vector تبدیل می‌کند.

همان مدل برای:

```text
Document Chunks
```

و:

```text
User Questions
```

استفاده می‌شود تا هر دو در فضای embedding یکسان قرار بگیرند و مقایسه معنایی امکان‌پذیر باشد.

---

# بازسازی Vector Index

پروژه دارای یک Django Management Command برای بازسازی index است:

```bash
python manage.py reindex_documents
```

این command تمام اسناد موجود در database را دوباره index می‌کند.

این دستور برای موارد زیر کاربرد دارد:

* حذف شدن Vector Database
* تغییر مدل embedding
* تغییر تنظیمات chunking
* بازسازی کامل index
* بازیابی consistency بین database و vector store

---

# داده نمونه

برای ساخت اسناد نمونه:

```bash
python manage.py seed_sample_data
```

این command چند سند نمونه ایجاد و آن‌ها را در Chroma index می‌کند.

---

# تست

برای اجرای تمام تست‌های خودکار:

```bash
python manage.py test
```

تست‌ها بخش‌هایی مانند موارد زیر را پوشش می‌دهند:

* رفتار Document Model
* استخراج متن DOCX
* Document API
* اعتبارسنجی فایل
* به‌روزرسانی Document
* حذف Document
* حذف vectorهای مرتبط
* Question Model
* Question API
* اعتبارسنجی سؤال
* تاریخچه پرسش‌ها

در تست‌های API، LLM واقعی mock می‌شود تا تست‌ها به:

* اینترنت
* OpenRouter
* rate limit مدل‌ها
* در دسترس بودن provider

وابسته نباشند.

برای تست دستی RAG می‌توان از embedding model، Chroma و OpenRouter واقعی استفاده کرد.

---

# Logging و مدیریت خطا

سیستم برای رویدادهای مهم از logging استفاده می‌کند، از جمله:

```text
Document indexing
RAG execution
Successful answer generation
RAG failures
```

خطاهای مربوط به RAG و LLM در log ثبت می‌شوند، اما traceback داخلی به کاربر API نمایش داده نمی‌شود و یک پاسخ خطای کنترل‌شده برگردانده می‌شود.

---

# Persistence

داده‌های runtime پروژه در مسیر زیر ذخیره می‌شوند:

```text
data/
├── media/
└── vector_db/
```

Docker این directory را به container متصل می‌کند:

```text
Host:
./data

Container:
/app/data
```

در نتیجه با recreate شدن container، فایل‌های آپلودشده و Vector Database باقی می‌مانند.

---

# اجرای پروژه بدون Docker

برای اجرای مستقیم در محیط Python:

```bash
python -m venv venv
```

فعال‌سازی virtual environment و نصب dependencyها:

```bash
pip install -r requirements.txt
```

اجرای migration:

```bash
python manage.py migrate
```

ساخت کاربر Admin:

```bash
python manage.py createsuperuser
```

اجرای Django:

```bash
python manage.py runserver
```

---

# تصمیمات طراحی

## استفاده از Django Admin

طبق الزامات پروژه، Django Admin به عنوان رابط کاربری اصلی استفاده شده است و نیازی به frontend جداگانه نیست.

## استفاده از Chroma

Chroma برای نگهداری embeddingها و انجام similarity search استفاده شده است، در حالی که SQLite وظیفه نگهداری داده‌های اصلی application را بر عهده دارد.

## استفاده از LangChain

LangChain وظیفه اتصال اجزای اصلی RAG مانند:

```text
Retriever
+
Prompt
+
LLM
```

را بر عهده دارد.

## استفاده از Embedding محلی

Embedding اسناد به صورت محلی با Sentence Transformers تولید می‌شود و محتوای سند برای تولید embedding به سرویس خارجی ارسال نمی‌شود.

## استفاده از OpenRouter

OpenRouter به عنوان درگاه دسترسی به مدل زبانی استفاده می‌شود و امکان تغییر مدل بدون تغییر ساختار اصلی RAG را فراهم می‌کند.

---

# محدودیت‌های فعلی

این پروژه با هدف سادگی، خوانایی و قابلیت توسعه طراحی شده است و یک سامانه توزیع‌شده در مقیاس production نیست.

نسخه فعلی:

* از SQLite استفاده می‌کند.
* از Chroma محلی استفاده می‌کند.
* Django development server را داخل Docker اجرا می‌کند.
* برای تولید پاسخ به سرویس خارجی LLM وابسته است.
* عملیات indexing سند را به صورت synchronous انجام می‌دهد.

برای deployment در مقیاس بزرگ‌تر می‌توان مواردی مانند PostgreSQL، سرور WSGI/ASGI مخصوص production، سیستم پردازش background، Vector Database مستقل و تکنیک‌های پیشرفته‌تر retrieval و reranking را اضافه کرد.

---

# اجرای سریع

برای سریع‌ترین راه‌اندازی:

cp .env.example .env
    # کلید OpenRouter را در .env قرار دهید

    docker compose build
    docker compose run --rm web python manage.py migrate
    docker compose run --rm web python manage.py createsuperuser
    docker compose run --rm web python manage.py seed_sample_data
    docker compose up

سپس:

```text
Admin:
http://127.0.0.1:8000/admin/

Swagger:
http://127.0.0.1:8000/api/docs/

OpenAPI:
http://127.0.0.1:8000/api/schema/
```

پس از این مراحل، سامانه آماده دریافت اسناد و پاسخ‌گویی بر اساس محتوای آن‌ها است.
