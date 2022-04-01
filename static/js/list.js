//좋아요 처음 누르면 +1, 다시 누르면 -1
const likeIcon = document.querySelector(".like-icon")
function onLike(event) {
    const parent = event.target.parentElement.parentElement;
    let likeNum = parent.querySelector(".like-num")
    if (likeIcon.classList.contains("liked")) {
        likeNum.innerText = parseInt(likeNum.innerText) - 1
        likeIcon.classList.remove("liked")
    } else {
        likeNum.innerText = parseInt(likeNum.innerText) + 1
        likeIcon.classList.add("liked")
    }
}
likeIcon.addEventListener("click", onLike);


//최신순, 인기순 정렬??




//검색창 입력값 불러오기
$("form").on("submit", function(event){
  event.preventDefault()
  const inputVal = $("#searchInput").val()
  console.log(inputVal)
})


//필터 선택값 불러오기
function onFilterClick(event) {
  const value = event.target.innerText
  const key = event.target.parentElement.id
  console.log(key, value)
}

Array.from($(".filter-value")).forEach(value => value.addEventListener("click", onFilterClick))



//데이터베이스로부터 리스트를 받아와서 카드로 어펜드하는 함수. 12개씩(또는 정해진 개수)불러 오는 방법은 찾아봐야 됨
function showRecipes() {
    $.ajax({
        type: "GET",
        url: "/list",
        data: {},
        success: function (response) {
            let recipes = response['all_Foodlist']
            for (let i = 0; i < recipes.length; i++) {
                let name = recipes[i]['recipe_name']
                let img = recipes[i]['recipe_img']
                let link = recipes[i]['recipe_link']
                let like = recipes[i]['recipe_like']
                let writter = recipes[i]['recipe_writter']
                let temp_html = `<div class="col">
                <div class="card">
                  <div class="card-img-div">
                    <a href="${link}">
                      <img
                        src="${img}"
                        class="card-img-top"
                        alt="..."
                      />
                    </a>
                  </div>
                  <div class="card-body">
                    <div class="card-info">
                      <a href="${link}" class="recipe-link"
                        ><span class="card-title"
                          >${name}</span
                        ></a
                      >
                      <div class="card-bottom-row">
                        <span class="card-text">${writter}</span>
                        <div class="like-div">
                          <span class="like-text">추천</span>
                          <span class="like-num">${like}</span>
                        </div>
                      </div>
                    </div>
                    <div class="card-like">
                      <img src="/static/img/good.png" class="like-icon" />
                    </div>
                  </div>
                </div>
              </div>`
                $('.card-group').append(temp_html)
            }
        }  
    })
}

// 스크롤이 맨 밑까지 가면 실행 되는 조건문
function onScroll() {
    if ($(window).scrollTop() - ($(document).height()-$(window).height()) >= -1) {
        console.log("load more!")  //여기에 ajax 코드 작성
    } 
 }

window.addEventListener("scroll",onScroll)






