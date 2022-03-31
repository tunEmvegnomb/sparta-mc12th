

const likeBtn = document.querySelector(".like-icon")
//좋아요 처음 누르면 +1, 다시 누르면 -1
function onLike(event) {
    const parent = event.target.parentElement.parentElement;
    let likeNum = parent.querySelector(".like-num")
    if (likeBtn.classList.contains("liked")) {
        likeNum.innerText = parseInt(likeNum.innerText) - 1
        likeBtn.classList.remove("liked")
    } else {
        likeNum.innerText = parseInt(likeNum.innerText) + 1
        likeBtn.classList.add("liked")
    }
}

likeBtn.addEventListener("click", onLike);






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

// 스크롤이 맨 밑까지 갈때 실행 되는 조건문
function onScroll() {
    if ($(window).scrollTop() - ($(document).height()-$(window).height()) >= -1) {
        console.log("load more!")  //여기에 ajax 코드 작성
    } 
 }

window.addEventListener("scroll",onScroll)






