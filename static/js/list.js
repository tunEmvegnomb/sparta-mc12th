// //좋아요 처음 누르면 +1, 다시 누르면 -1
// const likeIcon = document.querySelector(".like-icon")
// function onLike(event) {
//     const parent = event.target.parentElement.parentElement;
//     let likeNum = parent.querySelector(".like-num")
//     if (likeIcon.classList.contains("liked")) {
//         likeNum.innerText = parseInt(likeNum.innerText) - 1
//         likeIcon.classList.remove("liked")
//     } else {
//         likeNum.innerText = parseInt(likeNum.innerText) + 1
//         likeIcon.classList.add("liked")
//     }
// }
// likeIcon.addEventListener("click", onLike);


//최신순 정렬
$(".sortByDate").on("click", function() {
  $.ajax({
    type: "GET",
    url: "/list/order_date",
    data: {},
    success: function (response) {
      $('.card-group').empty();
        let recipes = response['append_data']
        for (let i = 0; i < recipes.length; i++) {
            let name = recipes[i]['recipe_name']
            let img = recipes[i]['recipe_img']
            let like = recipes[i]['recipe_like']
            let writter = recipes[i]['recipe_writter']
            let temp_html = `<div class="col">
            <div class="card">
              <div class="card-img-div">
                  <img
                    src="${img}"
                    class="card-img-top"
                    alt="..."
                  />
              </div>
              <div class="card-body">
                <div class="card-info">
                  <a href="#" class="recipe-link"
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
                  <i class="fa-regular fa-thumbs-up like-icon"></i>
                </div>
              </div>
            </div>
          </div>`
            $('.card-group').append(temp_html)
        }
        $('.spinner-border').hide();
    }  
})
})

//인기순 정렬
$(".sortByLike").on("click", function() {
  $.ajax({
    type: "GET",
    url: "/list/order_like",
    data: {},
    success: function (response) {
      $('.card-group').empty();
        let recipes = response['append_data']
        for (let i = 0; i < recipes.length; i++) {
            let name = recipes[i]['recipe_name']
            let img = recipes[i]['recipe_img']
            let like = recipes[i]['recipe_like']
            let writter = recipes[i]['recipe_writter']
            let temp_html = `<div class="col">
            <div class="card">
              <div class="card-img-div">
                  <img
                    src="${img}"
                    class="card-img-top"
                    alt="..."
                  />
              </div>
              <div class="card-body">
                <div class="card-info">
                  <a href="#" class="recipe-link"
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
                  <i class="fa-regular fa-thumbs-up like-icon"></i>
                </div>
              </div>
            </div>
          </div>`
            $('.card-group').append(temp_html)
        }
        $('.spinner-border').hide();
    }  
})
})


//검색창 입력
$("form").on("submit", function(event){
  event.preventDefault()
  const inputVal = $("#searchInput").val()
  console.log(inputVal)
  $.ajax({
    type: "GET",
    url: "/list/search",
    data: {search_give: inputVal},
    success: function (response) {
      $('.card-group').empty();
        let recipes = response['filtered_data']
        for (let i = 0; i < recipes.length; i++) {
            let name = recipes[i]['recipe_name']
            let img = recipes[i]['recipe_img']
            let like = recipes[i]['recipe_like']
            let writter = recipes[i]['recipe_writter']
            let ing = recipes[i]['recipe_ing']
            let diff = recipes[i]['recipe_diff']
            let taste = recipes[i]['recipe_taste']
            let detail = recipes[i]['recipe_detail']
            let info = name + writter + ing + diff + taste + detail;
            if (info.includes(inputVal)) {
            let temp_html = `<div class="col">
            <div class="card">
              <div class="card-img-div">
                  <img
                    src="${img}"
                    class="card-img-top"
                    alt="..."
                  />
              </div>
              <div class="card-body">
                <div class="card-info">
                  <a href="#" class="recipe-link"
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
                  <i class="fa-regular fa-thumbs-up like-icon"></i>
                </div>
              </div>
            </div>
          </div>`
            $('.card-group').append(temp_html)}
        }
        $('.spinner-border').hide();

    }  
})
})


//필터 선택값 불러오기
function onFilterClick(event) {
  const value = event.target.innerText
  const key = event.target.parentElement.id
  console.log(key, value)
  $.ajax({
    type: "GET",
    url: "/list/filter",
    data: {},
    success: function (response) {
      $('.card-group').empty();
        let recipes = response['filtered_data']
        for (let i = 0; i < recipes.length; i++) {
            let name = recipes[i]['recipe_name']
            let img = recipes[i]['recipe_img']
            let like = recipes[i]['recipe_like']
            let writter = recipes[i]['recipe_writter']
            let temp_html = `<div class="col">
            <div class="card">
              <div class="card-img-div">
                  <img
                    src="${img}"
                    class="card-img-top"
                    alt="..."
                  />
              </div>
              <div class="card-body">
                <div class="card-info">
                  <a href="#" class="recipe-link"
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
                  <i class="fa-regular fa-thumbs-up like-icon"></i>
                </div>
              </div>
            </div>
          </div>`
            $('.card-group').append(temp_html)
        }
    }  
})
}

Array.from($(".filter-value")).forEach(value => value.addEventListener("click", onFilterClick))


//처음 데이터 출력
$(document).ready(function() {
  showRecipes();
})
//처음 데이터 출력
function showRecipes() {
    $.ajax({
        type: "GET",
        url: "/list/data",
        data: {},
        success: function (response) {
            let recipes = response['append_data']
            for (let i = 0; i < recipes.length; i++) {
                let name = recipes[i]['recipe_name']
                let img = recipes[i]['recipe_img']
                let like = recipes[i]['recipe_like']
                let writter = recipes[i]['recipe_writter']
                let temp_html = `<div class="col">
                <div class="card">
                  <div class="card-img-div">
                      <img
                        src="${img}"
                        class="card-img-top"
                        alt="..."
                      />
                  </div>
                  <div class="card-body">
                    <div class="card-info">
                      <a href="#" class="recipe-link"
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
                      <i class="fa-regular fa-thumbs-up like-icon"></i>
                    </div>
                  </div>
                </div>
              </div>`
                $('.card-group').append(temp_html)
  
            }
            
        }  
    })
}



//레시피 이름으로 출력

let recipe_name = "";

$(document).ready(function () {
  $(".card-title").click(function () {
    recipe_name = $(this).text();
  })
})

function moveDetail() {
  if (recipe_name !== null) {
    document.location.href = `/detail?recipe_name=${recipe_name}`;
  }
}


// 스크롤이 맨 밑까지 가면 실행 되는 조건문
function onScroll() {
  if ($(window).scrollTop() - ($(document).height()-$(window).height()) >= -1) {
      console.log("load more!")  //여기에 ajax 코드 작성
  } 
}

window.addEventListener("scroll",onScroll)