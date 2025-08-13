# Resume Classifier AI

AI-powered tool to extract and classify resumes into job roles.

---

## 🧠 AI-Based Resume Classifier and Job Role Matcher

This project is part of my internship at **Bitzify**, focused on developing an AI-powered tool that analyzes resumes, extracts relevant information using NLP, and classifies them into the most suitable job roles.

**Key Features:**
- **Skill Extraction Classifier** — Detects and lists key skills from resumes.
- **Education Classifier** — Extracts educational qualifications and levels.
- **Experience Classifier** — Extracts relevant work experience.
- **Job Role Matching** — Matches extracted skills, education, and experience to the most relevant job roles.

---

## 🚀 Features

- 📄 Upload resumes in PDF, DOCX, or TXT format.
- 🧠 Automatic extraction of:
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

1. **User Uploads Resume** → PDF/DOCX/TXT
2. **NLP Processing** → Extracts text, contact info, skills, education, and experience
3. **Classification Models**:
   - Skill classifier matches keywords against a pre-trained skill database
   - Education classifier detects degree and field of study
   - Experience classifier identifies job titles and years of experience
4. **Job Role Matching** → Recommends suitable job roles
5. **Results Displayed** in the web interface

---

## 📚 Training the Classifiers

This repository includes **training scripts** to demonstrate the model-building process.

⚠️ **Note:**  
Real datasets and production-trained models are not included for privacy.  
A small synthetic dataset is provided for demonstration purposes.


## 📸 Project Snapshots

### Homepage
![Homepage](snapshots/homepage.jpeg)

### Login Page
![Login Page](snapshots/login.jpeg)

### Register Page
![Register Page](snapshots/register.jpeg)

### Admin Dashboard
![Admin Dashboard](snapshots/admin_dashboard.jpeg)

### Dashboard
![Dashboard](snapshots/dashborad.jpeg)

### Add User
![Add User](snapshots/add_user.jpeg)

### Edit User
![Edit User](snapshots/edit_user.jpeg)

### Update User
![Update User](snapshots/update_user.jpeg)

### Job Match Page
![Job Match Page](snapshots/job_match_page.jpeg)

### Extract Text from Upload
![Extract Text Upload File](snapshots/extract_text_upload_file.jpeg)

### Education Classifier Results
![Education Classifier Result](snapshots/education_classier_result.jpeg)

### Experience Classifier Results
![Experience Classifier Result](snapshots/experience_classifier_results.jpeg)

### Skills Classifier Results
![Skills Classifier Result](snapshots/skills_classifier_result.jpeg)

### Upload Files
![Upload Files](snapshots/uploadFiles.jpeg)

### Admin Panel
![Admin Panel](snapshots/admin_panel.jpeg)

