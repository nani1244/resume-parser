import spacy
import re
from pdfminer.high_level import extract_text
import docx2txt

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Define regex patterns for phone numbers and email
PHONE_PATTERN = re.compile(r'\+?\d[\d -]{8,12}\d')
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_text_from_pdf(file):
    return extract_text(file)

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

def extract_phone_and_email(text):
    phones = PHONE_PATTERN.findall(text)
    emails = EMAIL_PATTERN.findall(text)
    return phones, emails

def parse_resume(resume):
    filename = resume.filename
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(resume)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(resume)
    elif filename.endswith('.txt'):
        text = extract_text_from_txt(resume)
    else:
        return {"error": "Unsupported file type"}

    # Extract phone numbers and emails
    phones, emails = extract_phone_and_email(text)

    # Process text with spaCy
    doc = nlp(text)
    details = {
        "Name": "",
        "Phone Numbers": phones,
        "Emails": emails,
        "Experience": "",
        "Technical Skills": "",
        "Education": ""
    }

    # Extract names and experiences from entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            details["Name"] = ent.text
        elif ent.label_ in ["ORG", "WORK_OF_ART"]:
            details["Experience"] = details.get("Experience", "") + f"{ent.text}, "

    # Extract technical skills and education using pattern matching or custom rules
    # This is a simple placeholder; you might need to use more advanced techniques here
    text = text.lower()
    skills_keywords = ['python', 'java', 'c++', 'sql', 'html', 'css', 'javascript']  # Add more skills as needed
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']  # Add more education terms

    details["Technical Skills"] = ", ".join([skill for skill in skills_keywords if skill in text])
    details["Education"] = ", ".join([edu for edu in education_keywords if edu in text])

    return details
