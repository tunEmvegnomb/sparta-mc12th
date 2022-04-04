# flask 프레임워크 임포트.
# render_template(페이지 이동), jsonify(json값 리턴), request(클라이언트 값 받기), session(로그인) 라이브러리 임포트
import os

from flask import Flask, render_template, jsonify, request, session

# 현재 날짜를 받아오기위한 import
from datetime import datetime, timedelta

import threading



# 이미지파일 삭제를 위한 import
import os

# 암호화 라이브러리 bcrypy import. 오류가 뜬다면 interpreter에서 bcrypy 패키지 install
# 그래도 오류가 뜬다면 terminal에서 pip install flask-bcrypt 입력
from flask_bcrypt import Bcrypt

# MongoClient(몽고DB 관리 라이브러리) 임포트
from pymongo import MongoClient

# _id값을 받아오기 위해 import
from bson.objectid import ObjectId

# 클라이언트 정의 - MongoClient를 로컬호스트와 연결
# client = MongoClient('mongodb+srv://making:making@cluster0.ymxju.mongodb.net/Cluster0?retryWrites=true&w=majority')
client = MongoClient('localhost',27017)


# 컬렉션 정의. mc12th라는 컬렉션이 생성됨
db = client.mc12th

# app.route를 쓸 수 있게 해주는 코드
app = Flask(__name__)

# 암호화를 위한 bcrypt 시크릿 키
app.config['SECRET_KEY'] = 'Blue Like Aquamarine'
app.config['BCRYPT_LEVEL'] = 10

bcrypt = Bcrypt(app)


# pw_hash = bcrypt.hashpw("password".encode("utf-8"), bycrypt.gensalt())
# pw_hash2 = bcrypt.hashpw("password".encode("utf-8"), bycrypt.gensalt())

# pw_hash = bcrypt.generate_password_hash('password')
# bcrypt.checkpw("password", pw_hash)  # True
# 즉 password 라는 비밀번호를 암호화하고, 이후에 체크하는 작업을 할때 해당 메소드를 통해 일치여부 확인 가능

# pw_hash == pw_hash2  # False


# 그러나 같은 password를 넣어도 다른 암호화 값이 나온다.


# 메인 페이지 - app.py 실행 후, localhost:5000으로 접속했을 때, 가장 먼저 출력
@app.route('/', methods=['GET'])
def render_main():
    # index.html에 원하는 클라이언트 파일 입력
    return render_template('main.html')


# 메인페이지 API
# 추천배너 데이터 출력 API
@app.route('/reco', methods=['GET'])
def main_reco():
    # 페이크 리턴 값
    reco_data = [{'recipe_name': '순두부계란탕'}]
    return jsonify({'reco_data': reco_data})


# 메인페이지 API
# 인기배너 데이터 출력 API
@app.route('/top3', methods=['GET'])
def main_top3():
    # 페이크 리턴 값
    # top3_recipe = [
    #     {
    #         'recipe_img': 'https://recipe1.ezmember.co.kr/cache/recipe/2020/09/08/52110f292b905a27c30ea6bfed246a491.jpg'
    #     },
    #
    #     {
    #         'recipe_img': 'https://recipe1.ezmember.co.kr/cache/recipe/2019/01/12/b9343d314206275c1b6d0d0c4fcc2ce71.jpg'
    #     },
    #
    #     {
    #         'recipe_img': 'https://recipe1.ezmember.co.kr/cache/recipe/2016/09/01/484b1194a69d0b2da09014a25a9334de1.jpg'
    #     }
    # ]
    #
    # return jsonify({'filtered_data': top3_recipe})

    # 설계
    # 1. 사용자 요청 값 받기
    # 클릭 요청 값 - 연간/월간/일간 으로 구분
    click_receive = request.args.get('click_give')
    # 날짜 요청 값 - 사용자의 현재 시각을 문자열로 "yyyy-mm-dd" 받아옴
    date_receive = request.args.get('date_give')
    # 2. 날짜 리시브를 스플릿하여 년 월 일 조건 변수 생성
    year_receive = date_receive.split('-')[0]
    month_receive = year_receive + "-" + date_receive.split('-')[1]
    day_receive = date_receive
    print(year_receive, month_receive, day_receive)

    # 3. 조건문1 - 클릭 리시브 확인
    # 값이 만약 연간이라면
    if click_receive == "연간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        find_db = db.recipes.find({'recipe_post_update': {'$regex': year_receive}}, {'_id': False})
        top3_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(3))

    # 값이 만약 월간이라면
    elif click_receive == "월간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        find_db = db.recipes.find({'recipe_post_update': {'$regex': month_receive}}, {'_id': False})
        top3_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(3))

    # 값이 만약 일간이라면
    elif click_receive == "일간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬
        find_db = db.recipes.find({'recipe_post_update': {'$regex': day_receive}}, {'_id': False})
        top3_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(3))

    return jsonify({'filtered_data': top3_db})


# 리스트 페이지
@app.route('/list')
def render_list():
    return render_template('list.html')


# 리스트 페이지 API
# 다큐먼트 시작 시 데이터를 출력하는 API
@app.route('/list/data', methods=['GET'])
def list_data_append():
    # 페이크 값 리턴
    limited_data = list(db.recipes.find({}, {'_id': False}).limit(18))
    return jsonify({'append_data': limited_data})


# 리스트 페이지 API
# 추천순, 최신순 정렬 API
@app.route('/list/order', methods=['GET'])
def list_order():
    # 설계
    # 1. 사용자 요청 값 받기
    # 클릭 요청 값 - 추천순/최신순 으로 구분
    click_receive = request.args.get('click_give')

    # 3. 조건문1 - 클릭 리시브 확인
    # 값이 만약 추천순이라면
    if click_receive == "추천순":
        # 추천수를 기준으로 데이터 sort
        ordered_data = list(db.recipes.find({}, {'_id': False}).sort('recipe_like', -1))
    # 값이 만약 최신순이라면
    elif click_receive == "최신순":
        # 작성 날짜를 기준으로 데이터 sort
        ordered_data = list(db.recipes.find({}, {'_id': False}).sort('recipe_post_update', -1))

    return jsonify({'filtered_data': ordered_data})


# 리스트 페이지 API
# 리스트 필터 API


@app.route('/list/filter', methods=['GET'])
def list_filter():

    # 설계
    # 1. 사용자 요청 값 받기
    # 맛태그 리시브
    taste_receive = request.args.get('taste_give')
    # 재료 리시브
    ing_receive = request.args.get('ing_give')
    # 난이도 리시브
    diff_receive = request.args.get('diff_give')
    # 조리시간 리시브
    time_receive = request.args.get('time_give')

    print("요청 받음!", taste_receive, ing_receive, diff_receive, time_receive)

    # 리턴할 데이터 초기화
    filtered_data = []

    # 2. 조건1 - 단독 필터
    # 맛태그만 비어있지 않다면
    if taste_receive is not None and (ing_receive,diff_receive,time_receive is None):
        # 맛태그에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste':taste_receive},{'_id':False}))
        print('단독 필터 맛태그')
        filtered_data.append(db_find)
    # 재료만 비어있지 않다면
    elif ing_receive is not None and (taste_receive, diff_receive, time_receive is None):
        # 재료에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_ing':{'$regex':ing_receive}},{'_id':False}))
        print('단독 재료 맛태그')
        filtered_data.append(db_find)
    # 난이도만 비어있지 않다면
    elif diff_receive is not None and (taste_receive, ing_receive, time_receive is None):
        # 난이도에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_diff': diff_receive},{'_id':False}))
        print('단독 난이도 맛태그')
        filtered_data.append(db_find)
    # 조리시간만 비어있지 않다면
    elif time_receive is not None and (taste_receive, ing_receive, diff_receive is None):
        # 조리시간에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_time': time_receive},{'_id': False}))
        print('단독 조리시간 맛태그')
        filtered_data.append(db_find)

    # 3. 조건2 - 두 가지 필터 중첩
    # 맛태그와 재료 해당
    elif (taste_receive, ing_receive is not None) and (diff_receive, time_receive is None):
        # 맛태그와 재료에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste': taste_receive, 'recipe_ing': {'$regex':ing_receive}},{'_id': False}))
        print('이중중첩 필터 맛태그 재료')
        filtered_data.append(db_find)

    # 맛태그와 난이도 해당
    elif (taste_receive, diff_receive is not None) and (ing_receive, time_receive is None):
        # 맛태그와 재료에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste': taste_receive, 'recipe_diff': diff_receive},{'_id': False}))
        print('이중중첩 필터 맛태그 난이도')
        filtered_data.append(db_find)

    # 맛태그와 조리시간 해당
    elif (taste_receive, time_receive is not None) and (ing_receive, diff_receive is None):
        # 맛태그와 조리시간에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste': taste_receive, 'recipe_time': time_receive},{'_id': False}))
        print('이중중첩 필터 맛태그 조리시간')
        filtered_data.append(db_find)

    # 재료와 난이도 해당
    elif (ing_receive, diff_receive is not None) and (taste_receive, time_receive is None):
        # 재료와 난이도에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_ing':{'$regex':ing_receive}, 'recipe_diff': diff_receive},{'_id':False}))
        print('이중중첩 필터 재료 난이도')
        filtered_data.append(db_find)

    # 재료와 조리시간 해당
    elif (ing_receive, time_receive is not None) and (taste_receive, diff_receive is None):
        # 재료와 조리시간에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_ing': {'$regex':ing_receive}, 'recipe_time': time_receive},{'_id': False}))
        print('이중중첩 필터 재료 조리시간')
        filtered_data.append(db_find)

    # 난이도와 조리시간 해당
    elif (diff_receive, time_receive is not None) and (taste_receive, ing_receive is None):
        # 난이도와 조리시간에 해당하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_diff': diff_receive, 'recipe_time':time_receive},{'_id':False}))
        print('이중중첩 필터 난이도 조리시간')
        filtered_data.append(db_find)

    # 4. 조건3 - 세 가지 필터 중첩
    # 맛태그와 재료와 난이도
    elif (taste_receive, ing_receive, diff_receive is not None) and time_receive is None:
        # 맛태그, 재료, 난이도 모두 일치하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste': taste_receive, 'recipe_ing': {'$regex':ing_receive}, 'recipe_diff': diff_receive},{'_id': False}))
        print('삼중중첩 필터 맛태그 재료 난이도')
        filtered_data.append(db_find)

    # 맛태그와 재료와 조리시간
    elif (taste_receive, ing_receive, time_receive is not None) and diff_receive is None:
        # 맛태그, 재료, 조리시간 모두 일치하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste':taste_receive, 'recipe_ing': {'$regex':ing_receive}, 'recipe_time': time_receive},{'_id': False}))
        print('삼중중첩 필터 맛태그 재료 조리시간')
        filtered_data.append(db_find)
    # 맛태그와 난이도와 조리시간
    elif(taste_receive, diff_receive, time_receive is not None) and ing_receive is None:
        # 맛태그, 난이도, 조리시간 모두 일치하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_taste': taste_receive, 'recipe_diff': diff_receive, 'recipe_time': time_receive},{'_id': False}))
        print('삼중중첩 필터 맛태그 난이도 조리시간', db_find)

        filtered_data.append(db_find)
    # 재료와 난이도 조리시간
    elif (ing_receive, diff_receive, time_receive is not None) and taste_receive is None:
        # 재료, 난이도, 조리시간 모두 일치하는 데이터 어펜드
        db_find = list(db.recipes.find({'recipe_ing': {'$regex':ing_receive}, 'recipe_diff': diff_receive, 'recipe_time': time_receive},{'_id': False}))
        print('삼중중첩 필터 재료 난이도 조리시간')
        filtered_data.append(db_find)

    # 5. 조건4 - 모든 데이터 일치
    # 모든 데이터에 일치하는 데이터 어펜드
    elif (taste_receive, ing_receive, diff_receive, time_receive is not None):
        db_find = list(db.recipes.find({'recipe_taste':taste_receive, 'recipe_ing': {'$regex':ing_receive}, 'recipe_diff': diff_receive, 'recipe_time': time_receive},{'_id: False'}))
        print('모두 존재')
        filtered_data.append(db_find)

    # 6. 처리 - 데이터 리턴
    print("필터 데이터!",filtered_data)
    return jsonify({'filtered_data': filtered_data})



# 리스트 페이지 API
# 리스트 검색 API


@app.route('/list/search', methods=['GET'])
def list_search():
    # 페이크 값 리턴
    searched_data = list(db.recipes.find({}, {'_id': False}).limit(18))
    return jsonify({'filtered_data': searched_data})


# 테마 페이지
@app.route('/theme')
def render_theme():
    return render_template('theme.html')


# 테마 페이지 API
# 테마 레시피 데이터 출력 API


@app.route('/theme', methods=['GET'])
def theme_data():
    # 페이크 값 리턴
    append_data = list(db.recipes.find({}, {'_id': False}).limit(3))
    return jsonify({'append_data': append_data})


# 인기 페이지
@app.route('/rank')
def render_rank():
    return render_template('rank.html')


# 리퀘스트 변수로 받기 #


# @app.route('/rank/get', methods=['GET'])
# def rank_get():
# year_give = request.args.get('date_year')
# month_give = request.args.get('date_month')
# day_give = request.args.get('date_day')
# click_receive = request.args.get('click_data')
# print(year_give, month_give, day_give, click_receive)
#
# # 레시피 데이터 베이스 가져오기
# # 데이터베이스에서 상위 10개 가져오기
# recipes = list(db.recipes.find({}, {'_id': False}
#                                ).sort('recipe_like', -1).limit(10))
#
# # 반복문 사용(데이터 출력용도)
# for db_recipe in recipes:
#     # 날짜값 스플릿
#     db_date = db_recipe['recipe_post_update']
#     # 스플릿데이터 - 년도
#     db_year = db_date.split('-')[0]
#     # 스플릿데이터 - 월
#     db_month = db_date.split('-')[1]
#     # 스플릿데이터 - 일
#     db_day = db_date.split('-')[2]
#
#     # 조건문 - 클릭 리시브
#     if click_receive == '연간':
#         # 년도에 따라 데이터 출력
#         if db_year == "2022":
#             db_yearlist = db_recipe
#             print('연간 데이터 출력 완료!')
#             return jsonify({'filtered_data': db_yearlist})
#
#     elif click_receive == '월간':
#         if db_month == "03":
#             db_monthlist = db_recipe
#             print('월간 데이터 출력 완료!')
#             return jsonify({'filtered_data': db_monthlist})
#
#     elif click_receive == '일간':
#         if db_day == "01":
#             db_daylist = db_recipe
#             print('일간 데이터 출력 완료!')
#             return jsonify({'filtered_data': db_daylist})

# # 조건문1
# # 업데이트 날짜 기준으로 연간체크
# for db_recipe in recipes:
#     #업데이트 날짜 기준
#     db_date = db_recipe['recipe_post_update']
#     #연도 스플릿
#     db_year = db_date.split('-')[0]
#     # 년도에 따라 데이터 출력
#     if db_year == "2022":
#         db_yearlist = db_recipe
#         print(db_yearlist)

# 인기 페이지 API
# 인기 데이터 10개 조회 API
# 리퀘스트 변수로 받기 #


@app.route('/rank/get', methods=['GET'])
def rank_get():
    # 설계
    # 1. 사용자 요청 값 받기
    # 클릭 요청 값 - 연간/월간/일간 으로 구분
    click_receive = request.args.get('click_give')
    # 날짜 요청 값 - 사용자의 현재 시각을 문자열로 "yyyy-mm-dd" 받아옴
    date_receive = request.args.get('date_give')
    # 2. 날짜 리시브를 스플릿하여 년 월 일 조건 변수 생성
    year_receive = date_receive.split('-')[0]
    month_receive = year_receive + "-" + date_receive.split('-')[1]
    day_receive = date_receive

    print(year_receive, month_receive, day_receive)

    # 3. 조건문1 - 클릭 리시브 확인
    # 값이 만약 연간이라면
    if click_receive == "연간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        find_db = db.recipes.find({'recipe_post_update': {'$regex': year_receive}}, {'_id': False})
        find_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(10))
    # 값이 만약 월간이라면
    elif click_receive == "월간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        find_db = db.recipes.find({'recipe_post_update': {'$regex': month_receive}}, {'_id': False})
        find_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(10))
    # 값이 만약 일간이라면
    elif click_receive == "일간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬
        find_db = db.recipes.find({'recipe_post_update': {'$regex': day_receive}}, {'_id': False})
        find_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(10))

    return jsonify({'filtered_data': find_db})


# 마이 페이지
@app.route('/mypage')
def render_mypage():
    return render_template('mypage.html')

# 즐겨찾기 조회 페이지
@app.route('/mylike')
def render_mylike():
    return render_template('mylike.html')


# 로그인 페이지
@app.route('/login')
def render_login():
    return render_template('login.html')


# 로그인 페이지 API
# 로그인 체크
@app.route('/login/check', methods=['POST'])
def login_check():
    # 페이크 값 리턴
    # return jsonify({'msg': '로그인에 성공하였습니다. 환영합니다!'})

    # 설계
    # 1. 사용자 요청값 POST
    # 아이디 리시브
    id_receive = request.form['user_id']
    # 비밀번호 리시브
    pwd_receive = request.form['user_pwd']

    # 2. 조건문1 - 입력확인
    # 인풋의 모든 데이터가 없다면 실패 메시지 리턴
    if (id_receive, pwd_receive) is None:
        return jsonify({'msg': '정보를 빠짐없이 입력해주세요'})
    else:
        # 3. 아이디, 비밀번호 조회
        # 데이터베이스에서 아이디에 일치하는 데이터 찾기
        find_db = list(db.users.find({'user_id': id_receive}, {'_id': False}))

        # 4. 조건문2 - 아이디 일치
        # 조회 데이터가 존재하지 않는다면 실패 메시지 리턴
        if find_db is None:
            return jsonify({'msg': '아이디 및 비밀번호가 일치하지 않습니다'})
        else:
            # 5. 조건문3 - 비밀번호 체크

            # 데이터베이스에 저장된 사용자 비밀번호 가져오기
            # 리스트를 자를 수 없기 때문에 반복문으로 나누기
            for find in find_db:
                pw_hash = find['user_pwd']

                # 데이터가 둘다 문자열일 경우 테스트용 해시 작업 코드
                # pw_hash = bcrypt.generate_password_hash(pw_hash)

                # 비밀번호 체크 알고리즘(사용자 요청값 암호화 하지 않아도 됨. 괄호() 안에 데이터 두개를 넣기
                pwd_check = bcrypt.check_password_hash(pw_hash, pwd_receive)  # True, False 리턴
                # 비밀번호가 일치하지 않는다면 실패 메시지 리턴
                if pwd_check == False:
                    return jsonify({'msg': '비밀번호가 일치하지 않습니다'})
                # 비밀번호가 일치한다면 처리
                else:
                    # 사용자 아이디로 세션 삽입
                    session['user_id'] = id_receive
                    # 조회 성공 메시지 리턴
                    return jsonify({'msg': '로그인에 성공하였습니다. 환영합니다!'})


# 회원가입 페이지
@app.route('/signup')
def render_signup():
    return render_template('signup.html')


# 회원가입 페이지 API
# 회원가입 체크


@app.route('/signup', methods=['POST'])
def signup_check():
    # API 설계
    # 1. 사용자 요청 값을 받음(POST) - 아이디(이메일), 비밀번호, 비밀번호 확인, 닉네임
    # 이메일의 형태 검사는 verify API를 추가할 예정
    id_receive = request.form['user_id']
    pwd_receive = request.form['user_pwd']
    pwd2_receive = request.form['user_pwd2']
    nickname_receive = request.form['user_nickname']
    print(id_receive, pwd_receive, pwd2_receive, nickname_receive)
    # 2. 조건문1 - 입력확인
    # 데이터가 모두 입력되어 있지 않다면, fail msg return
    if (id_receive, pwd_receive, pwd2_receive, nickname_receive) is None:
        return jsonify({'response': 'failed_input_check','msg': '입력되지 않은 정보가 존재합니다'})
    # 데이터가 모두 입력되어 있다면, 조건문2 이동
    else:
        # 3. 조건문2 - 동일 아이디 확인
        # 동일 아이디가 존재한다면, fail msg return
        chk_id = list(db.users.find({'user_id': id_receive}))
        print(chk_id)
        if chk_id != []:
            return jsonify({'response': 'failed_id_check','msg': '동일한 아이디가 이미 존재합니다'})
        # 동일 아이디가 존재하지 않는다면, 조건문3 이동
        else:
            # 4. 조건문3 - 비밀번호 일치 여부 확인
            # 비밀번호와 비밀번호 확인이 일치하지 않는다면, fail msg return
            if pwd_receive != pwd2_receive:
                return jsonify({'response': 'failed_pwd_check','msg': '비밀번호가 일치하지 않습니다'})
            # 비밀번호와 비밀번호 확인이 일치한다면, 조건문4 이동
            else:
                # 5. 조건문4 - 동일 닉네임 확인
                # 동일 닉네임이 존재한다면, fail msg return
                chk_nickname = list(db.users.find(
                    {'user_nickname': nickname_receive}))
                if chk_nickname != []:
                    return jsonify({'response': 'failed_nickname_check','msg': '동일한 닉네임이 이미 존재합니다'})
                # 동일 닉네임이 존재하지 않는다면, 처리작업 수행
                else:
                    # 처리1 - 사용자 비밀번호 암호화(bcrypt)
                    pw_hash = bcrypt.generate_password_hash(pwd_receive)
                    # 처리2 - users 데이터베이스에 요청 정보 삽입
                    insert_doc = [
                        {
                            'user_id': id_receive,
                            'user_pwd': pw_hash,
                            'user_nickname': nickname_receive
                        }
                    ]
                    db.users.insert_many(insert_doc)
                    # 처리3 - 리턴 jsonify
                    return jsonify({'response': 'success','msg': '회원가입에 성공하였습니다!'})


# 레시피 상세페이지
@app.route('/detail')
def render_detail():
    return render_template('detail.html')


# 상세페이지 - 상세 레시피 데이터 출력 api
# list페이지에서 해당card를 클릭하면 get요청으로 해당레시피이름이 url을 통해 넘어와
@app.route('/detail/recipe-detail', methods=['GET'])
def recipe_detail():
    recipe_name_receive = request.args.get('recipe_name')
    # print(recipe_name_receive)
    target_recipe = db.recipes.find_one({'recipe_name': recipe_name_receive})
    target_recipe['_id'] = str(target_recipe['_id'])
    print(target_recipe)
    return jsonify({'target_recipe': target_recipe})


# 상세페이지 리뷰(댓글) 조회 api - 해당 상세레시피에 달린 리뷰(댓글)
@app.route('/detail/review-list', methods=['GET'])
def review_list():
    recipe_name_receive = request.args.get('recipe_name')
    # print(recipe_name_receive)
    reviews = objectIdDecoder(list(db.reviews.find({'recipe_name': recipe_name_receive})))
    # print(reviews)
    return jsonify({'reviews': reviews})


# object값을 str로 바꾸는 함수
def objectIdDecoder(list):
    results = []
    for document in list:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results


# 리뷰(댓글) 작성 api
@app.route('/detail/review-post', methods=['POST'])
def review_post():
    session['user_id'] = 'admin@gmail.com'
    if 'user_id' in session:
        user_nickname_receive = request.form['user_nickname_give']
        user_id_receive = session.get('user_id')
        print(user_id_receive)

        review_content_receive = request.form['review_content_give']
        recipe_name_receive = request.form['recipe_name_give']

        today = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        recipe_review_update = today  # 작성날짜

        print(user_nickname_receive, review_content_receive, recipe_name_receive)
        # print(recipe_review_update)

        doc = {
            'user_nickname': user_nickname_receive,
            'user_id': user_id_receive,
            'review_content': review_content_receive,
            'recipe_name': recipe_name_receive,
            'review_update': recipe_review_update
        }
        db.reviews.insert_one(doc)
        return jsonify({'msg': '댓글 작성 완료'})
    else:
        return jsonify({'msg': '로그인 해주세요.'})


# 내가 쓴 후기 페이지
@app.route('/myreview')
def render_myreview():
    return render_template('myreview.html')


# 내가쓴 리뷰(댓글) 조회 api
@app.route('/myreview/list', methods=['GET'])
def myreview_list():
    if 'user_id' in session:
        get_user_id = session.get('user_id')
        reviews = objectIdDecoder(list(db.reviews.find({'user_id': get_user_id})))
        return jsonify({'reviews': reviews})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 리뷰(댓글) 수정 api
@app.route('/myreview/update', methods=['POST'])
def myreview_update():
    session['user_id'] = 'qqqqqq'
    if 'user_id' in session:
        idx_receive = request.form['idx_give']
        data = db.reviews.find_one({"_id": ObjectId(idx_receive)})
        print(data)

        update_content_receive = request.form['review_content_give']  # 수정된 리뷰값
        # print(update_content_receive)

        # 댓글작성한아이디랑 세션에있는 아이디가 일치하는지 검증 - 로그인 기능 완성후 검증
        if session.get("user_id") == data.get('user_id'):
            db.reviews.update_one({"_id": ObjectId(idx_receive)}, {'$set': {'review_content': update_content_receive}})
            return jsonify({'msg': '댓글 수정 완료'})
        else:
            return jsonify({'msg': '댓글 수정 권한이 없습니다.'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 리뷰(댓글) 삭제 api
@app.route('/myreview/delete', methods=['POST'])
def myreview_delete():
    if 'user_id' in session:
        idx_receive = request.form['idx_give']
        data = db.reviews.find_one({"_id": ObjectId(idx_receive)})
        # print(data)

        if session.get("user_id") == data.get('user_id'):
            db.reviews.delete_one({"_id": ObjectId(idx_receive)})
            return jsonify({'msg': '댓글이 삭제되었습니다.'})
        else:
            return jsonify({'msg': '댓글 삭제 권한이 없습니다.'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 레시피 페이지 API
# 즐겨찾기 추가 API
@app.route('/detail/bookmark', methods=['POST'])
def detail_add_bookmark():
    # 페이크 리턴 값
    return jsonify({'msg': '즐겨찾기를 등록하였습니다.'})


# 나만의 레시피 작성 페이지
@app.route('/write')
def render_write():
    return render_template('write.html')


# 나만의 레시피 작성 api
@app.route('/write', methods=['POST'])
def myrecipe_write():
    if 'user_id' in session:
        myrecipe_title_receive = request.form['myrecipe_title_give']
        myrecipe_diff_receive = request.form['myrecipe_diff_give']
        myrecipe_time_receive = request.form['myrecipe_time_give']
        myrecipe_ing_receive = request.form['myrecipe_ing_give']
        myrecipe_detail_receive = request.form['myrecipe_detail_give']
        # print(myrecipe_title_receive,myrecipe_diff_receive, myrecipe_time_receive,myrecipe_ing_receive,myrecipe_detail_receive )


        myrecipe_user_id_receive = session.get('user_id')  # 세션에서 가져와
        # print(myrecipe_writter_receive)

        myrecipe_user_id_receive = session.get('user_id') # 세션에서 가져와
        # print(myrecipe_user_id_receive)


        # 이미지 업로드 기능
        myrecipe_img_receive = request.files['myrecipe_img_give']  # 이미지파일
        # print(myrecipe_img_receive)

        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  # 날짜- 파일 이름이 중복일경우를 위해
        temp_filename = myrecipe_img_receive.filename
        img_filename = f'{mytime}-{temp_filename}' # 최종 저장되는 이미지파일이름
        # print(img_filename)

        # 배포시 경로 변경예정
        save_to = 'static/myrecipe_img/{}'.format(img_filename)
        myrecipe_img_receive.save(save_to)

        # db저장
        doc = {
            'myrecipe_title': myrecipe_title_receive,
            'myrecipe_img': img_filename,
            'user_id': myrecipe_user_id_receive,
            'myrecipe_diff': myrecipe_diff_receive,
            'myrecipe_time': myrecipe_time_receive,
            'myrecipe_ing': myrecipe_ing_receive,
            'myrecipe_detail': myrecipe_detail_receive
        }
        db.myrecipes.insert_one(doc)
        return jsonify({'msg': '나만의 레시피 작성 완료'})
    else:
        return jsonify({'msg': '로그인 해주세요'})


# 나만의 레시피 조회 페이지
@app.route('/myrecipe')
def render_myrecipe():
    return render_template('myrecipe.html')


# 나만의레시피 수정 API
@app.route('/myrecipe/update', methods=['POST'])
def myrecipe_update():
    if 'user_id' in session:

        idx = request.form['idx']
        data = db.myrecipes.find_one({"_id": ObjectId(idx)})

        idx_receive = request.form['idx_give']
        data = db.myrecipes.find_one({"_id" : ObjectId(idx_receive)})

        # print(data)

        if session.get("user_id") == data.get('user_id'):
            update_title_receive = request.form['myrecipe_title_give']
            update_diff_receive = request.form['myrecipe_diff_give']
            update_time_receive = request.form['myrecipe_time_give']
            update_ing_receive = request.form['myrecipe_ing_give']
            update_detail_receive = request.form['myrecipe_detail_give']


            # 이미지파일 추가업데이트

            # 이전 이미지파일 삭제 부분
            delete_img = data.get('myrecipe_img')
            # print(delete_img)
            # 이미지삭제경로 -
            path = 'static/myrecipe_img/{}'.format(delete_img)
            if os.path.isfile(delete_img):
                os.remove(path)

            #이미지파일 추가 업데이트

            update_img_receive = request.files['myrecipe_img_give']  # 이미지파일
            today = datetime.now()
            mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  # 날짜- 파일이름이 중복일경우를 위해
            temp_filename = update_img_receive.filename
            img_filename = f'{mytime}-{temp_filename}'  # 최종 저장되는 이미지파일이름
            # print(img_filename)


            # 이전 이미지데이터 삭제 부분 - 미완성
            # delete_img =
            # data.get('myrecipe_img')
            # delete_to =

            save_to = 'static/myrecipe_img/{}-{}'.format(mytime, img_filename)
            update_img_receive.save(save_to)

            db.myrecipes.update_one({"_id": ObjectId(idx)}, {
                '$set': {
                    'myrecipe_title': update_title_receive,
                    'myrecipe_img': img_filename,
                    'myrecipe_diff': update_diff_receive,
                    'myrecipe_time': update_time_receive,
                    'myrecipe_ing': update_ing_receive,
                    'myrecipe_detail': update_detail_receive
                }
            })

            # 배포시 경로 변경될수도
            save_to = 'static/myrecipe_img/{}'.format(img_filename)
            update_img_receive.save(save_to)


            db.myrecipes.update_one({"_id": ObjectId(idx_receive)}, {
                                      '$set': {
                                            'myrecipe_title': update_title_receive,
                                            'myrecipe_img': img_filename,
                                            'myrecipe_diff': update_diff_receive,
                                            'myrecipe_time': update_time_receive,
                                            'myrecipe_ing': update_ing_receive,
                                            'myrecipe_detail': update_detail_receive
                                        }
                                    })

            return jsonify({'msg': '나만의 레시피가 수정되었습니다.'})
        else:
            return jsonify({'msg': '수정 권한이 없습니다.'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 나만의 레시피 삭제 API
@app.route('/myrecipe/delete', methods=['POST'])
def myrecipe_delete():
    if 'user_id' in session:
        idx_receive = request.form['idx_give']
        data = db.myrecipes.find_one({"_id": ObjectId(idx_receive)})

        if session.get("user_id") == data.get('user_id'):

            # 이미지파일 삭제
            delete_img = data.get('myrecipe_img')
            # print(delete_img)
            # 이미지삭제경로
            path = 'static/myrecipe_img/{}'.format(delete_img)
            if os.path.isfile(delete_img):
                os.remove(path)

            # db삭제
            db.myrecipes.delete_one({"_id": ObjectId(idx_receive)})
            return jsonify({'msg': '나만의 레시피가 삭제되었습니다'})
        else:
            return jsonify({'msg': ' 수정 권한이 없습니다.'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 나만의 레시피 조회 리스트 API
@app.route('/myrecipe/list', methods=['GET'])
def myrecipe_list():
    if 'user_id' in session:
        get_user_id = session.get('user_id')
        # print(get_user_id)
        myrecipes = objectIdDecoder(list(db.myrecipes.find({'user_id': get_user_id})))

        return jsonify({'myrecipes': myrecipes})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 마이 페이지
@app.route('/mypage/user', methods=['GET'])
def mypage_get():
    session['user_id'] = 'ggoooood'
    if 'user_id' in session:
        get_user_id = session.get('user_id')
        print(get_user_id)
        mypage = list(db.users.find({'user_id': get_user_id}, {'_id': False, 'user_pwd': False}))
        myrecipes = list(db.myrecipes.find({'user_id': get_user_id}, {'_id': False}))
        return jsonify({'mypage': mypage}, {'myrecipes': myrecipes})
    else:
        print(session)
        return jsonify({'msg': '로그인해주세요'})

# 오늘의 레시피
@app.route('/random', methods=['GET'])
def random_recipe():
    import random
    # 설계
    # 1. 랜덤 변수 선언
    random = random.randrange(1, 11)

    # 2. 추천순으로 정렬된 데이터 가져오기
    db_find = list(db.recipes.find({}, {'_id': False}).sort('recipe_like', -1))

    # 3. 랜덤변수 순번 데이터 출력
    random_value = db_find[random - 1]

    # 4. 오늘 변수 설정
    now = datetime.now()

    # 5. 24시 설정
    hour = timedelta(hours=24)

    # sec = timedelta(seconds=10)

    # 6. 남은시간
    time_result = hour - now

    # 7 . 초로 변경
    time_sec = time_result.total_seconds()
    # sec = sec.total_seconds()

    # 8. 반복출력
    print(now, " 현재 시각" + " 10 초 반복 설정")
    threading.Timer(time_sec, random_recipe).start()

    return jsonify({'random_value': random_value})


# localhost:5000 으로 들어갈 수 있게 해주는 코드
if __name__ == '__main__':



    app.run('0.0.0.0', port=5000, debug=True)