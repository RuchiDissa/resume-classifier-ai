import os

import pandas as pd
from flask import Blueprint, render_template, session, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect, secure_filename
from flask import request

from app import db
from app.auth import auth
from app.tokenizer import comma_tokenizer  # Import so pickle can find it
from app.classifier import predict_job_role, load_classifier, add_training_sample, train_classifier
from app.classifier import predict_job_role, match_skills, extract_text_from_file
from app.models import User
from app.resume_parser import extract_resume_text, extract_basic_info, extract_skills, extract_education_experience
from app.skills_list import SKILLS

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/about')
def about():
    return render_template('aboutus.html')

@routes.route('/contact')
def contact():
    return render_template('contacts.html')

@routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@routes.route('/create_resume')
def create_resume():
    return render_template('create_resume.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

@routes.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to upload files", "danger")
        return redirect(url_for('auth.login'))

    uploaded_files = []
    extracted_text = None

    if request.method == 'POST':
        session.pop('extracted_text', None)

        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['resume']

        if file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
            os.makedirs(user_folder, exist_ok=True)
            save_path = os.path.join(user_folder, filename)
            file.save(save_path)
            flash('Resume uploaded successfully! Click Extract to analyze.', 'success')
        else:
            flash('Invalid file type. Please upload PDF, DOCX, or TXT files.', 'danger')

    else:
        if 'extracted_text' in session:
            extracted_text = session.pop('extracted_text')

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    if os.path.exists(user_folder):
        uploaded_files = os.listdir(user_folder)

    return render_template('upload.html', uploaded_files=uploaded_files, extracted_text=extracted_text)


@routes.route('/uploads/delete/<filename>')
def delete_resume(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"{filename} deleted successfully", "success")
    else:
        flash(f"{filename} not found", "danger")

    return redirect(url_for('routes.upload_resume'))

from flask import jsonify

@routes.route('/api/resume/text/<filename>', methods=['GET'])
def get_resume_text(filename):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        text = extract_resume_text(file_path)
        return jsonify({"content": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/api/resume/save-text/<filename>', methods=['POST'])
def save_resume_text(filename):
    user_id = session.get('user_id')
    if not user_id:
        print("Unauthorized: No user_id in session")
        return jsonify({"error": "Unauthorized"}), 401

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    print(f"user_folder: {user_folder}")

    data = request.get_json()
    print(f"Received data: {data}")

    if not data or 'content' not in data:
        print("No content provided in request JSON")
        return jsonify({"error": "No content provided"}), 400

    new_text = data['content']

    # Prepare new filename with .txt extension regardless of original extension
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_edited.txt"
    new_file_path = os.path.join(user_folder, new_filename)
    print(f"Saving edited content to: {new_file_path}")

    try:

        os.makedirs(user_folder, exist_ok=True)

        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("File saved successfully")
        return jsonify({"message": "Edited file saved successfully", "new_filename": new_filename})
    except Exception as e:
        print(f"Exception while saving file: {e}")
        return jsonify({"error": str(e)}), 500

@routes.route('/admin')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only", "danger")
        return redirect(url_for('routes.home'))

    users = User.query.all()
    return render_template('admin.html', users=users)

@routes.route('/admin/add', methods=['POST'])
def add_user():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('routes.home'))

    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']
    password = request.form['password']

    # Check if email or username already exists
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        flash("Username or email already exists. Please choose another.", "warning")
        return redirect(url_for('routes.admin_dashboard'))

    hashed_pw = generate_password_hash(password, method='sha256')

    new_user = User(username=username, name=name, email=email, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit()

    flash("User added successfully", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes.route('/admin/edit-user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('routes.home'))

    user = User.query.get_or_404(user_id)

    user.username = request.form['username']
    user.name = request.form['name']
    user.email = request.form['email']
    user.role = request.form['role']
    db.session.commit()

    flash("User updated successfully", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes.route('/admin/block/<int:user_id>')
def toggle_block_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('routes.home'))

    user = User.query.get_or_404(user_id)
    user.blocked = not user.blocked
    db.session.commit()

    if user.blocked:
        flash(f"User {user.username} has been blocked", "warning")
    else:
        flash(f"User {user.username} has been unblocked", "success")

    return redirect(url_for('routes.admin_dashboard'))

@routes.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('routes.home'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully", "success")
    return redirect(url_for('routes.admin_dashboard'))

@routes.route('/resume/analyze/<filename>')
def analyze_resume(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    try:
        extracted_text = extract_resume_text(file_path)
        session['extracted_text'] = extracted_text

        info = extract_basic_info(extracted_text)
        session['extracted_info'] = info

        flash(f'Text extracted from {filename}', 'success')
    except Exception as e:
        flash(f"Error extracting text: {e}", 'danger')

    return redirect(url_for('routes.upload_resume'))

@routes.route('/resume/analyze-skills/<filename>')
def analyze_skills(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    try:
        extracted_text = extract_resume_text(file_path)
        skills = extract_skills(extracted_text)

        flash(f"Skills extracted from {filename}", "success")
        return render_template('analyze_skills.html', extracted_skills=skills, filename=filename)
    except Exception as e:
        flash(f"Error extracting skills: {e}", 'danger')
        return redirect(url_for('routes.upload_resume'))

@routes.route('/resume/skills/<filename>')
def extract_skills_route(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    try:
        extracted_text = extract_resume_text(file_path)
        skills = extract_skills(extracted_text)
        flash(f'Skills extracted from {filename}', 'success')
        return render_template('skills_result.html', skills=skills, filename=filename)
    except Exception as e:
        flash(f"Error extracting skills: {e}", 'danger')
        return redirect(url_for('routes.upload_resume'))

@routes.route('/resume/analyze-info/<filename>')
def analyze_info(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    try:
        extracted_text = extract_resume_text(file_path)
        info = extract_basic_info(extracted_text)
        flash(f'Extracted info from {filename}', 'success')
        return render_template('analyze_info.html', extracted_info=info, filename=filename)
    except Exception as e:
        flash(f"Error analyzing info: {e}", 'danger')
        return redirect(url_for('routes.upload_resume'))

@routes.route('/resume/analyze-sections/<filename>')
def analyze_sections(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    try:
        extracted_text = extract_resume_text(file_path)
        education, experience = extract_education_experience(extracted_text)

        if not education:
            education = "No education section found."
        if not experience:
            experience = "No experience section found."

        flash(f'Education and Experience extracted from {filename}', 'success')
        return render_template('analyze_sections.html', education=education, experience=experience)
    except Exception as e:
        flash(f"Error analyzing sections: {e}", 'danger')
        return redirect(url_for('routes.upload_resume'))

@routes.route('/clear_extracted_text')
def clear_extracted_text():
    session.pop('extracted_text', None)
    flash("Extracted text cleared", "info")
    return redirect(url_for('routes.upload_resume'))


@routes.route('/job-matches')
def job_matches():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    uploaded_files = []
    if os.path.exists(user_folder):
        uploaded_files = os.listdir(user_folder)
        uploaded_files.sort()

    print("Uploaded files:", uploaded_files)  # Debug print

    return render_template('job_matches.html', files=uploaded_files)

@routes.route('/resume/classify-role/<filename>')
def classify_role(filename):
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in first", "danger")
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    file_path = os.path.join(user_folder, filename)

    resume_text = extract_text_from_file(file_path)

    extracted_info = extract_basic_info(resume_text)
    education_text, experience_text = extract_education_experience(resume_text)

    from app.skills_list import SKILLS
    matched_skills = match_skills(resume_text, SKILLS)

    top_roles, matched_skills = predict_job_role(matched_skills)

    return render_template(
        "job_match_result.html",
        filename=filename,
        extracted_info=extracted_info,
        education=education_text,
        experience=experience_text,
        top_roles=top_roles,
        matched_skills=matched_skills
    )


import csv
from flask import request, redirect, url_for, flash

@routes.route('/admin/add-job-role', methods=['POST'])
def add_job_role():
    job_role = request.form.get('job_role').strip()
    skills = request.form.get('skills').strip()

    if not job_role or not skills:
        flash('Please provide both job role and skills.', 'danger')
        return redirect(url_for('routes.admin_dashboard'))


    csv_file = 'path/to/resume_samples.csv'  # Adjust path accordingly
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)


            import datetime
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, skills, job_role])
    except Exception as e:
        flash(f'Error saving job role: {e}', 'danger')
        return redirect(url_for('routes.admin_dashboard'))


    try:
        train_classifier()  # retrain your model here
    except Exception as e:
        flash(f'Job role added but retraining failed: {e}', 'warning')
        return redirect(url_for('routes.admin_dashboard'))

    flash('Job role added and classifier retrained successfully.', 'success')
    return redirect(url_for('routes.admin_dashboard'))

from flask import request

@routes.route('/admin/add-training-sample', methods=['POST'])
def add_training_sample_route():
    skills = request.form.get('skills')
    job_role = request.form.get('job_role')

    if skills and job_role:
        add_training_sample(skills, job_role)
        train_classifier()
        flash("Training sample added and classifier updated.", "success")
    else:
        flash("Please fill in all fields.", "danger")

    return redirect(url_for('routes.admin_dashboard'))
