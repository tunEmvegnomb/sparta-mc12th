function showMypage() {
    $.ajax({
        type: "GET",
        url: "/mypage",
        data: {},
        success: function (response) {
            let mypage = response['mypage']
            let user_id = mypage['user_id']
            let nickname = mypage['user_nickname']
            console.log(user_id, nickname)
        }
    })
}

