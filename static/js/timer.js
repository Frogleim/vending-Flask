var timeInSeconds = 10;
var popupTimer = 5;


function updatePopupTimer() {
    var minutes = Math.floor(popupTimer / 60);
    var seconds = popupTimer % 60;

    var displayMinutes = String(minutes).padStart(2, '0');
    var displaySeconds = String(seconds).padStart(2, '0');

    document.getElementById('timer').textContent = displayMinutes + ':' + displaySeconds;

    if (popupTimer <= 0) {
        clearInterval(popupTimer); 
        window.location.href = '/'; 
    } else {
        popupTimer--; 
    }
}

function updateTimer() {
    var minutes = Math.floor(timeInSeconds / 60);
    var seconds = timeInSeconds % 60;

    var displayMinutes = String(minutes).padStart(2, '0');
    var displaySeconds = String(seconds).padStart(2, '0');

    document.getElementById('timer').textContent = displayMinutes + ':' + displaySeconds;

    if (timeInSeconds <= 0) {
        clearInterval(timerInterval); 
        window.location.href = '/'; 
    } else {
        timeInSeconds--; 
    }
}
updateTimer();
var timerInterval = setInterval(updateTimer, 1000);