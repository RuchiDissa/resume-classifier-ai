from flask import Blueprint, render_template, session, url_for, flash
from werkzeug.utils import redirect
from flask import request

from app import db
from app.auth import auth
from app.models import User

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/about')
def about():
    return render_template('aboutus.html')

@routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
    user.blocked = not user.blocked  # Toggle block status
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

@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('routes.home'))
