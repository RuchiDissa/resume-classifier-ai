import os

from flask import Blueprint, render_template, session, url_for, flash, current_app
from werkzeug.utils import redirect, secure_filename
from flask import request

from app import db
from app.auth import auth
from app.models import User
from app.resume_parser import extract_resume_text, extract_basic_info, extract_skills

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

@routes.route('/uploads/edit/<filename>', methods=['GET', 'POST'])
def edit_resume(filename):
    flash("Edit functionality coming soon!", "info")
    return redirect(url_for('routes.upload_resume'))

@routes.route('/admin')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only", "danger")
        return redirect(url_for('routes.home'))

    users = User.query.all()
    return render_template('admin.html', users=users)

@routes.route('/admin/add', methods=['GET', 'POST'])
def add_user():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('routes.home'))

    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        from werkzeug.security import generate_password_hash
        hashed_pw = generate_password_hash(password, method='sha256')

        new_user = User(username=username, name=name, email=email, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully", "success")
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('add_user.html')

@routes.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('routes.home'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']
        db.session.commit()
        flash("User updated successfully", "success")
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('edit_user.html', user=user)

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

@routes.route('/clear_extracted_text')
def clear_extracted_text():
    session.pop('extracted_text', None)
    flash("Extracted text cleared", "info")
    return redirect(url_for('routes.upload_resume'))
