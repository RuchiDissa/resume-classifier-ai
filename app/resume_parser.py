import fitz
import docx
import re
from collections import namedtuple

def extract_text_from_pdf(filepath):
    text = ""
    doc = fitz.open(filepath)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_docx(filepath):
    document = docx.Document(filepath)
    text = "\n".join([para.text for para in document.paragraphs])
    return text

def extract_text_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def extract_resume_text(filepath):
    if filepath.lower().endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif filepath.lower().endswith('.docx'):
        return extract_text_from_docx(filepath)
    elif filepath.lower().endswith('.txt'):
        return extract_text_from_txt(filepath)
    else:
        raise ValueError("Unsupported file type. Only PDF, DOCX, and TXT are supported.")

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_phone(text):
    phone_pattern = r'(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        return ''.join(phones[0])
    return None

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and line.isalpha() and len(line.split()) <= 3:
            return line  # Likely a name (simple heuristic)
    return "Name not found"


ExtractedInfo = namedtuple('ExtractedInfo', ['name', 'email', 'phone'])

def extract_basic_info(text):

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else None

    phone_match = re.search(r'(\+?\d{1,3}[\s.-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}', text)
    phone = phone_match.group(0) if phone_match else None

    lines = text.strip().split('\n')
    name = None
    for line in lines:
        if line.strip() and line.strip().replace(" ", "").isalpha():
            name = line.strip()
            break

    return ExtractedInfo(name=name, email=email, phone=phone)
