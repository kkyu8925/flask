from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://myUser:1234@3.35.246.21:27017/MyDB')
db = client.MyDB

import requests
from bs4 import BeautifulSoup


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/base/codes', methods=['GET'])
def get_base_codes():
    codes = list(db.codes.find({}, {
        '_id': False}).distinct("group"))
    return jsonify({'codes': codes})


@app.route('/codes', methods=['GET'])
def get_codes():
    group = request.args.get("group")
    groups = list(db.codes.find({"group": group}, {'_id': False}))
    return jsonify({'groups': groups})


@app.route('/stock', methods=['POST'])
def stock():
    market = request.json['market']
    sector = request.json['sector']
    tag = request.json['tag']
    print(market)
    print(sector)
    print(tag)

    stocks = list(db.stocks.find({"market": market, "sector": sector, "tag": tag}, {'_id': False}))
    return jsonify({'stocks': stocks})


@app.route('/info', methods=['GET'])
def info():
    stock_code = request.args.get("stock_code")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://finance.naver.com/item/main.nhn?code=${stock_code}', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup)

    # price = soup.select_one('#chart_area > div.rate_info > div > p.no_today > em')
    market_cap = soup.select_one('#_market_sum')
    per = soup.select_one('#tab_con1 > div:nth-child(6) > table > tbody > tr.strong > td > em')
    # print(price)
    print(market_cap)
    # print(per)

    return jsonify({'price': '주가', 'market_cap': '시총', 'per': '펄'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
