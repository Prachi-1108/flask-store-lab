from flask import Flask, request, jsonify

app = Flask(__name__)

stores = [
    {
        "id": 1,
        "name": "Fashion Store",
        "location": "Vadodara"
    },
    {
        "id": 2,
        "name": "Electronics Store",
        "location": "Ahmedabad"
    }
]

products = []


@app.route("/")
def home():
    return "Flask Store API is running!"


@app.route("/stores", methods=["GET"])
def get_stores():
    return jsonify(stores)


@app.route("/stores", methods=["POST"])
def create_store():
    data = request.get_json()

    if not data or "name" not in data or "location" not in data:
        return jsonify({
            "error": "Name and location are required"
        }), 400

    new_store = {
        "id": len(stores) + 1,
        "name": data["name"],
        "location": data["location"]
    }

    stores.append(new_store)

    return jsonify(new_store), 201


@app.route("/stores/<int:store_id>", methods=["GET"])
def get_store(store_id):
    for store in stores:
        if store["id"] == store_id:
            return jsonify(store)

    return jsonify({
        "error": "Store not found"
    }), 404


@app.route("/stores/<int:store_id>/products", methods=["POST"])
def create_product(store_id):
    store_exists = False

    for store in stores:
        if store["id"] == store_id:
            store_exists = True
            break

    if not store_exists:
        return jsonify({
            "error": "Store not found"
        }), 404

    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({
            "error": "Product name and price are required"
        }), 400

    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"],
        "store_id": store_id
    }

    products.append(new_product)

    return jsonify(new_product), 201


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


if __name__ == "__main__":
    app.run(debug=True)