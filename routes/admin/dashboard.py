from flask import render_template
from app import app, db
from models import Product, Category, User  # Import your models


@app.get('/admin/dashboard')
def admin_dashboard():
    # Get counts
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()  # Assuming you have a User model

    # Get recent products (last 10)
    recent_products = Product.query.order_by(Product.id.desc()).limit(10).all()

    return render_template(
        'admin/admin_dash.html',
        total_products=total_products,
        total_categories=total_categories,
        total_users=total_users,
        recent_products=recent_products
    )