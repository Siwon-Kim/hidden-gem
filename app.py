
from flask import Flask, render_template, request, jsonify, redirect, url_for
from bson.objectid import ObjectId
from account import account


app = Flask(__name__)
app.register_blueprint(account)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.kpkxwy8.mongodb.net/?retryWrites=true&w=majority')
db = client.dbhiddengem



@app.route("/")
def home():
    client = MongoClient(
        "mongodb+srv://hidden:gem@cluster0.bdeer72.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client.dbtom
    stores = db.store
    return render_template("index.html", stores=stores)

#페이지 불러오기
@app.route('/login')
def go_login():
    return render_template("login.html")

@app.route('/register')
def go_register():
    return render_template("register.html")

@app.route("/store", methods=["POST"])
def store_post():
    url_receive = request.form["url_give"]
    comment_receive = request.form["comment_give"]
    star_receive = request.form["star_give"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    store_name = soup.select_one(
        "body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > header > div.restaurant_title_wrap > span > h1"
    ).text
    category = soup.select_one(
        "body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(3) > td > span"
    ).text
    address = soup.select_one(
        "body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(1) > td"
    ).text.split("지번")
    img_url = soup.find("img")["src"]

    store = {
        "store_name": store_name,
        "address": address[0],
        "category": category,
        "image": img_url,
        "store_comment": comment_receive,
        "star": star_receive,
    }

    db.stores.insert_one(store)
    return jsonify({"msg": "Store is Successfully Saved!"})


# Read
@app.route("/store", methods=["GET"])
def store_get():
    stores = list(db.stores.find())
    for store in stores:
        store["_id"] = str(store["_id"])
    # stores_info = list(db.stores.find({}, {"_id": False}))
    return jsonify({"stores": stores})


# # Update

# # Delete
@app.route("/store", methods=["DELETE"])
def delete_store():
    # id = request.args.to_dict

    # name = request.form.get("store_name")
    # print(name)
    id_get = request.form["id_give"]
    db.stores.delete_one({"_id": ObjectId(id_get)})
    return jsonify({"msg": "Store Deleted!"})

    # mydb = db["stores"]
    # print(mydb)
    # for i in mydb.keys("store_name"):
    #     if i == name:
    #         mydb.delete_one(myquery)
    # target = db.stores.keys(myquery)
    # print(target)
    # return redirect(url_for("home"))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
