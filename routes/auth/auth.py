from datetime import timedelta

from app import app , db
from flask import request, jsonify, render_template, flash, redirect, url_for
from sqlalchemy import text, select

from flask_jwt_extended import create_access_token, get_jwt, set_access_cookies, create_refresh_token, \
    set_refresh_cookies, unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash

from models import User

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "203920iosdf"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)



# blocklist for revoked JTIS
REVOKED_JTIS = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header , jwt_data):
    return jwt_data["jti"] in REVOKED_JTIS

@app.route('/login')
def login_index():
    return render_template('login.html')


@app.post('/login_confirm')
def login_confirm():
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if not username or not password:
        return "Missing username or password.", 400

    sql_str = text("select * from user where username  = :username")
    result = db.session.execute(sql_str, {"username": username}).fetchone()


    if not result:
        return "Incorrect username or password", 401

    user_id = str(result[1])
    hash_password = result[4]
    user_role = result[7]


    if check_password_hash(hash_password, password):
        # Successful login
        access_token = create_access_token(identity=user_id)

        if user_role == 'api':
            destination_url = url_for('api')
        else:
            destination_url = url_for('index')

        response = redirect(destination_url)

        set_access_cookies(response, access_token)

        # 3. Return the response object
        return response

    else:
        return "Incorrect username or password", 401

# postman
@app.post("/logout")
@jwt_required() # revoke current access token
def logout():
    jti = get_jwt()["jti"]
    REVOKED_JTIS.add(jti)
    return jsonify(msg= "Access Token Revoked")

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
# @app.post("/login-confirm")
# def login():
#     username = request.json.get("username", None)
#     password = request.json.get("password", None)
#     sql_str = text("select * from user where username  = :username")
#     result = db.session.execute(sql_str, {"username": username}).fetchone()
#     if not result:
#         return jsonify({"msg": "Incorrect username or password"}), 401
#     user_id = str(result[1])
#     hash_password = result[4]
#
#     if check_password_hash(hash_password, password):
#         access_token = create_access_token(identity=user_id)
#         return jsonify(access_token=access_token)
#     else:
#         return jsonify({"msg": "Incorrect username or password"}), 401


# postman
@app.post('/login')
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    sql_str = text("select * from user where username  = :username")
    result = db.session.execute(sql_str, {"username": username}).fetchone()
    if not result:
        return jsonify({"msg": "Incorrect username or password"}), 401
    user_id = str(result[1])
    hash_password = result[4]

    if check_password_hash(hash_password, password):
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Incorrect username or password"}), 401
