// Set up the validation for the add session form
function setupAddSessionForm() {
    const form = document.getElementById('addSessionForm');
    const groupId = document.getElementById('group_id');
    const date = document.getElementById('date');
    const submitButton = document.getElementById('submitButton');

    // If the form is not found, stop the script
    if (!form) {
        console.error('Add session form not found');
        return;
    }

    // event-driven programming:
    // block runs when the user clicks the add session button
    form.addEventListener("submit", function (event) {

        // Check that a group has been selected
        if (groupId.value === "") {
            event.preventDefault();
            alert("Please select a study group.");
            return;
        }

        // Check that a date has been selected
        if (date.value === "") {
            event.preventDefault();
            alert("Please select a date for the session.");
            return;
        }

        // Confirmation before submitting
        const confirmed = confirm("Are you sure you want to add this session?");

        // If the user clicks Cancel, stop the form from submitting
        if (!confirmed) {
            event.preventDefault();
            return;
        }

        // Disable submit button after submit to prevent multiple submissions
        submitButton.disabled = true;
        submitButton.textContent = "Adding...";
    });
}

// Browser event: run setupAddSessionForm after the HTML page has loaded.
document.addEventListener("DOMContentLoaded", setupAddSessionForm);