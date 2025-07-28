from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if user.blocked:
                flash("Your account has been blocked. Please contact admin.", "danger")
                return redirect(url_for('auth.login'))

            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                flash('Logged in successfully', 'success')
                return redirect(url_for('routes.dashboard'))

        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_Password']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password, method='sha256')

        new_user = User(
            username=username,
            name=name,
            email=email,
            password=hashed_pw,
            role='none',
            blocked=False
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registered successfully", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('auth.login'))
