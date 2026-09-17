from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import db, Store
from schemas import StoreSchema


blp = Blueprint(
    "stores",
    "stores",
    url_prefix="/store",
    description="Operations on stores"
)


@blp.route("/")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return Store.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = Store(
            name=store_data["name"],
            location=store_data["location"]
        )

        db.session.add(store)
        db.session.commit()

        return store


@blp.route("/<int:store_id>")
class StoreById(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = Store.query.get(store_id)

        if not store:
            abort(404, message="Store not found.")

        return store

    def delete(self, store_id):
        store = Store.query.get(store_id)

        if not store:
            abort(404, message="Store not found.")

        db.session.delete(store)
        db.session.commit()

        return {
            "message": "Store deleted successfully."
        }, 200