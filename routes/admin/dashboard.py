from flask import render_template, session # Import session
from app import app, db
from models import Product, Category, User

@app.get('/admin/dashboard')
def admin_dashboard():
    # 1. Fetch the logged-in user to prevent the UndefinedError
    user_id = session.get('user_id')
    current_user = User.query.get(user_id)

    # 2. Get counts
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()

    # 3. Get recent products
    recent_products = Product.query.order_by(Product.id.desc()).limit(10).all()

    return render_template(
        'admin/admin_dash.html',
        user=current_user,           # This fixes the 'user is undefined' error
        total_products=total_products,
        total_categories=total_categories,
        total_users=total_users,
        recent_products=recent_products,
        model='dashboard'            # Helps highlight the active link in sidebar
    )