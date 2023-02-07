from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.dbjungle


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.article.find({}, {'_id': False}))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result': 'success', 'msg': 'GET 연결되었습니다!', 'article': result})


# API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give']  # 클라이언트로부터 url 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    url_title = soup.select_one('meta[property="og:title"]')['content']
    url_image = soup.select_one('meta[property="og:image"]')['content']
    url_desc = soup.select_one('meta[property="og:description"]')['content']

    article = {
        'url': url_receive,
        'title': url_title,
        'image': url_image,
        'desc': url_desc,
        'comment': comment_receive
    }

    # 3. mongoDB에 데이터 넣기
    db.article.insert_one(article)
    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
