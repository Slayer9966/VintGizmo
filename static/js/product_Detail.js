$(document).ready(function() {
$(".AddImage").click(function () {
    const productId = $(this).data("id");
    const url = `/get/variation/${productId}/`;
    $.ajax({
      url: url,
      method: "GET",
      success: function (data) {
        $("#product_image_id").val(data.id);

        $("#ImageModal").modal("show");
      },
      error: function () {
        alert("Failed to retrieve product data.");
      },
    });
  });
  // for preview of images of product in imagemodal
  document
    .getElementById("formFile")
    .addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          const imagePreview = document.getElementById("imagePreview");
          imagePreview.src = e.target.result;
          imagePreview.style.display = "block"; // Show the image preview
        };
        reader.readAsDataURL(file);
      } else {
        document.getElementById("imagePreview").style.display = "none"; // Hide the image preview if no file is selected
      }
    });
var searchInput = document.getElementById("searchInput");
if (searchInput) {
  searchInput.addEventListener("keyup", function () {
    var input = this.value.toLowerCase();
    var tableRows = document.querySelectorAll("#tableBody tr");

    tableRows.forEach(function (row) {
      var rowText = row.textContent.toLowerCase();
      if (rowText.includes(input)) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  });
}
$(".del").click(function () {
  $("#exampleModalUpdate").modal("hide");
});
$(".open").click(function () {
   
   console.log("hello")
    $("#exampleModal").modal("show");
  });
  $(".close_add").click(function () {
    console.log("hjello")
    $("#exampleModal").modal("hide");
  });
  $(".cl_i").click(function () {
    $("#ImageModal").modal("hide");
  });
  $(".update").click(async function () {
    const productId = $(this).data("id");
    const url = `/get/variation/${productId}/`;

    $.ajax({
      url: url,
      method: "GET",
      success: async function (data) {
       

        $("#name").val(data.name);
        $("#quantity").val(data.quantity);
        $("#cost_price").val(data.cost_price);
        $("#sales_price").val(data.sales_price);
        $("#sale_price").val(data.sale_price);
        $("#warranty").val(data.warranty);
        $("#description").val(data.description);
        $("#name").val(data.name);
        
        $("#product_id").val(data.id);

        $("#exampleModalUpdate").modal("show");
      },
      error: function () {
        alert("Failed to retrieve product data.");
      },
    });
  });
 
});
