// Fetch annual sales and profits data for the bar chart
$.ajax({
    url: "/api/annual-sales-profits/",  // Adjust the URL to match your route
    method: "GET",
    success: function(data) {
        var ctx1 = $("#salse-revenue").get(0).getContext("2d");
        var myChart1 = new Chart(ctx1, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Sales",
                        data: data.salesData,
                        backgroundColor: "rgba(235, 22, 22, .7)"
                    },
                    {
                        label: "Profits",
                        data: data.profitsData,
                        backgroundColor: "rgba(235, 22, 22, .5)"
                    }
                ]
            },
            options: {
                responsive: true
            }
        });
    },
    error: function(xhr, status, error) {
        console.error("Error fetching annual sales and profits:", error);
    }
});

// Fetch monthly sales and profits data for the line chart
$.ajax({
    url: "/api/monthly-sales-profits/",
    method: "GET",
    success: function(data) {
        var ctx2 = $("#worldwide-sales").get(0).getContext("2d");
        var myChart2 = new Chart(ctx2, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Sales",
                        data: data.salesData,
                        backgroundColor: "rgba(235, 22, 22, .7)",
                        borderColor: "rgba(235, 22, 22, .7)",
                        fill: true
                    },
                    {
                        label: "Profits",
                        data: data.profitsData,
                        backgroundColor: "rgba(235, 22, 22, .5)",
                        borderColor: "rgba(235, 22, 22, .5)",
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true
            }
        });
    },
    error: function(xhr, status, error) {
        console.error("Error fetching monthly sales and profits:", error);
    }
});
