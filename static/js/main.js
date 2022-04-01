$(document).ready(function(){
	  random();
});

function random() {
    $.ajax({
        type: 'GET',
        url: '/main',
        data: {},
        success: function (response) {

        }
    })
}