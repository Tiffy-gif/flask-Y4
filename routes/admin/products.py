from werkzeug.utils import secure_filename
from flask import request, render_template, redirect, url_for
from app import app, db
from models import Product, Category
import os

@app.get('/admin/products')
def admin_products():
    model = 'product'
    products = Product.query.all()  # optional: pass products to template
    return render_template('admin/products/products.html', model=model, products=products)


@app.get('/form/products/add')
def form_product_add():
    model = 'product_add'
    status = request.args.get('status')
    categories = Category.query.all()  # fetch categories from DB
    return render_template(
        'admin/products/product_add.html',
        model=model,
        categories=categories, status=status
    )

@app.get('/form/products/edit')
def form_product_edit():
    model = 'form_product_edit'
    product_id = request.args.get('product_id')
    product = None

    if product_id:
        product = Product.query.get(product_id)

        # assert False, product

    return render_template('admin/products/product_edit.html', model=model, status='edit', product=product)


@app.get('/form/products/delete')
def form_product_delete():
    model = 'delete'
    product_id = int(request.args.get('product_id'))
    product = Product.query.get(product_id)

    return render_template('admin/products/product_delete.html', model=model, product=product)



@app.post('/products/create')
def product_create():
    form = request.form
    file = request.files.get('image')

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join('static/product_upload', filename)
        file.save(upload_path)

    product = Product(
        name=form.get('name'),
        price=float(form.get('price')),
        description=form.get('description'),
        category_id=int(form.get('category_id')),
        image=filename

    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for('admin_products'))



@app.post('/products/edit')
def product_edit():
    form = request.form
    product_id = int(form.get('product_id'))
    product = Product.query.get(product_id)

    if product:
        product.name = form.get('name') or product.name
        product.price = form.get('price') or product.price
        product.description = form.get('description') or product.description
        # product.category_id = form.get('category') or product.category_id


        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)
            upload_path = os.path.join(app.root_path, 'static/product_upload', filename)
            image.save(upload_path)
            product.image = filename  # only overwrite if new image

        db.session.commit()

    return redirect(url_for('admin_products'))


@app.post('/products/delete')
def product_delete():
    product_id = request.form.get('product_id')
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('admin_products'))


