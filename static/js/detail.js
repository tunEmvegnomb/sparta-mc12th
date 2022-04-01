$(document).ready(function(){

    $('ul.tabs li').click(function(){
    let tab_id = $(this).attr('data-tab');

    $('ul.tabs li').removeClass('current');
    $('.tabContent').removeClass('current');

    $(this).addClass('current');
    $("#"+tab_id).addClass('current');
    })

    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get("recipe_name");
    console.log(name)

    $.ajax({
        type: "GET",
        url: `/detail/recipe-detail?name=${name}`,
        data: {},
        success: function (response) {
            console.log(response)
            console.log(response['recipe'])
        }
    })





})
