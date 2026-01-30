from flask import request, render_template, redirect, url_for, flash
from app import app, db
from models import Product, Category, Order, OrderItem


# Function for the list of orders
@app.get('/admin/orders')
def admin_orders():
    """Display all orders"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders/orders.html', orders=orders)


# Function for the specific order - THIS NAME MUST MATCH url_for
@app.get('/admin/order-details/<int:order_id>')
def admin_order_details(order_id):
    """Display specific order details"""
    order = Order.query.get_or_404(order_id)
    # Make sure to pass 'order' to the template
    return render_template('admin/orders/order_detail.html', order=order)


# Alternative route if you're using /admin/orders/<id> URL pattern
@app.get('/admin/orders/<int:order_id>')
def admin_order_details_alt(order_id):
    """Alternative URL pattern for order details"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/orders/order_detail.html', order=order)


# Function to update order status
@app.post('/admin/orders/<int:order_id>/update-status')
def update_order_status(order_id):
    """Update the status of an order"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')

    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order_id} status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'error')

    return redirect(url_for('admin_order_detail', order_id=order_id))


# Function to delete an order
@app.post('/admin/orders/<int:order_id>/delete')
def delete_order(order_id):
    """Delete an order and all its items"""
    order = Order.query.get_or_404(order_id)

    try:
        db.session.delete(order)
        db.session.commit()
        flash(f'Order #{order_id} has been deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting order: {str(e)}', 'error')

    return redirect(url_for('admin_orders'))