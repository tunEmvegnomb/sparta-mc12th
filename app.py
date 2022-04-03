# flask 프레임워크 임포트.
# render_template(페이지 이동), jsonify(json값 리턴), request(클라이언트 값 받기), session(로그인) 라이브러리 임포트
from flask import Flask, render_template, jsonify, request, session

# 암호화 라이브러리 bcrypy import. 오류가 뜬다면 interpreter에서 bcrypy 패키지 install
# 그래도 오류가 뜬다면 terminal에서 pip install flask-bcrypt 입력
from flask_bcrypt import Bcrypt

# MongoClient(몽고DB 관리 라이브러리) 임포트
from pymongo import MongoClient

# 클라이언트 정의 - MongoClient를 로컬호스트와 연결
client = MongoClient('mongodb+srv://making:making@cluster0.ymxju.mongodb.net/Cluster0?retryWrites=true&w=majority')
# client = MongoClient('localhost',27017)



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
@app.route('/')
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
        top3_db = db.recipes.find({'recipe_post_update': {'$regex': year_receive}}, {'_id': False})
        top3_db = list(top3_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(3))
    # 값이 만약 월간이라면
    elif click_receive == "월간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        top3_db = db.recipes.find({'recipe_post_update': {'$regex': month_receive}}, {'_id': False})
        top3_db = list(top3_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(3))
    # 값이 만약 일간이라면
    elif click_receive == "일간":
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬
        top3_db = db.recipes.find({'recipe_post_update': {'$regex': day_receive}}, {'_id': False})
        top3_db = list(top3_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(3))

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
# 추천순 정렬 API


@app.route('/list/order_like', methods=['GET'])
def list_order_like():
    # 페이크 값 리턴
    order_like = list(db.recipes.find({}, {'_id': False}))
    return jsonify({'append_data': order_like})

# 리스트 페이지 API
# 최신순 정렬 API


@app.route('/list/order_date', methods=['GET'])
def list_order_date():
    # 페이크 값 리턴
    order_date = list(db.recipes.find({}, {'_id': False}))
    return jsonify({'append_data': order_date})

# 리스트 페이지 API
# 리스트 필터 API


@app.route('/list/filter', methods=['GET'])
def list_filter():
    # 페이크 값 리턴
    filtered_data = list(db.recipes.find({}, {'_id': False}).limit(18))
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

#리퀘스트 변수로 받기 #


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

    print(year_receive,month_receive,day_receive)

    # 3. 조건문1 - 클릭 리시브 확인
    # 값이 만약 연간이라면
    if click_receive == "연간" :
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        find_db = db.recipes.find({'recipe_post_update':{'$regex': year_receive}},{'_id':False})
        find_db = list(find_db.sort('recipe_post_update',-1).sort('recipe_like',-1).limit(10))
    # 값이 만약 월간이라면
    elif click_receive == "월간" :
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬, 10개 제한
        find_db = db.recipes.find({'recipe_post_update': {'$regex': month_receive}},{'_id':False})
        find_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(10))
    # 값이 만약 일간이라면
    elif click_receive == "일간" :
        # 날짜 리시브와 부분 일치하는 데이터베이스 찾아오기, (1)작성 업데이트 날짜-(2)추천 수를 기준으로 정렬
        find_db = db.recipes.find({'recipe_post_update': {'$regex': day_receive}},{'_id':False})
        find_db = list(find_db.sort('recipe_post_update', -1).sort('recipe_like', -1).limit(10))

    return jsonify({'filtered_data': find_db})




# 마이 페이지
@app.route('/mypage', methods=['GET'])
def render_mypage():
    if session is not None:
        user_id = "admin"  # 추후 로그인 세션값으로 변경
        mypage = list(db.users.find({'user_id': user_id}, {'_id': False}))
        return jsonify({'mypage': mypage})


# 즐겨찾기 조회 페이지
@app.route('/mylike')
def render_mylike():
    return render_template('mylike.html')
#
#
# # 나만의 레시피 조회 페이지
# @app.route('/myrecipe')
# def render_myrecipe():
#     return render_template('myrecipe.html')


# 내가 쓴 후기 페이지
@app.route('/myreview')
def render_myreview():
    return render_template('myreview.html')

# 나만의 레시피 조회 페이지
@app.route('/myrecipe')
def render_myrecipe():
    return render_template('myrecipe.html')


# 로그인 페이지
@app.route('/login')
def render_login():
    return render_template('login.html')



# 로그인 페이지 API
# 로그인 체크
@app.route('/login', methods=['POST'])
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
    if (id_receive, pwd_receive) is None :
        return jsonify({'msg' : '정보를 빠짐없이 입력해주세요'})
    else:
        # 3. 아이디, 비밀번호 조회
        # 데이터베이스에서 아이디에 일치하는 데이터 찾기
        find_db = list(db.users.find({'user_id': id_receive},{'_id':False}))

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
                pwd_check = bcrypt.check_password_hash(pw_hash, pwd_receive)    # True, False 리턴
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
        return jsonify({'msg': '입력되지 않은 정보가 존재합니다'})
    # 데이터가 모두 입력되어 있다면, 조건문2 이동
    else:
        # 3. 조건문2 - 동일 아이디 확인
        # 동일 아이디가 존재한다면, fail msg return
        chk_id = list(db.users.find({'user_id': id_receive}))
        print(chk_id)
        if chk_id != []:
            return jsonify({'msg': '동일한 아이디가 이미 존재합니다'})
        # 동일 아이디가 존재하지 않는다면, 조건문3 이동
        else:
            # 4. 조건문3 - 비밀번호 일치 여부 확인
            # 비밀번호와 비밀번호 확인이 일치하지 않는다면, fail msg return
            if pwd_receive != pwd2_receive:
                return jsonify({'msg': '비밀번호가 일치하지 않습니다'})
            # 비밀번호와 비밀번호 확인이 일치한다면, 조건문4 이동
            else:
                # 5. 조건문4 - 동일 닉네임 확인
                # 동일 닉네임이 존재한다면, fail msg return
                chk_nickname = list(db.users.find(
                    {'user_nickname': nickname_receive}))
                if chk_nickname != []:
                    return jsonify({'msg': '동일한 닉네임이 이미 존재합니다'})
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
                    return jsonify({'msg': '회원가입에 성공하였습니다!'})


# 레시피 상세페이지
@app.route('/detail')
def render_detail():
    return render_template('detail.html')

# 상세페이지 - 상세 레시피 데이터 출력 api
# list페이지에서 해당card를 클릭하면 get요청으로 해당레시피이름이 url을 통해 넘어와


@app.route('/detail/recipe-detail', methods=['GET'])
def recipe_detail():
    recipe_name_receive = request.args.get('name')
    print(recipe_name_receive)
    target_recipe = db.recipes.find_one(
        {'recipe_name': recipe_name_receive}, {'_id': False})
    print(target_recipe)

    return jsonify({'target_recipe': target_recipe})

# 리뷰(댓글) api - create 기능


@app.route('/detail/review-post', methods=['POST'])
def review_post():
    if 'user_id' in session:
        user_nickname_receive = request.form['user_nickname_give']
        review_content_receive = request.form['review_content_give']
        recipe_name_receive = request.form['recipe_name_give']
        print(user_nickname_receive, review_content_receive, recipe_name_receive)

        doc = {
            'user_nickname': user_nickname_receive,
            'review_content': review_content_receive,
            'recipe_name': recipe_name_receive
        }
        db.reviews.insert_one(doc)
        return jsonify({'msg': '댓글 작성 완료'})
    else:
        return jsonify({'msg': '로그인해주세요'})

# 리뷰(댓글) api - list기능


@app.route('/detail/review-list', methods=['GET'])
def review_list():
    recipe_name_receive = request.args.get('recipe_name_give')
    # print(recipe_name_receive)
    reviews = list(db.reviews.find(
        {'recipe_name': recipe_name_receive}, {'_id': False}))
    return jsonify({'reviews': reviews})

# 리뷰(댓글) api - update 기능


@app.route('/detail/review-update', methods=['POST'])
def review_update():
    if 'user_id' in session:
        # user식별하기위한값
        user_nickname_receive = request.form['user_nickname_give']
        # 해당 레시피를 식별하기위한값
        recipe_name_receive = request.form['recipe_name_give']
        update_content_receive = request.form['review_content_give']  # 수정된 리뷰값

        db.reviews.update_one({'user_nickname': user_nickname_receive, 'recipe_name': recipe_name_receive},
                              {'$set': {'review_content': update_content_receive}})
        return jsonify({'POST': '댓글 수정 완료'})
    else:
        return jsonify({'msg': '로그인해주세요'})

# 리뷰(댓글) api - 삭제 기능


@app.route('/detail/review-delete', methods=['POST'])
def review_delete():
    if 'user_id' in session:
        # user를 식별하기위한 값
        user_nickname_receive = request.form['user_nickname_give']
        # 해당 레시피를 식별하기위한 값
        recipe_name_receive = request.form['recipe_name_give']
        db.reviews.delete_one(
            {'user_nickname': user_nickname_receive, 'recipe_name': recipe_name_receive})
        return jsonify({'msg': '댓글이 삭제되었습니다'})
    else:
        return jsonify({'msg': '로그인해주세요'})

# 레시피 페이지 API
# 즐겨찾기 추가 API


@app.route('/detail/bookmark', methods=['POST'])
def detail_add_bookmark():
    # 페이크 리턴 값
    return jsonify({'msg': '즐겨찾기를 등록하였습니다.'})

# 상세페이지 - 상세 레시피 데이터 출력
# list페이지에서 해당card를 클릭하면 get요청으로 해당레시피이름이 url을 통해 넘어와


# @app.route('/detail/recipe-detail', methods=['GET'])
# def recipe_detail():
#     recipe_name_receive = request.args.get('name')
#     print(recipe_name_receive)
#     target_recipe = db.recipes.find_one(
#         {'recipe_name': recipe_name_receive}, {'_id': False})
#     print(target_recipe)


# 나만의 레시피 작성 페이지
@app.route('/write')
def render_write():
    return render_template('write.html')

# 나만의 레시피 api - 작성 기능


@app.route('/write', methods=['POST'])
def myrecipe_write():
    if 'user_id' in session:
        myrecipe_title_receive = request.form['myrecipe_title_give']
        # 사용자 id를 받아와야할듯..
        myrecipe_writter_receive = request.form['myrecipe_writter_give']
        myrecipe_diff_receive = request.form['myrecipe_diff_give']
        myrecipe_time_receive = request.form['myrecipe_time_give']
        myrecipe_ing_receive = request.form['myrecipe_ing_give']
        myrecipe_detail_receive = request.form['myrecipe_detail_give']

        # print(myrecipe_title_receive, myrecipe_writter_receive,myrecipe_diff_receive, myrecipe_time_receive,myrecipe_ing_receive,myrecipe_detail_receive )

        # 이미지 파일 업로딩 관련부분 - 보완필요
        myrecipe_img_receive = request.files['myrecipe_img_give']  # 이미지파일
        # print(myrecipe_img_receive)
        img_filename = myrecipe_img_receive.filename
        # filename = f'{today}---{_filename}'
        # extension = myrecipe_img_receive.filename.split('.')[-1]
        # print(filename, extension)
        save_to = 'static/myrecipe_img/{}'.format(img_filename)
        myrecipe_img_receive.save(save_to)

        # db저장
        doc = {
            'myrecipe_title': myrecipe_title_receive,
            'myrecipe_img': img_filename,
            'myrecipe_writter': myrecipe_writter_receive,
            'myrecipe_diff': myrecipe_diff_receive,
            'myrecipe_time': myrecipe_time_receive,
            'myrecipe_ing': myrecipe_ing_receive,
            'myrecipe_detail': myrecipe_detail_receive
        }
        db.myrecipes.insert_one(doc)
        return jsonify({'msg': '나만의 레시피 작성 완료'})
    else:
        return jsonify({'msg': '로그인 해주세요'})

# 나만의레시피 작성 페이지 API
# 나만의레시피 수정 API


@app.route('/write/update', methods=['UPDATE'])
def write_update():
    # 페이크 리턴 값
    return jsonify({'msg': '나만의레시피가 수정되었습니다.'})

# 나만의레시피 작성 페이지 API
# 나만의레시피 이미지 업로드 API


@app.route('/write/upload', methods=['POST'])
def write_img_upload():
    # 페이크 리턴 값
    return jsonify({'msg': '이미지를 업로드했습니다.'})


# localhost:5000 으로 들어갈 수 있게 해주는 코드
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
