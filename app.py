from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.kpkxwy8.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import account.py
import requests
from bs4 import BeautifulSoup

@app.route("/")
def home():
    return render_template("index.html")


# Create : crawling Needed Section
# @app.route("/store", methods=["POST"])
# def post_menu():
#     next_id = len(stores) + 1
#     request_data = request.get_json()
#     store = {
#         "id": next_id,
#         "store_name": request_data["store_name"],
#         "store_comment": request_data["store_comment"],
#         "star": request_data["star"],
#     }
#     next_id += 1
#     stores.append(store)
#     return jsonify(store)

@app.route("/store", methods=["POST"])
def post_menu():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    store_name = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > header > div.restaurant_title_wrap > span > h1').get_text()
    category = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(3) > td > span').get_text()
    address = soup.select_one('body > main > article > div.column-wrapper > div.column-contents > div > section.restaurant-detail > table > tbody > tr:nth-child(1) > td').get_text().split('지번')
    imgUrl = soup.find("img")["src"]

    next_id = len(stores) + 1
    #request_data = request.get_json()

    store = {
        "id": next_id,
        "store_name": store_name,
        "address" : address[0],
        "category" : category,
        "image" : imgUrl,
        "store_comment": comment_receive,
        "star": star_receive,
    }
    next_id += 1
    stores.append(store)
    db.stores.insert_one(store)
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
