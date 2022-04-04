// 회원가입 ajax 코드
// $('.signup-form').on('submit', function(event) {
function signup() {
    event.preventDefault();

     user_id = $('#id').val()
     user_pwd = $('#password').val()
     user_pwd2 = $('#password_check').val()
     user_nickname = $('#nickname').val()
    console.log(user_id, user_pwd, user_pwd2, user_nickname)
    $.ajax({
        type: 'POST',
        url: '/signup',
        data: {user_id: user_id, user_pwd: user_pwd, user_pwd2: user_pwd2, user_nickname: user_nickname},
        success: function (response) {
            alert(response['msg']);
            document.location.href = "/login" //로그인페이지로 이동
        }
    })
}


;
