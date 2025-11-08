from app import app , mail
from flask_mail import Message
from flask import render_template , request

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.post('/confrim_contact')
def contact_confirm():
    form = request.form
    name = form.get('name')
    email = form.get('email')
    mess = form.get('mess')
    phone = form.get('phone')
    msg = Message('contact' , recipients=['vidlovergt123@gmail.com'])
    msg.body = "This is a plain text email sent from Flask."
    message = render_template('msg.html',
                              email=email,
                              name=name,
                              phone=phone,
                              mess=mess)
    msg.html = message
    try:
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        # You may want to handle this error more gracefully for the user
    return render_template('success.html')