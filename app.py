from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# Create : crawling Needed Section
@app.route("/store", methods=["POST"])
def post_menu():
    next_id = len(stores) + 1
    request_data = request.get_json()
    store = {
        "id": next_id,
        "store_name": request_data["store_name"],
        "store_comment": request_data["store_comment"],
        "star": request_data["star"],
    }
    next_id += 1
    stores.append(store)
    return jsonify(store)


# Read
@app.route("/store")  # methods=["GET"]
def store_get():
    return jsonify({"stores": stores})


# Update

# Delete
@app.route("/store/<int:id>", methods=["DELETE"])
def delete_store(id):
    for i, store in enumerate(stores):
        if store["id"] == id:
            stores.pop(i)
            return jsonify(stores)
    return jsonify("삭제 불가능한 식당입니다")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
