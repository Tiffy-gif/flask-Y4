from werkzeug.utils import secure_filename
from app import app , db, render_template
from flask import request, redirect, url_for, session, flash
from models import Category
import os

@app.get('/admin/category')
def admin_category():
    model = 'category'
    category = Category.query.all()
    return render_template('admin/categories/category.html', model=model, category=category)



@app.get('/form/category/add')
def form_category_add():
    model = 'category_new'
    status = request.args.get('status')
    return render_template('admin/categories/add-category.html', model=model, status=status)


@app.get('/form/category/edit')
def form_category_edit():
    model = 'form_category_edit'
    category_id = request.args.get('category_id')
    category = None

    if category_id:
        category = Category.query.get(category_id)

        # assert False, category

    return render_template('admin/categories/category_edit.html', model=model, status='edit', category=category)


@app.get('/form/category/delete')
def form_category_delete():
    model = 'category_delete'
    category_id = request.form.get('category_id')
    category = Category.query.get(category_id)
    return render_template('admin/categories/category_delete.html', model=model, category=category)



@app.post('/category/create')
def category_create():
    form = request.form
    file = request.files.get('image')

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join('static/category_upload', filename)
        file.save(upload_path)

    category = Category(
        name=form.get('name'),

    )

    db.session.add(category)
    db.session.commit()

    return redirect(url_for('admin_category'))



@app.post('/category/edit')
def category_edit():
    category_id = request.form.get('category_id')

    if not category_id:
        flash('Invalid category', 'error')
        return redirect(url_for('admin_category'))

    category = Category.query.get_or_404(category_id)
    category.name = request.form.get('name')
    db.session.commit()

    flash('Category updated successfully', 'success')
    return redirect(url_for('admin_category'))


