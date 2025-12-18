from pypdf import PdfReader

def extract_pdf(path):
    reader = PdfReader(path)
    return [p.extract_text() for p in reader.pages if p.extract_text()]
