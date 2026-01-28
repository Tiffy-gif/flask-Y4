from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app import app , db
from sqlalchemy import text
from flask import request, render_template, redirect, url_for
from models import User
from werkzeug.security import generate_password_hash


@app.route('/register')
def register():
    return render_template('register.html')
@app.get('/user/list')

def user_list():
    return get_user_info(user_id=0)

@app.get('/user/list/<int:user_id>')
def user_list_by_id(user_id):
    return get_user_info(user_id=user_id)

@app.post('/user/delete/api')
def user_delete1():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        }
    is_exist = get_user_info(form.get('user_id'))
    if is_exist.get('message'):
        return {
            'message': 'User not found!',
        } , 400
    sql_str = text("""delete from user where id = :user_id""")
    result = db.session.execute(sql_str,
                                {
                                    "user_id": form.get('user_id'),
                                })
    db.session.commit()
    return {
        'message': ' user have been deleted',
    }, 200
@app.put('/user/update')
def user_update():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        } , 400
    is_exist = get_user_info(form.get('user_id'))
    if is_exist.get('message'):
        return {
            'message': 'User not found!',
        } , 400

    user = User.query.get(form.get('user_id'))
    user.branch_id = form.get('branch_id')
    user.username = form.get('username')
    user.email = form.get('email')
    db.session.commit()

    return {
        'message': ' user have been updated'
    }, 200

def get_user_info(user_id: int = 0):
    if user_id == 0:
        check_all_user = User.query.all()
        if not check_all_user:
            return {'message': 'user table is empty!'}
        return [
            {
                column.name : getattr(user , column.name)
                for column in user.__table__.columns
            }
            for user in check_all_user
        ]

    if user_id != 0:
        user_check_id = User.query.get(user_id)
        if not user_check_id:
            return {'message' : 'user is not found'}
    return dict(user_check_id=user_id)

@app.post('/user/create')
def user_create1():
    form = request.form
    password = form.get('password')
    password_confirmation = form.get('password_confirmation')
    branch_id = 1
    file = request.files.get('image')
    image= None
    if password != password_confirmation:
        return 'passwords do not match'

    if not form:
        return 'no data'

    if file and file.filename != '':
        file = request.files['image']
        filename = f"{form.get('name')}_{form.get('phone')}_{secure_filename(file.filename)}"
        file.save(f'./static/assets/images/userpf/{filename}')
        image = filename


    user = User(
        branch_id=branch_id,
        username=form.get('username'),
        email= form.get('email'),
        phone = form.get('phone'),
        password=generate_password_hash(form.get('password')),
        image=image
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login_index'))

# postman
@app.post('/user/create2')
def user_create2():
    form = request.form
    username = form.get('name')
    password = form.get('password')
    password_confirmation = form.get('password_confirmation')
    branch_id = 1
    file = request.files.get('image')
    image = None
    if password != password_confirmation:
        return 'passwords do not match'

    if not form:
        return 'no data'

    if file and file.filename != '':
        file = request.files['image']
        filename = f"{form.get('name')}_{form.get('phone')}_{secure_filename(file.filename)}"
        file.save(f'./static/assets/images/userpf/{filename}')
        image = filename


    user = User(
        branch_id=branch_id,
        username=form.get('username'),
        email= form.get('email'),
        phone = form.get('phone'),
        password=generate_password_hash(form.get('password')),
        image=image
    )
    db.session.add(user)
    db.session.commit()
    return {
        'message': ' User have been created',
        'branch': get_user_info(user.id)
    }, 200