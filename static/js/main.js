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
    if(onclick(month)){
            function month() {
        $.ajax({
            type: 'GET',
            url: '/main',
            data: {},
            success: function (response) {


            }
        })
    }

    }
