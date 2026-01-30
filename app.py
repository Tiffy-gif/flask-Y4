from flask import Flask, render_template , request  , json , jsonify
from flask_mail import Mail , Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import urllib.parse
from datetime import timedelta
from flask import request, jsonify, render_template, flash, redirect, url_for
from sqlalchemy import text, select
from flask_jwt_extended import create_access_token, get_jwt, set_access_cookies, create_refresh_token, \
    set_refresh_cookies, unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash

# mail
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidlovergt123@gmail.com'
app.config['MAIL_PASSWORD'] = 'hegy zyrn bbvu fphn'  # Use App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'vidlovergt123@gmail.com'

mail = Mail(app)

app.config["JWT_SECRET_KEY"] = "203920iosdf"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)

#session
app.config['SECRET_KEY'] = '203920iosdf'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)


# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)
# blocklist for revoked JTIS
REVOKED_JTIS = set()
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


# @app.before_request
# def before_request():
#     from flask import session, redirect, url_for
#     admin_url = request.path
#     is_admin = 'admin' in admin_url
#     # assert False, is_admin
#     if is_admin:
#         if not session.get('user_id') :
#             return redirect(url_for('login_page'))
#
#     print(admin_url)

import models
import routes



if __name__ == '__main__':
    app.run()
