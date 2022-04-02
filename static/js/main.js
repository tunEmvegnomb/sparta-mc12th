    $(document).ready(function(){
          random();
    });

    function logo() {
            onclick = window.location.reload();
    }

    function random() {
        $.ajax({
            type: 'GET',
            url: '/main',
            data: {},
            success: function (response) {

            }
        })
    }