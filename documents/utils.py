from docx import Document as DocxDocument


def extract_text_from_docx(file):
    document = DocxDocument(file)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)