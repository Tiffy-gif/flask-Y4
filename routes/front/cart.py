from app import app
from flask import render_template
# from product import products
from models.product import Product
@app.get('/cart')
def cart():
    products = Product.query.all()
    return render_template('cart.html', products=products)
