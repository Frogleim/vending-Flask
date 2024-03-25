window.onload = function() {
    var fioElement = document.getElementById("fio");
    var fioText = fioElement.textContent;
    var fioWords = fioText.split(" ");
    fioElement.innerHTML = fioWords.join("<br>");
};


function deniedButtonClick() {
    // Handle the logic when the "Cancel" button is clicked
    console.log("Cancel button clicked");
    // You can add your logic here
    PopUpHide(); // Close the popup if needed
}

function PopUpShow(snipe_id, message, imgSrc, cell_number) {
    console.log(cell_number);
    $("#device-title").text(message);
    $("#popup1").data("snipe_id", snipe_id);  // Store snipe_id in the data attribute
    $("#popup1, #overlay").show();
    $("#popup1 .popup-image").attr("src", imgSrc); // Set the src attribute of the popup image
    $("#cell_number").val(cell_number);
}

function PopUpHide() {
    $("#popup1, #overlay").hide();
}


$(document).ready(function () {
    PopUpHide();
});

function checkAndPopUpShow(cell) {
    var cellText = $(cell).find("td").text().trim();
    var snipe_id = $(cell).data("snipe_id");  // Retrieve snipe_id from the data attribute
    var imgSrc = $(cell).find(".card-img").attr("src"); // Retrieve the src attribute of the image
    var cellNumber = $(cell).find(".cell_number").val();
    console.log(cellNumber);

    var title = $(cell).find("#good-title").text().trim();
    var type = $(cell).find('.good-type').text().trim();

    // Check if cellText is "Cell is Empty" or "Goods is None" or title is undefined
    if (cellText === "Cell is Empty" || cellText === "Goods is None" || type === undefined || type.trim() === "Нет в наличии") {
        console.log('No goods or undefined title');
    } else {
        PopUpShow(snipe_id, title, imgSrc, cellNumber);
    }
}


function addLineBreak() {
    var cardTextElements = document.querySelectorAll("#good-title");

    console.log(cardTextElements);
    
    cardTextElements.forEach(function(cardTextElement) {
        var cardText = cardTextElement.textContent;
        var cardWords = cardText.split(" ");
        if (cardWords.length > 1) {
            // Insert <br> after the second word
            cardWords.splice(2, 0, "<br>");
        }
        cardTextElement.innerHTML = cardWords.join(" ");
    });
}

// Call the addLineBreak function when the document is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    addLineBreak();
});