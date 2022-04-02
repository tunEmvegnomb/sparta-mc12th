// 회원가입 ajax 코드
$('.signup-form').on('submit', function(event) {
    event.preventDefault();

    let user_id = $('#id').val()
    let user_pwd = $('#password').val()
    let user_pwd2 = $('#password_check').val()
    let user_nickname = $('#nickname').val()

    $.ajax({
        type: 'POST',
        url: '/signup',
        data: {id_give: user_id, pwd_give: user_pwd, pwd2_give: user_pwd2, nickname_give: user_nickname}, 
        success: function (response) {
            alert(response['msg']);
            document.location.href = "/login" //로그인페이지로 이동
        }
    })
});
