var timeInSeconds = 10;
var popupTimer = 5;



function updateTimer() {
    console.log(document.getElementById('timer').textContent);
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
var timerInterval = setInterval(updateTimer, 1000);