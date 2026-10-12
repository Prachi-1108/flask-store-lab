
import os
from datetime import timedelta

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from models import db
from resources.store import blp as StoreBlueprint
from resources.product import blp as ProductBlueprint
from resources.auth import blp as AuthBlueprint


def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "Flask Store API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY",
        "dev-only-change-this-secret-key"
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    db.init_app(app)

    jwt = JWTManager(app)
    api = Api(app)

    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ProductBlueprint)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)