
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from schemas import LoginSchema


blp = Blueprint(
    "auth",
    "auth",
    url_prefix="",
    description="Authentication operations"
)

# Demo account for this lab only
DEMO_USERNAME = "admin"
DEMO_PASSWORD_HASH = generate_password_hash("admin123")


@blp.route("/login")
class Login(MethodView):

    @blp.arguments(LoginSchema)
    def post(self, login_data):
        username = login_data["username"]
        password = login_data["password"]

        if (
            username != DEMO_USERNAME
            or not check_password_hash(DEMO_PASSWORD_HASH, password)
        ):
            abort(401, message="Invalid username or password.")

        access_token = create_access_token(
            identity=username,
            fresh=True
        )

        return {
            "message": "Login successful.",
            "access_token": access_token,
            "token_type": "Bearer"
        }, 200