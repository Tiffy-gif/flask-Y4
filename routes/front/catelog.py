from app import app
from flask import render_template
from product import products

@app.get('/catelog')
def catelog():
    product = products
    return  render_template('catolog.html', products=product)