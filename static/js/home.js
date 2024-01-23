$(document).ready(function () {
    PopUpHide();
});

function finishButtonClick() {
    var user_id = {{ user_id|tojson|safe }};
    var snipe_id = $("#popup1").data("snipe_id");  // Retrieve snipe_id from the data attribute
    console.log(user_id);
    console.log(snipe_id);

    $.ajax({
        type: "POST",
        url: "{{ url_for('takeout_goods') }}",
        data: {
            snipe_id: snipe_id,
            user_id: user_id
        },
        success: function (response) {
            console.log(response); // Log the response from the server
            // Handle the response as needed (e.g., redirect to /takeout)
            window.location.href = "/takeout";
        },
        error: function (error) {
            console.error("Error:", error);
        }
    });

    PopUpHide(); // Close the popup if needed
};

function cancelButtonClick() {
    // Handle the logic when the "Cancel" button is clicked
    console.log("Cancel button clicked");
    // You can add your logic here
    PopUpHide(); // Close the popup if needed
}

function PopUpShow(snipe_id, message) {
    $("#popupMessage").text(message);
    $("#popup1").data("snipe_id", snipe_id);  // Store snipe_id in the data attribute
    $("#popup1, #overlay").show();
}

function PopUpHide() {
    $("#popup1, #overlay").hide();
}

function checkAndPopUpShow(cell) {
    var cellText = $(cell).find("td").text().trim();
    var snipe_id = $(cell).data("snipe_id");  // Retrieve snipe_id from the data attribute
    var title = $(cell).find("td strong").text().trim();

    if (cellText == "Cell is Empty" || cellText == "Goods is None") {
        PopUpShow(null, "This cell is empty.");
    } else {
        PopUpShow(snipe_id, "Title: " + title);
    }
}