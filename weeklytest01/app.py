from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('mongodb://myUser:1234@3.35.246.21:27017/MyDB')
db = client.MyDB


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/base/codes', methods=['GET'])
def get_base_codes():
    codes = list(db.codes.find({}, {'_id': False}).distinct("group"))
    return jsonify({'codes': codes})


@app.route('/codes', methods=['GET'])
def get_codes():
    group = request.args.get("group")
    groups = list(db.codes.find({"group": group}, {'_id': False}))
    return jsonify({'groups': groups})


@app.route('/stocks', methods=['POST'])
def stocks():
    info = request.json
    stocks = list(db.stocks.find(info, {'_id': False}))
    return jsonify({'stocks': stocks})


@app.route('/stock/like', methods=['PUT'])
def set_like():
    info = request.json
    db.stocks.update_one({"code": info['code']}, {"$set": {"isLike": True}})
    return "success"


@app.route('/stock/unlike', methods=['PUT'])
def set_unlike():
    info = request.json
    db.stocks.update_one({"code": info['code']}, {"$set": {"isLike": False}})
    return "success"


@app.route('/stocks/like', methods=['GET'])
def get_stocks():
    stocks = list(db.stocks.find({"isLike": True}, {'_id': False}))
    return jsonify({'stocks': stocks})


@app.route('/stock', methods=['GET'])
def stock():
    stock_code = request.args.get("stock_code")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    data = requests.get('https://finance.naver.com/item/main.nhn?code=' + stock_code, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    amount = soup.select_one('#_market_sum').text
    amount = amount.replace('\n', '')
    amount = amount.replace('\t', '')
    if soup.select_one('#_per') is None:
        per = 'N/A'
    else:
        per = soup.select_one('#_per').text
    price = soup.select_one(
        '#content > div.section.trade_compare > table > tbody > tr:nth-child(1) > td:nth-child(2)').text

    return jsonify({'amount': amount, 'per': per, 'price': price})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
