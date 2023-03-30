from flask import Flask, render_template, request, jsonify, redirect, url_for
from bson.objectid import ObjectId
from account import account


app = Flask(__name__)
app.register_blueprint(account)

import requests, certifi, jwt

SECRET_KEY = "SPARTA"

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://siwon:rlaznf11@cluster0.icysouv.mongodb.net/?retryWrites=true&w=majority"
)
db = client.dbHiddenGem


@app.route("/")
def home():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("index.html", nickname=user_info["nick"])
    except:
        return render_template("index.html")
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for(".login", msg="로그인 정보가 존재하지 않습니다."))

    # stores = db.store
    # return render_template("index.html", stores=stores)


# 페이지 불러오기
@app.route("/login")
def go_login():
    return render_template("login.html")


@app.route("/register")
def go_register():
    return render_template("register.html")


@app.route("/store", methods=["POST"])
def store_post():
    # 입력으로 받아온 URL을 통해 크롤링합니다
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
    like = 0

    # 로그인된 유저 정보도 DB에 추가합니다
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload["id"]
    except:
        userid = None
        
    store = {
        "store_name": store_name,
        "address": address[0],
        "category": category,
        "image": img_url,
        "store_comment": comment_receive,
        "star": star_receive,
        "like": like,
        "userid": userid
    }

    db.stores.insert_one(store)
    return jsonify({"msg": "Store is Successfully Saved!"})


# Read
@app.route("/store", methods=["GET"])
def store_get():
    stores = list(db.stores.find())
    for store in stores:
        store["_id"] = str(store["_id"])
    
    # FE에서 해당 유저의 like 클릭 판별을 위한 부분
    userid, liked_store = None, []
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload["id"]
        user_info = list(db.user.find({'id': userid}))
        for info in user_info:
            for liked_s in info["liked_store"]:
                liked_store.append(str(liked_s))
        return jsonify({"stores": stores, "userid": userid, "liked_store": liked_store})
    except:
        return jsonify({"stores": stores, "userid": userid, "liked_store": liked_store})


# Update
@app.route("/update", methods=["POST"])
def store_update():
    pass

# Delete
@app.route("/store", methods=["DELETE"])
def store_delete():
    id_receive = request.form["id_give"]
    db.stores.delete_one({"_id": ObjectId(id_receive)})
    return jsonify({"msg": "Store is successfully deleted!"})


# Like button
@app.route("/likeUp", methods=["POST"])
def like_up():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload["id"]

        store_id_receive = request.form["id_give"]

        # store id를 기준으로 현재 like의 개수를 추출
        like = db.stores.find_one({"_id": ObjectId(store_id_receive)}, {"like": 1})
        num_like = int(like["like"]) + 1

        # db에서 store의 like 개수 update시켜줄 부분
        add_like = {"$set": {"like": num_like}}
        db.stores.update_one({"_id": ObjectId(store_id_receive)}, add_like)

        # db에서 해당 사용자가 해당 store에 like를 눌렀다는 요소 추가
        add_liked_store = {'$addToSet': {'liked_store': store_id_receive}}
        db.user.update_one({'id': userid}, add_liked_store)
        
        return jsonify({"msg": "You added Like"})
    
    except jwt.ExpiredSignatureError:
        return redirect(url_for("go_login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("go_login", msg="로그인 정보가 존재하지 않습니다."))


@app.route("/likeDown", methods=["POST"])
def like_down():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload["id"]

        store_id_receive = request.form["id_give"]

        # store id를 기준으로 현재 like의 개수를 추출
        like = db.stores.find_one({"_id": ObjectId(request.form["id_give"])}, {"like": 1})
        num_like = int(like["like"]) - 1

        # db에서 store의 like 개수 update시켜줄 부분
        add_like = {"$set": {"like": num_like}}
        db.stores.update_one({"_id": ObjectId(request.form["id_give"])}, add_like)

        # db에서 해당 사용자가 해당 store에 like를 지웠다는 요소 추가
        print('down', userid, store_id_receive)
        delete_liked_store = {'$pull': {'liked_store': store_id_receive}}
        db.user.update_one({'id': userid}, delete_liked_store)
        
        return jsonify({"msg": "You deleted Like"})
    
    except jwt.ExpiredSignatureError:
        return redirect(url_for("go_login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("go_login", msg="로그인 정보가 존재하지 않습니다."))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
