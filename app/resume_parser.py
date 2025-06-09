
import PyPDF2
import io

def extract_text_from_pdf_bytes(pdf_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()
