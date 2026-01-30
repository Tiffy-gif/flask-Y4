from werkzeug.utils import secure_filename
from app import app , db, render_template
from flask import request, redirect, url_for, session, flash
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.get('/login')
def login_page():
    return render_template('login.html')


@app.post('/admin/do_login')
def do_login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    user = User.query.filter_by(username=username).first()

    if not user:

        flash('Invalid username or password', 'danger')
        return redirect(url_for('login_page'))

    hash_password = user.password
    if not check_password_hash(hash_password, password):
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login_page'))
    else:
        # Store user info in session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session['user_image'] = user.image
        # session.permanent = True

        if user.role == 'admin' or user.username == 'admin':

            return redirect(url_for('admin_dashboard'))
        else:
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out successfully', 'success')
    return redirect(url_for('login_page') + '?logout=true')