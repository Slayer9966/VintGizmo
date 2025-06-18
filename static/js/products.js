document.addEventListener("DOMContentLoaded", function () {
  // Search function for table
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

  // Search function for category items
  document.getElementById("searchInputCategory").addEventListener("keyup", function () {
      let filter = this.value.toLowerCase();
      let items = document.querySelectorAll(
        "#searchableItems .searchable-item"
      );

      console.log("Category Filter:", filter); // Debugging filter value
      items.forEach(function (item) {
        let text = item.textContent.toLowerCase();
        console.log("Item Text:", text); // Debugging item text

        if (text.includes(filter)) {
          item.style.display = ""; // Show the item
          console.log("Item shown:", item);
        } else {
          item.style.display = "none"; // Hide the item
          console.log("Item hidden:", item);
        }
      });
    });

  // Search function for brand items
  document.getElementById("searchInputBrand").addEventListener("keyup", function () {
      let filter = this.value.toLowerCase();
      let items = document.querySelectorAll(
        "#searchableItems1 .searchable-item1"
      );

      console.log("Brand Filter:", filter); // Debugging filter value
      items.forEach(function (item) {
        let text = item.textContent.toLowerCase();
        console.log("Item Text:", text); // Debugging item text

        if (text.includes(filter)) {
          item.style.display = ""; // Show the item
          console.log("Item shown:", item);
        } else {
          item.style.display = "none"; // Hide the item
          console.log("Item hidden:", item);
        }
      });
    });
  // Function to fetch details from a given route
  // Function to fetch details from a given route
  // Function to fetch details from a given route
  // Function to fetch details from a given route
  async function fetchDetails(route) {
    try {
      const response = await fetch(route);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log(`Fetched details from ${route}:`, data);
      return data;
    } catch (error) {
      console.error(`Error fetching details from ${route}:`, error);
    }
  }

  // Function to populate select options with placeholders
  function populateSelectOptions(selectElements, items, selectClass) {
    console.log("Select Class in populateSelectOptions:", selectClass); // Debugging: Log the class name

    selectElements.forEach((select) => {
      console.log("Select Element:", select); // Debugging: Log the select element

      select.innerHTML = ""; // Clear existing options

      // Create placeholder option
      const placeholderOption = document.createElement("option");
      placeholderOption.value = "";
      placeholderOption.disabled = true;
      placeholderOption.selected = true;

      // Set placeholder text based on select class
      if (selectClass === "brandSelect" || selectClass === "brandSelectAdd") {
        placeholderOption.textContent = "Select a Brand";
      } else if (
        selectClass === "CategorySelect" ||
        selectClass === "CategorySelectAdd"
      ) {
        placeholderOption.textContent = "Select a Category";
      } else {
        placeholderOption.textContent = "Select an Option"; // Default for other cases
      }

      select.appendChild(placeholderOption);

      // Add options from items
      items.forEach((item) => {
        const option = document.createElement("option");
        option.value = item.id || ""; // Ensure item.id exists or default to ''
        option.textContent = item.name || "Unknown"; // Ensure item.name exists or default to 'Unknown'
        select.appendChild(option);
        console.log(option.value);
      });
    });
  }

  const choicesInstances = new Map();

async function updateSelect(route, selectClass, selectedValue = null) {
    const items = await fetchDetails(route);
    console.log(selectClass);
    if (items && items.length > 0) {
        const selectElements = document.querySelectorAll(`.${selectClass}`);
        selectElements.forEach((select) => {
            // Check if the Choices instance is already initialized
            if (choicesInstances.has(select)) {
                // Destroy the previous instance
                choicesInstances.get(select).destroy();
                choicesInstances.delete(select);
            }

            // Populate the select options
            populateSelectOptions([select], items, selectClass);

            // Initialize Choices.js on the select element
            const choices = new Choices(select, {
                searchEnabled: true, // Enable search functionality
                shouldSort: false,
                placeholderValue: "Select an option",
                placeholder: true,
                allowHTML: true,
            });

            // Save the Choices instance to the Map
            choicesInstances.set(select, choices);

            // Set the selected option after population
            if (selectedValue !== null) {
                choices.setChoiceByValue(selectedValue.toString());
                console.log(
                    `Set selected value for ${selectClass}: ${selectedValue}`
                );
            }
        });
    } else {
        console.log(`No items found for route ${route}`);
    }
}

  $(".del").click(function () {
    $("#exampleModalUpdate").modal("hide");
  });

  $(".cl_i").click(function () {
    $("#ImageModal").modal("hide");
  });
  $(".open").click(function () {
   
    updateSelect("/getCategories", "CategorySelectAdd", null);
    updateSelect("/getBrands", "brandSelectAdd", null);
    $("#exampleModal").modal("show");
  });
  $(".close_add").click(function () {
    console.log("hjello")
    $("#exampleModal").modal("hide");
  });
  $(".update").click(async function () {
    const productId = $(this).data("id");
    const url = `/product/get/${productId}/`;
    var shipping_cost = $(this).data('shipping');
    $("#shipping_cost").val(shipping_cost)
    $.ajax({
      url: url,
      method: "GET",
      success: async function (data) {
        await updateSelect(
          "/getCategories",
          "CategorySelect",
          data.category_id
        );
        await updateSelect("/getBrands", "brandSelect", data.brand_id);

        $("#name").val(data.name);
        
        $("#product_id").val(data.id);

        $("#exampleModalUpdate").modal("show");
      },
      error: function () {
        alert("Failed to retrieve product data.");
      },
    });
  });

  // for getting data into ImageModal
  
});
