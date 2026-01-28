from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(
        db.Integer,
        db.ForeignKey('branch.id', ondelete='CASCADE'),
        index=True
    )

    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(128))
    role = db.Column(db.String(128))
    image = db.Column(db.String(128))
    remark = db.Column(db.String(256))



    branch = db.relationship('Branch', backref='users')

