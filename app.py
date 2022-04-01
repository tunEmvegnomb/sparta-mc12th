# flask 프레임워크 임포트.
# render_template(페이지 이동), jsonify(json값 리턴), request(클라이언트 값 받기), session(로그인) 라이브러리 임포트
from flask import Flask, render_template, jsonify, request, session

# MongoClient(몽고DB 관리 라이브러리) 임포트
from pymongo import MongoClient

# 클라이언트 정의 - MongoClient를 로컬호스트와 연결
client = MongoClient('mongodb+srv://making:making@cluster0.ymxju.mongodb.net/Cluster0?retryWrites=true&w=majority')
# client = MongoClient('localhost',27017)

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


# 테마 페이지
@app.route('/theme')
def render_theme():
    return render_template('theme.html')


# 인기 페이지
@app.route('/rank')
def render_rank():
    return render_template('rank.html')

#리퀘스트 변수로 받기 #
@app.route('/rank/get', methods=['GET'])
def rank():
    year_give = request.args.get('date_year')
    month_give = request.args.get('date_month')
    day_give = request.args.get('date_day')
    click_receive = request.args.get('click_data')
    print(year_give, month_give, day_give, click_receive)

    # 레시피 데이터 베이스 가져오기
    # 데이터베이스에서 상위 10개 가져오기
    recipes = list(db.recipes.find({}, {'_id': False}).sort('recipe_like', -1).limit(10))

    # 반복문 사용(데이터 출력용도)
    for db_recipe in recipes:
        # 날짜값 스플릿
        db_date = db_recipe['recipe_post_update']
        # 스플릿데이터 - 년도
        db_year = db_date.split('-')[0]
        # 스플릿데이터 - 월
        db_month = db_date.split('-')[1]
        # 스플릿데이터 - 일
        db_day = db_date.split('-')[2]

        # 조건문 - 클릭 리시브
        if click_receive == '연간':
            # 년도에 따라 데이터 출력
            if db_year == "2022":
                db_yearlist = db_recipe
                print('연간 데이터 출력 완료!')
                return jsonify({'filtered_data': db_yearlist})


        elif click_receive == '월간':
            if db_month == "03":
                db_monthlist = db_recipe
                print('월간 데이터 출력 완료!')
                return jsonify({'filtered_data': db_monthlist})

        elif click_receive == '일간':
            if db_day == "01":
                db_daylist = db_recipe
                print('일간 데이터 출력 완료!')
                return jsonify({'filtered_data': db_daylist})

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
    #
    # # 조건문2
    # # 달별로 데이터 출력
    # for db_recipe in recipes:
    #     #업데이트 날짜 기준
    #     db_date = db_recipe['recipe_post_update']
    #     #월 스플릿
    #     db_month = db_date.split('-')[1]
    #     #연도 스필릿
    #     db_year = db_date.split('-')[0]
    #     # 같은년도에 해당하는 달에 따라 데이터 출력
    #     if db_month == "05" and db_year == "2023":
    #         db_monthlist = db_recipe
    #         print(db_monthlist)
    #
    # # 조건문3
    # # 일별로 데이터 출력
    # for db_recipe in recipes:
    #     #업데이트 날짜 기준
    #     db_date = db_recipe['recipe_post_update']
    #     #일 스플릿
    #     db_day = db_date.split('-')[2]
    #     #월 스필릿
    #     db_month = db_date.split('-')[1]
    #     #연도 스플릿
    #     db_year = db_date.split('-')[0]
    #     # 같은년도 같은월에 해당하는 일에 따라 데이터 출력
    #     if db_day == "02" and db_month == "03" and db_year == "2023":
    #         db_daylist = db_recipe
    #         print(db_daylist)


# 마이 페이지
@app.route('/mypage', methods=['GET'])
def render_mypage():
    if session is not None:
        user_id = "admin" #추후 로그인 세션값으로 변경
        mypage = list(db.users.find({'user_id': user_id}, {'_id': False}))
        return jsonify({'mypage': mypage})


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
@app.route('/signUp')
def render_signUp():
    return render_template('signup.html')


## API 역할을 하는 부분

# POST
@app.route('/', methods=['POST'])
def name():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'POST'})

# 회원가입

# 로그인

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
    target_recipe = db.recipes.find_one({'recipe_name': recipe_name_receive},{'_id':False})
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
            'recipe_name' : recipe_name_receive
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
    reviews = list(db.reviews.find({'recipe_name' : recipe_name_receive}, {'_id': False}))
    return jsonify({'reviews': reviews})


# 리뷰(댓글) api - update 기능
@app.route('/detail/review-update', methods=['POST'])
def review_update():
    if 'user_id' in session:
        user_nickname_receive = request.form['user_nickname_give'] # user식별하기위한값
        recipe_name_receive = request.form['recipe_name_give'] # 해당 레시피를 식별하기위한값
        update_content_receive = request.form['review_content_give'] # 수정된 리뷰값

        db.reviews.update_one({'user_nickname': user_nickname_receive, 'recipe_name':recipe_name_receive}, {'$set': {'review_content': update_content_receive}})
        return jsonify({'POST': '댓글 수정 완료'})
    else:
        return jsonify({'msg': '로그인해주세요'})


# 리뷰(댓글) api - 삭제 기능
@app.route('/detail/review-delete', methods=['POST'])
def review_delete():
    if 'user_id' in session:
        user_nickname_receive = request.form['user_nickname_give'] # user를 식별하기위한 값
        recipe_name_receive = request.form['recipe_name_give'] # 해당 레시피를 식별하기위한 값
        db.reviews.delete_one({'user_nickname': user_nickname_receive, 'recipe_name': recipe_name_receive})
        return jsonify({'msg': '댓글이 삭제되었습니다'})
    else:
        return jsonify({'msg': '로그인해주세요'})



# 나만의 레시피 작성 페이지
@app.route('/write')
def render_write():
    return render_template('write.html')


# 나만의 레시피 api - 작성 기능
@app.route('/write', methods=['POST'])
def myrecipe_write():
    if 'user_id' in session:
        myrecipe_title_receive = request.form['myrecipe_title_give']
        myrecipe_writter_receive = request.form['myrecipe_writter_give'] # 사용자 id를 받아와야할듯..
        myrecipe_diff_receive = request.form['myrecipe_diff_give']
        myrecipe_time_receive = request.form['myrecipe_time_give']
        myrecipe_ing_receive = request.form['myrecipe_ing_give']
        myrecipe_detail_receive = request.form['myrecipe_detail_give']

        # print(myrecipe_title_receive, myrecipe_writter_receive,myrecipe_diff_receive, myrecipe_time_receive,myrecipe_ing_receive,myrecipe_detail_receive )

        # 이미지 파일 업로딩 관련부분 - 보완필요
        myrecipe_img_receive = request.files['myrecipe_img_give'] # 이미지파일
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
            'myrecipe_writter' : myrecipe_writter_receive,
            'myrecipe_diff' : myrecipe_diff_receive,
            'myrecipe_time' : myrecipe_time_receive,
            'myrecipe_ing' : myrecipe_ing_receive,
            'myrecipe_detail' : myrecipe_detail_receive
        }
        db.myrecipes.insert_one(doc)
        return jsonify({'msg': '나만의 레시피 작성 완료'})
    else:
        return jsonify({'msg': '로그인 해주세요'})







# localhost:5000 으로 들어갈 수 있게 해주는 코드
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)







