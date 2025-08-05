import pandas as pd
from app.skills_list import SKILLS

def match_skills(text, skills_list):
    matched = []
    text_lower = text.lower()
    for skill in skills_list:
        if skill.lower() in text_lower:
            matched.append(skill)
    return matched

def classify_job_role(matched_skills, df):
    best_match = None
    max_overlap = 0

    for index, row in df.iterrows():
        sample_skills = [s.strip().lower() for s in row['skills'].split(',')]
        overlap = len(set(s.lower() for s in matched_skills) & set(sample_skills))
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = row['job_role']

    return best_match
