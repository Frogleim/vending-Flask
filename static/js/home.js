$(document).ready(function () {
    PopUpHide();
});

function finishButtonClick() {
    var user_id = {{ user_id|tojson|safe }};
    var snipe_id = $("#popup1").data("snipe_id");  
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
    console.log(response);
    window.location.href = "/takeout";
},
error: function (jqXHR, textStatus, errorThrown) {
    console.error("Error:", errorThrown);
    window.location.href = "/error";
}
});

    PopUpHide(); 
}

function cancelButtonClick() {
    console.log("Cancel button clicked");
    PopUpHide(); 
}

function PopUpShow(snipe_id, message) {
    $("#popupMessage").text(message);
    $("#popup1").data("snipe_id", snipe_id); 
    $("#popup1, #overlay").show();
}

function PopUpHide() {
    $("#popup1, #overlay").hide();
}

function checkAndPopUpShow(cell) {
    var cellText = $(cell).find("td").text().trim();
    var snipe_id = $(cell).data("snipe_id");  
    console.log(snipe_id);
    var title = $(cell).find(".card-text").text().trim();

    if (cellText == "Cell is Empty" || cellText == "Goods is None") {
        PopUpShow(null, "This cell is empty.");
    } else {
        PopUpShow(snipe_id, title);
    }
}