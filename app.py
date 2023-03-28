from flask import Flask, render_template, request, jsonify
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
    print (1234)
    return render_template("index.html")

@app.route("/store", methods=["POST"])
def store_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    store_name = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > header > div.restaurant_title_wrap > span > h1').text
    category = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(3) > td > span').text
    address = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(1) > td').text.split('지번')
    img_url = soup.find("img")["src"]

    store = {
        "store_name": store_name,
        "address" : address[0],
        "category" : category,
        "image" : img_url,
        "store_comment": comment_receive,
        "star": star_receive,
    }

    db.stores.insert_one(store)
    return jsonify({"msg": "Store is Successfully Saved!"})


# Read
@app.route("/store", methods=["GET"])
def store_get():
    stores_info = list(db.stores.find({}, {'_id': False}))
    return jsonify({"stores": stores_info})


# # Update

# # Delete
# @app.route("/store/<int:id>", methods=["DELETE"])
# def delete_store(id):
#     for i, store in enumerate(stores):
#         if store["id"] == id:
#             stores.pop(i)
#             return jsonify(stores)
#     return jsonify("삭제 불가능한 식당입니다")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
