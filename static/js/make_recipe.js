
        function logo() {
            onclick = window.location.reload();
        }

        function recipe_create() {
            let myrecipe_title = $('#title').val();
            let myrecipe_diff = $('#diff').val();
            let myrecipe_time1 = $('#time1').val();
            let myrecipe_time2 = $('#time2').val();
            let  myrecipe_detail = $('#detail').val();
            let  myrecipe_ing = $('#ing').val();
            let myrecipe_img = $('#file_upload')[0].files[0];

            let myrecipe_time = myrecipe_time1 + myrecipe_time2

            let form_data = new FormData()
            form_data.append("myrecipe_title_give", myrecipe_title)
            form_data.append("myrecipe_writter_give", myrecipe_writter)
            form_data.append("myrecipe_diff_give", myrecipe_diff)
            form_data.append("myrecipe_time_give", myrecipe_time)
            form_data.append("myrecipe_ing_give", myrecipe_ing)
            form_data.append("myrecipe_detail_give", myrecipe_detail)
            form_data.append("myrecipe_img_give", myrecipe_img)

             $.ajax({
                type: 'POST',
                url: '/write',
                data: form_data,
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    alert(response['msg']);
                    window.location.href = "/";
                }
            });
        }
        //
        // $(document).ready(function() {
	    //     var i=1; // 변수설정은 함수의 바깥에 설정!
        //     $('#order-add').click(function() {
        //         $("#recipe-order").append("<p class='original'>등장"+i+"</p>");
        //         i++; // 함수 내 하단에 증가문 설정
        //     });
        // });
        //
        // $(document).ready(function() {
	    //     var i=1; // 변수설정은 함수의 바깥에 설정!
        //     $('#ing-add').click(function() {
        //         $("#recipe-ing").append("<p class='original'>등장"+i+"</p>");
        //         i++; // 함수 내 하단에 증가문 설정
        //     });
        // });

        function ing_add(){
        // pre_set 에 있는 내용을 읽어와서 처리..
        var div = document.createElement('div');
        div.innerHTML = document.getElementById('recipe-ing-input').innerHTML;
        document.getElementById('recipe-ing-add').appendChild(div);

        }

        function order_add(){
        // pre_set 에 있는 내용을 읽어와서 처리..
        var div = document.createElement('div');
        div.innerHTML = document.getElementById('recipe-order-input').innerHTML;
        document.getElementById('recipe-add-add').appendChild(div);

        }