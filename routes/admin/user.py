from werkzeug.utils import secure_filename
from app import app , db, render_template
from flask import request, redirect, url_for, session, flash
from models import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os


@app.get('/admin/users')
def admin_user():
    model = 'user'
    users = User.query.all()

    # 1. You need to identify the current logged-in user.
    # For example, if you store the user_id in the session:
    current_user_id = session.get('user_id')
    current_admin = User.query.get(current_user_id)

    # 2. Pass 'user' to the template so admin_layout.html can find it
    return render_template('admin/users/users.html', users=users, user=current_admin, model=model)


@app.get('/form/users/create')
def form_user_create():
    model = 'user_create    '
    status = request.args.get('status')
    return render_template('admin/users/add_user.html', model=model, status=status)

@app.get('/form/users/edit')
def form_user_edit():
    model = 'form_user_edit'
    status = request.args.get('status')
    user = None
    if status == 'edit':
        user_id = int(request.args.get('user_id'))
        user = User.query.get(user_id)

    return render_template('admin/users/edit_user.html', model=model, status=status, user=user)


@app.get('/form/users/delete')
def form_user_delete():
    model = 'user_delete'
    user_id = int(request.args.get('user_id'))
    user = User.query.get(user_id)
    return render_template('admin/users/user_delete.html', model=model, user=user)


@app.post('/users/create')
def user_create():
    form = request.form
    file = request.files.get('image')

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join('static/uploads', filename)
        file.save(upload_path)

    user = User(
        branch_id=1,
        username=form.get('username'),
        email=form.get('email'),
        phone=form.get('phone'),
        role=form.get('role'),
        password=generate_password_hash(form.get('password')),
        image=filename
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login_page'))



@app.post('/users/edit')
def user_edit():
    form = request.form
    user_id = int(form.get('user_id'))
    user = User.query.get(user_id)

    if user:
        user.username = form.get('username') or user.username
        user.email = form.get('email') or user.email
        user.phone = form.get('phone') or user.phone
        user.role = form.get('role') or user.role



        # Handle image uploads
        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)
            upload_path = os.path.join(app.root_path, 'static/uploads', filename)
            image.save(upload_path)
            user.image = filename  # only overwrite if new image

        db.session.commit()

    return redirect(url_for('admin_user'))


@app.post('/users/delete')
def user_delete():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('admin_user'))







@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        db_user = User.query.get(user_id)
        return dict(user=db_user) # This creates the 'user' variable for HTML
    return dict(user=None)