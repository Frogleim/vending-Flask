document.addEventListener("DOMContentLoaded", function () {
    const hiddenInput = document.getElementById("user_id");
    const submitButton = document.getElementById("submitButton");
    hiddenInput.focus()
    if (hiddenInput && submitButton) {
        hiddenInput.select();

        hiddenInput.addEventListener("input", function () {
            const inputValue = this.value;
            console.log(inputValue);

            if (inputValue.length === 10) {
                console.log("ok");
                // Automatically submit the form when input length is 10
                document.getElementById("myForm").submit();
            }
        });
    } else {
        console.error("Element with ID 'user_id' or 'submitButton' not found.");
    }
});

function cancelButtonClick() {
    console.log("Button clicked");
    // Add your button click functionality here
}

var inactivityTimeout; // Variable to hold the timeout ID

    // Function to reset the inactivity timer
    function resetInactivityTimer() {
        clearTimeout(inactivityTimeout); // Clear previous timeout
        inactivityTimeout = setTimeout(refreshPage, 5000); // Set a new timeout for 30 seconds
        console.log(inactivityTimeout);
    }

    // Function to refresh the page
    function refreshPage() {
        window.location.reload(true); // Reload the page
    }

    // Event listeners for user activity
    document.addEventListener('mousemove', resetInactivityTimer);
    document.addEventListener('keypress', resetInactivityTimer);

    // Initial call to start the inactivity timer
    resetInactivityTimer();