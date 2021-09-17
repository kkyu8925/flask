from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://myUser:1234@3.35.246.21:27017/MyDB')
db = client.MyDB


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stock', methods=['POST'])
def save_info():
    info = request.args.get()
    print(info)
    stocks = list(db.codes.find({}, {'_id': False}))
    return jsonify({'stocks': stocks})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)