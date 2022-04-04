    $(document).ready(function(){
          random();
    });

    function logo() {
            onclick = window.location.reload();
    }

    function random() {
        $.ajax({
            type: 'GET',
            url: '/reco',
            data: {},
            success: function (response) {
                alert('reco_data')
            }
        })
    }
    function main_top3() {
        $.ajax({
            type: 'GET',
            url: '/top3',
            data: {},
            success: function (response) {
                let images = response['filtered_data']
                for (let i=0; i<images.length; i++){
                    let image0 = images[0]['recipe_img']
                    let image1 = images[1]['recipe_img']
                    let image2 = images[2]['recipe_img']

                    let temp_html = `<div style="display: flex; justify-content: space-around;">
                    <div>
                        <img src="\\static\\img\\rank-1.png" alt="이미지" class="best-recipe-rank-top"/>
                        <img src="${image0}" alt="이미지"/>
                    </div>
                    <div>
                        <img src="\\static\\img\\rank-2.png" alt="이미지" class="best-recipe-rank-second"/>
                        <img src="${image1}" alt="이미지"/>
                    </div>
                    <div>
                        <img src="\\static\\img\\rank-3.png" alt="이미지" class="best-recipe-rank-third"/>
                        <img src="${image2}" alt="이미지"/>
                    </div>
                </div>`
                    $('#image-card').append(temp_html)
                }

            }
        });
    }
