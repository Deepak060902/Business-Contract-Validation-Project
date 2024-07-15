from pdfminer.high_level import extract_text
from io import BytesIO

def parse_pdf(file_content: bytes) -> str:
    text = extract_text(BytesIO(file_content))
    return text
    