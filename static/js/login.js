// 로그인 아이디, 패스워드 입력 불러오기
$(".login-form").on("submit", function(event){
    event.preventDefault()

    let user_id = $("#loginId").val()
    let user_pwd = $("#loginPassword").val()

    $.ajax({
        type: 'POST',
        url: '/login',
        data: {id_give: user_id, pwd_give: user_pwd}, 
        success: function (response) {
            alert(response['msg']);
            // document.location.href = "/"    //메인페이지로 이동
        }
    })

   
})