from app import app , products
from flask import render_template
@app.get('/product/<int:id>')
def product_details(id):
    product = next((p for p in products if p['id'] == id),None)
    return render_template('product_detail.html' , products=product)

