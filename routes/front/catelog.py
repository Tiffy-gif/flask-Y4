from app import app, db
from flask import render_template
from models import Product

@app.get('/catelog')
def catelog():
    products = Product.query.all()
    return render_template('catolog.html', products=products)
