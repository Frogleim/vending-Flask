window.onload = function() {
    var fioElement = document.getElementById("fio");
    var fioText = fioElement.textContent;
    var fioWords = fioText.split(" ");
    fioElement.innerHTML = fioWords.join("<br>");
};