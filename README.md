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

---

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

## 📸 Snapshots

### Homepage
![Homepage](https://raw.githubusercontent.com/<username>/<repo>/main/assets/4c7ad4e8-963c-4685-8c4d-43c63fae5a90)

### Login
![Login](https://raw.githubusercontent.com/<username>/<repo>/main/assets/d8c7820f-8e41-480c-b8fb-65d73427a71a)

### Register
![Register](https://raw.githubusercontent.com/<username>/<repo>/main/assets/b182201e-2e61-405a-8883-17f6331f956f)

### Dashboard
![Dashboard](https://raw.githubusercontent.com/<username>/<repo>/main/assets/6b6e0dec-c728-497b-8b9c-d0f839cab1a6)

### Upload Files
![Upload Files](https://raw.githubusercontent.com/<username>/<repo>/main/assets/e21dbabe-6d9c-44f0-bbe1-81de6b5804ac)

### Extract Text from Upload
![Extract Text](https://raw.githubusercontent.com/<username>/<repo>/main/assets/39df2106-2bed-4889-8ece-67b90082aedf)

### Job Match Page
![Job Match](https://raw.githubusercontent.com/<username>/<repo>/main/assets/6fb94bee-ceae-42dc-bfd0-efcc18737d16)

### Skills Classifier Result
![Skills Classifier](https://raw.githubusercontent.com/<username>/<repo>/main/assets/36ce0970-34f1-456b-9b9d-6bbe957b8961)

### Experience Classifier Result
![Experience Classifier](https://raw.githubusercontent.com/<username>/<repo>/main/assets/af720a25-a37f-40e0-ad9d-d2a26fb830a7)

### Education Classifier Result
![Education Classifier](https://raw.githubusercontent.com/<username>/<repo>/main/assets/db147b08-a346-4607-b041-1e613a2348a9)

### Admin Dashboard
![Admin Dashboard](https://raw.githubusercontent.com/<username>/<repo>/main/assets/a1366c94-ebd3-4ae4-a5c0-9b9782555a45)

### Admin Panel
![Admin Panel](https://raw.githubusercontent.com/<username>/<repo>/main/assets/21aefc49-5c8a-4021-9f11-8564f7dbe95f)

### Update User
![Update User](https://raw.githubusercontent.com/<username>/<repo>/main/assets/84149209-619b-49c2-89d6-c07e6fc42587)

### Add User
![Add User](https://raw.githubusercontent.com/<username>/<repo>/main/assets/edff6549-6839-41a1-b839-602a47884f7a)

### Edit User
![Edit User](https://raw.githubusercontent.com/<username>/<repo>/main/assets/dedc921b-35f2-464e-8070-4d0924955369)


