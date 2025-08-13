# Resume Classifier AI

AI-powered tool to extract and classify resumes into job roles.

---

## 🧠 AI-Based Resume Classifier and Job Role Matcher

This project is part of my internship at **Bitzify**, focused on developing an AI-powered tool that analyzes resumes, extracts relevant information using NLP, and classifies them into the most suitable job roles.

Now enhanced with:
- **Skill Extraction Classifier** — Detects and lists key skills from resumes.
- **Education Classifier** — Extracts educational qualifications and levels.
- **Experience Classifier** — Extracts relevant work experience.
- **Job Role Matching** — Matches extracted skills, education, and experience to the most relevant job roles.

---

## 🚀 Features

- 📄 Upload resumes in PDF, DOCX, or TXT format.
- 🧠 Automatically extract:
  - Skills
  - Education
  - Work experience
- 🎯 Match candidates to job roles using classification logic.
- 🔍 Extract contact details: Name, Email, Phone.
- 🌐 Simple, responsive web interface.
- ⚡ Fast backend response (< 2 seconds).
- 👨‍💼 Admin panel for user management (add/edit/delete/block users).
- 📥 Secure file handling with dynamic resume analysis.

---

## 🧠 Technologies Used

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python (Flask or FastAPI)
- **Machine Learning:** Scikit-learn
- **NLP:** spaCy, NLTK
- **Resume Parsing:** PyMuPDF, pdfminer.six, python-docx

---

## 📌 Project Workflow

1. **User Uploads Resume** → PDF/DOCX/TXT.
2. **NLP Processing** → Extracts text, contact info, skills, education, and experience.
3. **Classification Models**:
   - Skill classifier matches keywords against a pre-trained skill database.
   - Education classifier detects degree and field of study.
   - Experience classifier identifies job titles and years of experience.
4. **Job Role Matching** → Combines extracted data to recommend suitable job roles.
5. **Results Displayed** in the web interface.

---

## 📚 Training the Classifiers

This repository includes **training scripts** to demonstrate the model-building process.

⚠️ **Note:**  
Real datasets and production-trained models are not included for privacy.  
A small synthetic dataset is provided for demonstration purposes.

### 📂 Dataset Structure

To recreate the training data, structure your CSVs as follows:

1. **Skills CSV (`skills.csv`)**

| timestamp           | skill   | job_role          |
|-------------------|--------|-----------------|
| 2025-08-13 10:00  | Python | Software Engineer |
| 2025-08-13 10:05  | SQL    | Data Analyst      |

- **Columns:**  
  - `timestamp`: When the skill data was recorded.  
  - `skill`: The skill keyword or phrase.  
  - `job_role`: The job role associated with the skill.

2. **Education CSV (`education.csv`)**

| timestamp           | education                  | job_role          |
|-------------------|----------------------------|-----------------|
| 2025-08-13 10:00  | BSc Computer Engineering  | Software Engineer |
| 2025-08-13 10:05  | MSc Data Science          | Data Analyst      |

- **Columns:**  
  - `timestamp`: When the education data was recorded.  
  - `education`: Degree or certification name.  
  - `job_role`: The job role associated with this education.

3. **Experience CSV (`experience.csv`)**

| timestamp           | experience           | job_role          |
|-------------------|--------------------|-----------------|
| 2025-08-13 10:00  | 3 years Software Engineer | Software Engineer |
| 2025-08-13 10:05  | 2 years Data Analyst      | Data Analyst      |

- **Columns:**  
  - `timestamp`: When the experience data was recorded.  
  - `experience`: Job experience description or duration.  
  - `job_role`: The job role associated with the experience.

> All CSVs should have headers and be UTF-8 encoded. These files will be read by the training scripts to build the respective classifiers.

---

### 🛠️ 1. Train the **Skill Classifier**
```bash
python train_skill_classifier.py
### 🛠️ 2. Train the **Education Classifier**
```bash
python train_education_classifier.py
### 🛠️ 3. Train the **Experience Classifier**
```bash
python train_education_classifier.py

## 📸 Snapshots

### 🏠 Homepage Interface
<img width="827" height="913" alt="Screenshot 2025-07-31 132311" src="https://github.com/user-attachments/assets/9c13e475-e6d5-43ba-bd1e-deca03e8de75" />
<img width="838" height="869" alt="Screenshot 2025-07-31 132331" src="https://github.com/user-attachments/assets/0d8e05dd-5e4a-4d9c-87e1-6ec9d6c3ace9" />


### 🔐 Login Page
<img width="804" height="822" alt="Screenshot 2025-07-31 131835" src="https://github.com/user-attachments/assets/5ed88aa1-45cf-4246-9325-b3d0d1730f46" />


### 📝 Register Page
<img width="817" height="877" alt="Screenshot 2025-07-31 134410" src="https://github.com/user-attachments/assets/dd16a15d-3312-44d7-bfca-a6d829b8b269" />


### 📊 User Dashboard
<img width="827" height="899" alt="Screenshot 2025-07-31 131931" src="https://github.com/user-attachments/assets/b78f7182-c9a4-4216-83ba-4b8e793d4cdc" />


### 📤 Resume Upload Page
<img width="815" height="594" alt="Screenshot 2025-07-31 131944" src="https://github.com/user-attachments/assets/8733754d-1d6d-4071-84e8-deb1977d8a76" />


### 📄 Uploaded Resumes List
<img width="814" height="718" alt="Screenshot 2025-07-31 132008" src="https://github.com/user-attachments/assets/2bc1b547-5e41-4f72-b409-8e554993e8bf" />


### 🔎 Extracted Resume Text
<img width="544" height="915" alt="Screenshot 2025-07-31 132047" src="https://github.com/user-attachments/assets/32261954-c18d-413d-9f8a-a7d34a8a2d17" />


### 📧 Extracted Contact Info
<img width="766" height="569" alt="Screenshot 2025-07-31 132107" src="https://github.com/user-attachments/assets/56d08d46-de97-412d-bb28-c8bd54244869" />


### 🧠 Resume Skill Analysis
<img width="773" height="635" alt="Screenshot 2025-07-31 132116" src="https://github.com/user-attachments/assets/7adcfb96-24a1-4cb3-8c8d-ef9f4f9b135a" />

### 🎓 Education & Experience Sections
<img width="773" height="804" alt="Screenshot 2025-07-31 132254" src="https://github.com/user-attachments/assets/c8df96af-038b-4de1-a0b8-ef4315766cbe" />


### ⚙️ Admin Panel - User Management
<img width="839" height="869" alt="Screenshot 2025-07-31 134031" src="https://github.com/user-attachments/assets/681e9b29-a2e9-4687-9816-cf02df82844c" />


### 🗂️ Edit User Interface
<img width="832" height="909" alt="Screenshot 2025-07-31 134926" src="https://github.com/user-attachments/assets/dd7f08a9-eefb-4f27-b123-dc5829d5218a" />

### ➕ Add User Interface
<img width="817" height="896" alt="Screenshot 2025-07-31 134945" src="https://github.com/user-attachments/assets/f2dd283f-80d8-42f7-be60-fa87e572ca5b" />

---
