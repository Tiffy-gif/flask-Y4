import json
from datetime import datetime
from fun_tele import sendMessage
from app import app, db, mail
from flask_mail import Message
from flask import render_template, request, redirect, url_for, session, flash
from tabulate import tabulate

from models import Order, OrderItem, Product


@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout')
        return redirect(url_for('login_page'))
    return render_template('checkout.html')


@app.post('/confirm')
def confirm():
    # Get data from form input in checkout.html
    form = request.form
    name = form.get('name')
    email = form.get('email')
    phone = form.get('phone')
    house = form.get('house')
    street = form.get('street')
    area = form.get('area')
    cart_item_str = form.get('cart-item')
    cart_item = json.loads(cart_item_str)

    # Calculate total
    total = sum(float(item['price']) * float(item['qty']) for item in cart_item)

    # Create the Order record
    new_order = Order(
        user_id=None,  # Set to current user's ID if authentication is implemented
        name=name,
        phone=phone,
        email=email,
        house=house,
        street=street,
        area=area,
        total_amount=total,
        status='pending',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add order to session
    db.session.add(new_order)
    db.session.flush()  # This assigns an ID to new_order without committing

    # Create OrderItem records
    for item in cart_item:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.get('id'),  # Assuming cart items have product IDs
            product_name=item['name'],
            product_price=float(item['price']),
            quantity=int(item['qty']),
            subtotal=float(item['price']) * int(item['qty'])
        )
        db.session.add(order_item)

    # Commit all changes to database
    db.session.commit()

    # Prepare item rows for table
    item_row = []
    for item in cart_item:
        item_row.append([
            f"{item['name'][0:15]}...",
            "$" + item["price"],
            item["qty"],
        ])

    # Create table for Telegram message
    table = tabulate(
        tabular_data=item_row,
        headers=['Product Name', 'Price', 'Qty'],
    )

    # HTML for telegram bot
    chat_id = '@notify_test_for_fun'
    html = f"<strong>Order #{new_order.id}</strong>\n"
    html += f"<strong>Customer Name: {name}</strong>\n"
    html += f"<strong>Phone: {phone}</strong>\n"
    html += f"<strong>Email: {email}</strong>\n"
    html += f"<strong>Address: No.{house}, St.{street}, Area: {area}</strong>\n"
    html += f"<strong>-----------------------------</strong>\n"
    html += f"<pre>{table}</pre>\n"
    html += f"<strong>Total: ${total:.2f}</strong>\n"

    # Send message to Telegram
    try:
        sendMessage(
            chat_id=chat_id,
            message=html,
        )
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

    # Send email to customer
    try:
        msg = Message('Invoice From SU4.13 Shop', recipients=[email])
        msg.body = 'Thank you for your order! Please find your invoice attached.'
        message = render_template('invoice.html',
                                  cart_item=cart_item,
                                  customer_name=name,
                                  email=email,
                                  house=house,
                                  area=area,
                                  street=street,
                                  total=total,
                                  order_id=new_order.id)
        msg.html = message
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

    return render_template('confirm_order.html', order_id=new_order.id, total=total)