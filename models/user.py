from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, index=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(128), nullable=True)
    role = db.Column(db.String(128), nullable=True)
    image = db.Column(db.String(128), nullable=True)
    remark = db.Column(db.String(256))

