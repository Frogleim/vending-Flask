document.addEventListener("DOMContentLoaded", function () {
    const hiddenInput = document.getElementById("user_id");
    const submitButton = document.getElementById("submitButton");
    hiddenInput.focus();

    if (hiddenInput && submitButton) {
        hiddenInput.select();

        hiddenInput.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent default Enter key behavior
                submitButton.click(); // Trigger form submission
            }
        });

        submitButton.addEventListener("click", function () {
            const inputValue = hiddenInput.value;
            console.log(inputValue);

            if (inputValue.length === 10) {
                console.log("ok");
                // Submit the form when input length is 10
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
