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

<div align="center">

### Homepage
<img src="https://github.com/user-attachments/assets/4c7ad4e8-963c-4685-8c4d-43c63fae5a90" width="300px" />

### Login
<img src="https://github.com/user-attachments/assets/d8c7820f-8e41-480c-b8fb-65d73427a71a" width="300px" />

### Register
<img src="https://github.com/user-attachments/assets/b182201e-2e61-405a-8883-17f6331f956f" width="300px" />

### Dashboard
<img src="https://github.com/user-attachments/assets/6b6e0dec-c728-497b-8b9c-d0f839cab1a6" width="300px" />

### Upload Files
<img src="https://github.com/user-attachments/assets/e21dbabe-6d9c-44f0-bbe1-81de6b5804ac" width="300px" />

### Extract Text from Upload
<img src="https://github.com/user-attachments/assets/39df2106-2bed-4889-8ece-67b90082aedf" width="300px" />

### Job Match Page
<img src="https://github.com/user-attachments/assets/6fb94bee-ceae-42dc-bfd0-efcc18737d16" width="300px" />

### Skills Classifier Result
<img src="https://github.com/user-attachments/assets/36ce0970-34f1-456b-9b9d-6bbe957b8961" width="300px" />

### Experience Classifier Result
<img src="https://github.com/user-attachments/assets/af720a25-a37f-40e0-ad9e-d2a26fb830a7" width="300px" />

### Education Classifier Result
<img src="https://github.com/user-attachments/assets/db147b08-a346-4607-b041-1e613a2348a9" width="300px" />

### Admin Dashboard
<img src="https://github.com/user-attachments/assets/a1366c94-ebd3-4ae4-a5c0-9b9782555a45" width="300px" />

### Admin Panel
<img src="https://github.com/user-attachments/assets/21aefc49-5c8a-4021-9f11-8564f7dbe95f" width="300px" />

### Update User
<img src="https://github.com/user-attachments/assets/84149209-619b-49c2-89d6-c07e6fc42587" width="300px" />

### Add User
<img src="https://github.com/user-attachments/assets/edff6549-6839-41a1-b839-602a47884f7a" width="300px" />

### Edit User
<img src="https://github.com/user-attachments/assets/dedc921b-35f2-464e-8070-4d0924955369" width="300px" />

</div>

