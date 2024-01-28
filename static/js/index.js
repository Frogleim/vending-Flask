document.addEventListener("DOMContentLoaded", function () {
    const hiddenInput = document.getElementById("user_id");
    const submitButton = document.getElementById("submitButton");
    hiddenInput.focus()
    if (hiddenInput && submitButton) {
        hiddenInput.select();

        hiddenInput.addEventListener("input", function () {
            const inputValue = this.value;

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
