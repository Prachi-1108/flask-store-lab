from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    products = db.relationship(
        "Product",
        backref="store",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(
        db.Integer,
        db.ForeignKey("store.id"),
        nullable=False
    )