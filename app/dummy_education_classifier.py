# dummy_education_classifier.py
import os
import re
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load
import PyPDF2
from docx import Document

MODEL_PATH = "models/dummy_education_classifier.pkl"
VECTORIZER_PATH = "models/dummy_education_vectorizer.pkl"
DATASET_PATH = "data/dummy_education_samples.csv"

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
    return re.sub(r'\s+', ' ', text).strip()

def extract_education_section(text):
    lines = text.split("\n")
    edu_lines = []
    capture = False
    for line in lines:
        if re.search(r'education|qualifications|degrees', line, re.IGNORECASE):
            capture = True
            continue
        if capture and re.search(r'experience|work history', line, re.IGNORECASE):
            break
        if capture:
            edu_lines.append(line.strip())
    return " ".join(edu_lines)

def add_training_sample(education_str, degree_level):
    timestamp = datetime.now().isoformat()
    new_row = pd.DataFrame([[timestamp, education_str.lower(), degree_level.strip()]],
                           columns=['timestamp', 'education', 'degree_level'])
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

    df['education'] = df['education'].str.lower()
    df['degree_level'] = df['degree_level'].str.strip()

    X = df['education']
    y = df['degree_level']

    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)

    clf = MultinomialNB()
    clf.fit(X_vect, y)

    dump(clf, MODEL_PATH)
    dump(vectorizer, VECTORIZER_PATH)
    print("Dummy Education classifier trained and saved.")

def load_classifier():
    return load(MODEL_PATH), load(VECTORIZER_PATH)

def predict_degree_from_file(filepath):
    text = extract_text_from_file(filepath)
    edu_text = clean_resume_text(extract_education_section(text))

    clf, vectorizer = load_classifier()
    vect = vectorizer.transform([edu_text])
    return clf.predict(vect)[0]

if __name__ == "__main__":
    train_classifier()
