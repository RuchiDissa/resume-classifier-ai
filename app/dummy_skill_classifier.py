# dummy_skill_classifier.py
import os
import re
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load
import PyPDF2
from docx import Document

MODEL_PATH = "models/dummy_skill_classifier.pkl"
VECTORIZER_PATH = "models/dummy_skill_vectorizer.pkl"
DATASET_PATH = "data/dummy_skills_samples.csv"

# Dummy list of skills — replace with real list in production
SKILL_LIST = ["python", "machine learning", "project management", "javascript"]

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

def extract_skills_from_text(text):
    text = text.lower()
    found = [skill for skill in SKILL_LIST if skill.lower() in text]
    return list(set(found))

def add_training_sample(skills_str, category):
    timestamp = datetime.now().isoformat()
    new_row = pd.DataFrame([[timestamp, skills_str.lower(), category.strip()]],
                           columns=['timestamp', 'skills', 'category'])
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

    df['skills'] = df['skills'].str.lower()
    df['category'] = df['category'].str.strip()

    X = df['skills']
    y = df['category']

    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)

    clf = MultinomialNB()
    clf.fit(X_vect, y)

    dump(clf, MODEL_PATH)
    dump(vectorizer, VECTORIZER_PATH)
    print("Dummy Skills classifier trained and saved.")

def load_classifier():
    return load(MODEL_PATH), load(VECTORIZER_PATH)

def predict_category_from_file(filepath):
    text = extract_text_from_file(filepath)
    skills = " ".join(extract_skills_from_text(text))

    clf, vectorizer = load_classifier()
    vect = vectorizer.transform([skills])
    return clf.predict(vect)[0]

if __name__ == "__main__":
    train_classifier()
