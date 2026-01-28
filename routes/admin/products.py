from app import app
from flask import render_template
from werkzeug.utils import secure_filename

@app.get('/products')
def admin_products():
    model = 'products'
    return render_template('admin/products.html', model=model)