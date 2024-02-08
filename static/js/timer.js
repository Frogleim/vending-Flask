var timeInSeconds = 10;

        // Function to update the timer display
        function updateTimer() {
            var minutes = Math.floor(timeInSeconds / 60);
            var seconds = timeInSeconds % 60;

            // Add leading zeros if needed
            var displayMinutes = String(minutes).padStart(2, '0');
            var displaySeconds = String(seconds).padStart(2, '0');

            // Update the timer display
            document.getElementById('timer').textContent = displayMinutes + ':' + displaySeconds;

            // Check if the timer has expired
            if (timeInSeconds <= 0) {
                clearInterval(timerInterval); // Stop the timer
                window.location.href = '/'; // Redirect to the specified URL
            } else {
                timeInSeconds--; // Decrement the time remaining
            }
        }

        // Call the updateTimer function initially
        updateTimer();

        // Update the timer display every second
        var timerInterval = setInterval(updateTimer, 1000);