# flask 프레임워크 임포트.
# render_template(페이지 이동), jsonify(json값 리턴), request(클라이언트 값 받기) 라이브러리 임포트
from flask import Flask, render_template, jsonify, request
# app.route를 쓸 수 있게 해주는 코드
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
# 컬렉션 정의. mc12th라는 컬렉션이 생성됨
db = client.mc12th
## HTML을 주는 부분
# 메인 페이지 - app.py 실행 후, localhost:5000으로 접속했을 때, 가장 먼저 출력
@app.route('/')
def home():
		# index.html에 원하는 클라이언트 파일 입력
    return render_template('main.html')

## API 역할을 하는 부분
#POST
@app.route('/', methods=['POST'])
def name():
sample_receive = request.form['sample_give']
print(sample_receive)
return jsonify({'POST'})
#GET
@app.route('/', methods=['GET'])
def name():
sample_receive = request.args.get('sample_give')
print(sample_receive)
return jsonify({'msg': 'GET'})
@app.route('/', methods=['GET'])
def listing():
    Foodlist = list(db.mc12th.find({}, {'_id': False}))

    return jsonify({'all_Foodlist':Foodlist})

# localhost:5000 으로 들어갈 수 있게 해주는 코드
if __name__ == '__main__':
app.run('0.0.0.0', port=5000, debug=True)

