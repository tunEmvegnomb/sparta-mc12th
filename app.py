# flask 프레임워크 임포트.
# render_template(페이지 이동), jsonify(json값 리턴), request(클라이언트 값 받기), session(로그인) 라이브러리 임포트
from flask import Flask, render_template, jsonify, request, session

from pymongo import MongoClient

# 클라이언트 정의 - MongoClient를 로컬호스트와 연결
client = MongoClient('mongodb+srv://making:making@cluster0.ymxju.mongodb.net/Cluster0?retryWrites=true&w=majority')

# 컬렉션 정의. mc12th라는 컬렉션이 생성됨
db = client.mc12th

# app.route를 쓸 수 있게 해주는 코드
app = Flask(__name__)


# 메인 페이지 - app.py 실행 후, localhost:5000으로 접속했을 때, 가장 먼저 출력
@app.route('/')
def render_main():
    # index.html에 원하는 클라이언트 파일 입력
    return render_template('main.html')


# 리스트 페이지
@app.route('/list')
def render_list():
    return render_template('list.html')


# 레시피 페이지
@app.route('/detail')
def render_detail():
    return render_template('detail.html')


# 테마 페이지
@app.route('/theme')
def render_theme():
    return render_template('theme.html')


# 인기 페이지
@app.route('/rank')
def render_rank():
    return render_template('rank.html')


# 나만의 레시피 작성 페이지
@app.route('/write')
def render_write():
    return render_template('write.html')


# 마이 페이지
@app.route('/mypage')
def render_mypage():
    return render_template('mypage.html')


# 즐겨찾기 조회 페이지
@app.route('/mylike')
def render_mylike():
    return render_template('mylike.html')


# 나만의 레시피 조회 페이지
@app.route('/myrecipe')
def render_myrecipe():
    return render_template('myrecipe.html')


# 로그인 페이지
@app.route('/login')
def render_login():
    return render_template('login.html')


# 회원가입 페이지
@app.route('/signup')
def render_signup():
    return render_template('signup.html')


## API 역할을 하는 부분

# POST
@app.route('/', methods=['POST'])
def name():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'POST'})


# GET
@app.route('/', methods=['GET'])
def name_get():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': 'GET'})


# GET 2
@app.route('/', methods=['GET'])
# list
def listing():
    Foodlist = list(db.mc12th.find({}, {'_id': False}))

    return jsonify({'all_Foodlist': Foodlist})


# 리뷰(댓글) create 기능
@app.route('/detail/review-post', methods=['POST'])
def review_post():
    if 'user_id' in session:
        user_name_receive = request.form['user_name_give']
        review_content_receive = request.form['review_content_give']

        doc = {
            'user_name': user_name_receive,
            'review_content': review_content_receive
        }
        db.review.insert_one(doc)
        return jsonify({'msg': '댓글 작성 완료'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 리뷰(댓글) list기능
@app.route('/detail/review-list', methods=['GET'])
def review_list():
    reviews = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews': reviews})


# 리뷰(댓글) update 기능
@app.route('/detail/review-update', methods=['POST'])
def review_update():
    if 'user_id' in session:
        user_name_receive = request.form['user_name_give']
        update_content_receive = request.form['review_content_give']

        db.review.update_one({'user_name': user_name_receive}, {'$set': {'review_content': update_content_receive}})
        return jsonify({'POST': '댓글 수정 완료'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 리뷰(댓글) 삭제 기능
@app.route('/detail/review-delete', methods=['POST'])
def review_delete():
    if 'user_id' in session:
        user_name_receive = request.form['user_name_give']
        db.review.delete_one({'name': user_name_receive})
        return jsonify({'msg': '댓글이 삭제되었습니다'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 상세페이지 - 상세 레시피 데이터 출력
# list페이지에서 해당card를 클릭하면 get요청으로 레시피이름이 url을 통해 넘어와
@app.route('/detail/recipe-detail', methods=['GET'])
def recipe_detail():
    recipe_name_receive = request.args.get('recipe_name_give')
    target_recipe = db.recipe.find_one({'recipe_name': recipe_name_receive})
    return jsonify({'recipe': target_recipe})

# localhost:5000 으로 들어갈 수 있게 해주는 코드
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)