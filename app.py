from flask import Flask, render_template , request , session , json , jsonify
from flaskext.mysql import MySQL

from product import products
from flask_mail import Mail , Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# mail
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidlovergt123@gmail.com'
app.config['MAIL_PASSWORD'] = 'hegy zyrn bbvu fphn'  # Use App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'vidlovergt123@gmail.com'

mail = Mail(app)


# MySql
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app@**Aa12345localhost/app"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Optional, to suppress a warning
import urllib.parse

# Your actual password
password = "**Aa12345" 

# URL-encode the password
encoded_password = urllib.parse.quote_plus(password)

# Construct the URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://app:{encoded_password}@localhost/app"
DB_CONFIG= {
    'host': 'localhost',
    'user': 'app',
    'password': '**Aa12345',
    'database': 'app',
}

db = SQLAlchemy(app)
migrate = Migrate(app, db)
import models
import routes

db = SQLAlchemy(app)
migrate = Migrate(app, db)
import models
import routes




if __name__ == '__main__':
    app.run()
