from app import app
from flask import render_template
from product import products

@app.get('/cart')
def cart():
    product = products
    return render_template('cart.html' ,products=product)