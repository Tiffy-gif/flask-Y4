from app import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    products = db.relationship(
        'Product',
        backref='category',
        cascade='all, delete-orphan',
        lazy=True
    )
