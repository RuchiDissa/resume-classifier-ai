# dummy_experience_classifier.py
import os
import re
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load
import PyPDF2
from docx import Document

MODEL_PATH = "models/dummy_experience_classifier.pkl"
VECTORIZER_PATH = "models/dummy_experience_vectorizer.pkl"
DATASET_PATH = "data/dummy_experience_samples.csv"

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif ext == ".docx":
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def clean_resume_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_experience_section(text):
    lines = text.split("\n")
    exp_lines = []
    capture = False
    for line in lines:
        if re.search(r'experience|work history|employment', line, re.IGNORECASE):
            capture = True
            continue
        if capture and re.search(r'education', line, re.IGNORECASE):
            break
        if capture:
            exp_lines.append(line.strip())
    return " ".join(exp_lines)

def add_training_sample(experience_str, job_role):
    timestamp = datetime.now().isoformat()
    new_row = pd.DataFrame([[timestamp, experience_str.lower(), job_role.strip()]],
                           columns=['timestamp', 'experience', 'job_role'])
    if not os.path.isfile(DATASET_PATH):
        new_row.to_csv(DATASET_PATH, index=False)
    else:
        new_row.to_csv(DATASET_PATH, mode='a', header=False, index=False)

def train_classifier():
    if not os.path.isfile(DATASET_PATH):
        print("No training data found.")
        return

    df = pd.read_csv(DATASET_PATH)
    if df.empty:
        print("Training file is empty.")
        return

    df['experience'] = df['experience'].str.lower()
    df['job_role'] = df['job_role'].str.strip()

    X = df['experience']
    y = df['job_role']

    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)

    clf = MultinomialNB()
    clf.fit(X_vect, y)

    dump(clf, MODEL_PATH)
    dump(vectorizer, VECTORIZER_PATH)
    print("Dummy Experience classifier trained and saved.")

def load_classifier():
    return load(MODEL_PATH), load(VECTORIZER_PATH)

def predict_job_role_from_file(filepath, top_n=3):
    text = extract_text_from_file(filepath)
    exp_text = clean_resume_text(extract_experience_section(text))

    clf, vectorizer = load_classifier()
    vect = vectorizer.transform([exp_text])
    probs = clf.predict_proba(vect)[0]
    classes = clf.classes_

    sorted_probs = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)
    return sorted_probs[:top_n]

if __name__ == "__main__":
    train_classifier()
