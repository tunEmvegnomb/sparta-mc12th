let recipe_name = "";

$(document).ready(function () {
  $(".card-title").click(function () {
    recipe_name = $(this).text()
  })
})

function moveDetail() {
  if (recipe_name !== null) {
    document.location.href = `/detail?recipe_name=${recipe_name}`;
  }
}
