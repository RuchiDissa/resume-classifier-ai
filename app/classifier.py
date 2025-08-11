import os
from datetime import datetime

import PyPDF2
import joblib
from docx import Document
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load

from app.tokenizer import comma_tokenizer

MODEL_PATH = "app/models/job_classifier_model.pkl"
VECTORIZER_PATH = "app/models/skill_vectorizer.pkl"
DATASET_PATH = "app/resume_samples.csv"

SKILLS = [
    # Original + extended skills from data samples:
    "python", "flask", "sql", "html", "css", "javascript", "react", "docker",
    "aws", "azure", "linux", "machine learning", "data analysis", "accounting", "tax",
    "apis", "node.js", "mongodb", "express", "java", "postgresql", "rest apis",
    "microservices", "django", "mysql", "postgreSQL", "microservices",

    # Additional skills from the data:
    "financial analysis", "audit", "tensorflow", "pandas", "r",
    "scikit-learn", "vue.js", "html5", "css3", "responsive design",
    "servers", "networking", "cybersecurity", "windows server", "active directory",
    "powershell", "vmware", "angular", "mySQL", "jenkins", "terraform",
    "kubernetes", "monitoring", "ux research", "wireframing", "figma",
    "adobe xd", "user interface design", "prototyping", "sketch", "usability testing",
    "business analysis", "requirements gathering", "stakeholder management",
    "process mapping", "documentation", "project coordination", "photoshop",
    "illustrator", "branding", "typography", "indesign", "adobe creative suite",
    "layout", "color theory", "agile", "scrum", "project planning", "jira",
    "communication", "risk management", "budgeting", "team leadership",
    "waterfall", "mobile development", "swift", "xcode", "ui design",
    "ios", "objective-c", "core data", "uikit", "app debugging",
    "android", "kotlin", "firebase", "mobile testing", "tableau",
    "dashboard creation", "data cleaning"
]


def train_classifier():
    df = pd.read_csv(DATASET_PATH)
    df['skills'] = df['skills'].str.lower()
    df['job_role'] = df['job_role'].str.strip()

    X = df['skills']
    y = df['job_role']

    vectorizer = CountVectorizer(tokenizer=comma_tokenizer)
    X_vect = vectorizer.fit_transform(X)

    clf = MultinomialNB()
    clf.fit(X_vect, y)

    dump(clf, MODEL_PATH)
    dump(vectorizer, VECTORIZER_PATH)
    print("✅ Classifier and vectorizer trained and saved.")

def load_classifier():
    clf = load(MODEL_PATH)
    vectorizer = load(VECTORIZER_PATH)
    return clf, vectorizer

def predict_job_role(matched_skills, top_n=3):
    clf, vectorizer = load_classifier()

    if not matched_skills:
        return [], []

    skill_str = ", ".join([s.lower() for s in matched_skills])
    vect = vectorizer.transform([skill_str])

    probs = clf.predict_proba(vect)[0]
    classes = clf.classes_

    prob_tuples = list(zip(classes, probs))
    sorted_probs = sorted(prob_tuples, key=lambda x: x[1], reverse=True)
    top_roles = [(role, prob) for role, prob in sorted_probs[:top_n] if prob > 0]

    return top_roles, matched_skills

def match_skills(text, skills_list=SKILLS):
    text_lower = text.lower()
    matched = []
    for skill in skills_list:
        if skill in text_lower and skill not in matched:
            matched.append(skill)
    return matched

def extract_text_from_file(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()

        if ext == ".pdf":
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                return text

        elif ext == ".docx":
            doc = Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text

        elif ext == ".txt":
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

        else:
            print(f"Unsupported file format: {ext}")
            return ""

    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""


def add_training_sample(skills_str, job_role):
    timestamp = datetime.now().isoformat()
    new_row = pd.DataFrame([[timestamp, skills_str.lower(), job_role.strip()]], columns=['timestamp', 'skills', 'job_role'])

    if not os.path.isfile(DATASET_PATH):
        new_row.to_csv(DATASET_PATH, index=False)
    else:
        new_row.to_csv(DATASET_PATH, mode='a', header=False, index=False)

def train_classifier():
    df = pd.read_csv(DATASET_PATH)
    df['skills'] = df['skills'].str.lower()
    df['job_role'] = df['job_role'].str.strip()

    X = df['skills']
    y = df['job_role']

    vectorizer = CountVectorizer(tokenizer=comma_tokenizer)
    X_vect = vectorizer.fit_transform(X)

    clf = MultinomialNB()
    clf.fit(X_vect, y)

    dump(clf, MODEL_PATH)
    dump(vectorizer, VECTORIZER_PATH)

    print("✅ Classifier and vectorizer trained and saved.")

if __name__ == "__main__":
    train_classifier()
