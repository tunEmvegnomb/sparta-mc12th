$(document).ready(function(){

  $('ul.tabs li').click(function(){
    let tab_id = $(this).attr('data-tab');

    $('ul.tabs li').removeClass('current');
    $('.listWrap').removeClass('current');

    $(this).addClass('current');
    $("#"+tab_id).addClass('current');
  })

})