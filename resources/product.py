from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import db, Product, Store
from schemas import ProductSchema

blp = Blueprint(
    "products",
    "products",
    url_prefix="/product",
    description="Operations on products"
)


@blp.route("/")
class ProductList(MethodView):

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return Product.query.all()

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        store_id = product_data["store_id"]

        store = Store.query.get(store_id)

        if not store:
            abort(404, message="Store not found.")

        product = Product(
            name=product_data["name"],
            price=product_data["price"],
            store_id=store_id
        )

        db.session.add(product)
        db.session.commit()

        return product


@blp.route("/<int:product_id>")
class ProductById(MethodView):

    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = Product.query.get(product_id)

        if not product:
            abort(404, message="Product not found.")

        return product

    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        product = Product.query.get(product_id)

        if not product:
            abort(404, message="Product not found.")

        store = Store.query.get(product_data["store_id"])

        if not store:
            abort(404, message="Store not found.")

        product.name = product_data["name"]
        product.price = product_data["price"]
        product.store_id = product_data["store_id"]

        db.session.commit()

        return product

    def delete(self, product_id):
        product = Product.query.get(product_id)

        if not product:
            abort(404, message="Product not found.")

        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted successfully."}, 200