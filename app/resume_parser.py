import fitz
import docx
import re
from collections import namedtuple

from app.skills_list import SKILLS


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

""" def extract_email(text):
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
            return line
    return "Name not found" """

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


def extract_skills(text):
    found = []
    text_lower = text.lower()
    for skill in SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)
    return found


def extract_education_experience(text):
    all_headers = [
        'education', 'educational background', 'academic history',
        'experience', 'work experience', 'employment history',
        'career history', 'professional experience',
        'skills', 'projects', 'certifications', 'summary', 'objective'
    ]

    lines = text.split('\n')
    lines_lower = [line.strip().lower() for line in lines]

    def normalize(s):
        return re.sub(r'[\s\.\:\-]+', '', s).lower()

    def find_all_section_indices(headers):
        normalized_headers = [normalize(h) for h in headers]
        indices = []
        for i, line in enumerate(lines_lower):
            norm_line = normalize(line)
            for norm_header in normalized_headers:
                if norm_header in norm_line:
                    indices.append(i)
                    break
        return sorted(indices)

    def extract_sections_combined(start_indices):
        if not start_indices:
            return ""
        start_indices = sorted(start_indices)
        combined_lines = []

        for idx, start_idx in enumerate(start_indices):
            # End at the next start index or next general header or end of lines
            next_start_idx = start_indices[idx + 1] if idx + 1 < len(start_indices) else None


            next_header_idx = None
            for i in range(start_idx + 1, len(lines)):
                norm_line = normalize(lines_lower[i])
                if any(normalize(h) in norm_line for h in all_headers):
                    if next_start_idx is None or i < next_start_idx:
                        next_header_idx = i
                        break

            candidates = [i for i in [next_start_idx, next_header_idx] if i is not None]
            section_end = min(candidates) if candidates else len(lines)


            section_lines = lines[start_idx:section_end]
            combined_lines.extend(section_lines)

            combined_lines.append('')

        return '\n'.join([line.strip() for line in combined_lines if line.strip()])

    edu_idx = None
    for h in ['education', 'educational background', 'academic history']:
        edu_idx = find_all_section_indices([h])
        if edu_idx:
            edu_idx = edu_idx[0]
            break

    def extract_single_section(start_idx):
        if start_idx is None:
            return ""
        next_header_idx = None
        for i in range(start_idx + 1, len(lines)):
            norm_line = normalize(lines_lower[i])
            if any(normalize(h) in norm_line for h in all_headers):
                next_header_idx = i
                break
        section_lines = lines[start_idx:] if next_header_idx is None else lines[start_idx:next_header_idx]
        return '\n'.join([l.strip() for l in section_lines if l.strip()])

    education_text = extract_single_section(edu_idx)

    exp_headers = ['experience', 'work experience', 'career history']
    exp_indices = find_all_section_indices(exp_headers)

    if not exp_indices:
        job_keywords = ['engineer', 'developer', 'intern', 'manager', 'analyst', 'scrum master']
        for i, line in enumerate(lines_lower):
            if any(job in line for job in job_keywords):
                exp_indices = [i]
                break

    experience_text = extract_sections_combined(exp_indices)

    return education_text.strip(), experience_text.strip()

