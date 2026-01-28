from app import app
from flask import render_template
from models.product import Product  # import the Product model

@app.get('/product/<int:id>')
def product_details(id):
    # Query the product from the database
    product = Product.query.get_or_404(id)  # returns 404 if not found

    # Pass the product object to template
    return render_template('product_detail.html', product=product)
