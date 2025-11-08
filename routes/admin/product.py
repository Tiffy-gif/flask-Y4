from app import app , db
from sqlalchemy import text
from flask import request
from models import Product
from werkzeug.security import generate_password_hash

@app.get('/product/list')
def product_list():
    return get_product_info(product_id=0)
@app.get('/product/list/<int:product_id>')
def product_list_by_id(product_id):
    return get_product_info(product_id=product_id)
@app.post('/product/create')
def product_create():
    form = request.get_json()
    if not form:
        return 'no data'


    product = Product(
        branch_id=form.get('branch_id'),
        productname=form.get('productname'),
        email=form.get('email'),
        password=generate_password_hash(form.get('password')),
    )
    db.session.add(product)
    db.session.commit()
    return {
        'message': ' product have been created',
        'product': get_product_info(product.id)
    }, 200
@app.post('/product/delete')
def product_delete():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        }
    is_exist = get_product_info(form.get('product_id'))
    if is_exist.get('message'):
        return {
            'message': 'product not found!',
        } , 400
    sql_str = text("""delete from product where id = :product_id""")
    result = db.session.execute(sql_str,
                                {
                                    "product_id": form.get('product_id'),
                                })
    db.session.commit()
    return {
        'message': ' product have been deleted',
    }, 200
@app.put('/product/update')
def product_update():
    form = request.get_json()
    if not form:
        return {
            'message': 'no data',
        } , 400
    is_exist = get_product_info(form.get('product_id'))
    if is_exist.get('message'):
        return {
            'message': 'branh not found!',
        } , 400

    product = Product.query.get(form.get('product_id'))
    product.branch_id = form.get('branch_id')
    product.productname = form.get('productname')
    product.email = form.get('email')
    db.session.commit()

    return {
        'message': ' product have been updated'
    }, 200

def get_product_info(product_id: int = 0):
    if product_id == 0:
        sql_str = text("select * from product")
        result = db.session.execute(sql_str).fetchall()
        if not result:
            return {'message': 'product table is empty!'}
        return [dict(row._mapping) for row in result]

    if product_id != 0:
        sql_str = text("select * from product where id = :product_id")
        result = db.session.execute(sql_str , {"product_id": product_id}).fetchone()
        if not result:
            return {'message' : 'product is not found'}
    return dict(result._mapping)
