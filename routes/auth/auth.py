# from datetime import timedelta
# from app import app, db
# from flask import request, jsonify, render_template, flash, redirect, url_for
# from sqlalchemy import text, select
# from flask_jwt_extended import create_access_token, get_jwt, set_access_cookies, create_refresh_token, \
#     set_refresh_cookies, unset_jwt_cookies
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager
# from werkzeug.security import check_password_hash
#
# from models import User
#
# # IMPORTANT: Add SECRET_KEY for Flask sessions (required for flash messages)
#   # Add this line!
# app.config["JWT_SECRET_KEY"] = "203920iosdf"  # Change this!
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
#
# #session
# app.config['SECRET_KEY'] = '203920iosdf'
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)
#
#
# # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
# jwt = JWTManager(app)
# # blocklist for revoked JTIS
# REVOKED_JTIS = set()
#
# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_data):
#     return jwt_data["jti"] in REVOKED_JTIS
#
# @app.route('/login')
# def login_index():
#     return render_template('login.html')
#
#
# @app.post('/login_confirm')
# def login_confirm():
#     username = request.form.get("username", None)
#     password = request.form.get("password", None)
#
#     # Validate input - REDIRECT instead of returning string
#     if not username or not password:
#         flash('Please enter both username and password.', 'danger')
#         return redirect(url_for('login_index') + '?error=1')
#
#     # Query user from database
#     sql_str = text("select * from user where username = :username")
#     result = db.session.execute(sql_str, {"username": username}).fetchone()
#
#     # Check if user exists - REDIRECT instead of returning string
#     if not result:
#         flash('Incorrect username or password. Please try again.', 'danger')
#         return redirect(url_for('login_index') + '?error=1')
#
#     user_id = str(result[1])
#     hash_password = result[4]
#     user_role = result[7]
#
#     # Verify password - REDIRECT instead of returning string
#     if not check_password_hash(hash_password, password):
#         flash('Incorrect username or password. Please try again.', 'danger')
#         return redirect(url_for('login_index') + '?error=1')
#
#     # Successful login
#     access_token = create_access_token(identity=user_id)
#
#     # Determine destination based on user role
#     if user_role == 'api':
#         destination_url = url_for('api')
#     else:
#         destination_url = url_for('index')
#
#     response = redirect(destination_url)
#     set_access_cookies(response, access_token)
#
#     # Optional success message
#     flash(f'Welcome back, {username}!', 'success')
#
#     return response
#
#
# # postman
# @app.post("/logout")
# @jwt_required()  # revoke current access token
# def logout1():
#     jti = get_jwt()["jti"]
#     REVOKED_JTIS.add(jti)
#     return jsonify(msg="Access Token Revoked")
#
#
# # postman - API login endpoint
# # @app.post('/login')
# # def login():
# #     username = request.json.get("username", None)
# #     password = request.json.get("password", None)
# #     sql_str = text("select * from user where username = :username")
# #     result = db.session.execute(sql_str, {"username": username}).fetchone()
# #     if not result:
# #         return jsonify({"msg": "Incorrect username or password"}), 401
# #     user_id = str(result[1])
# #     hash_password = result[4]
# #
# #     if check_password_hash(hash_password, password):
# #         access_token = create_access_token(identity=user_id)
# #         return jsonify(access_token=access_token)
# #     else:
# #         return jsonify({"msg": "Incorrect username or password"}), 401
#
#
