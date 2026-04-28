// Set up the validation for the create group form 
function setupCreateGroupForm() {
    const form = document.getElementById('createGroupForm');
    const unitCode = document.getElementById('unitCode');
    const unitName = document.getElementById('unitName');
    const topic = document.getElementById('topic');
    const members = document.getElementById('members');
    const submitButton = document.getElementById('submitButton');

    // if the form is not found, stop the script
    if (!form) {
        console.error('Create group form not found');
        return;
    }

    // event-driven programming:
    // block responds when the user types, it updates the form dynamically
    unitCode.addEventListener('input', function() {
        unitCode.value = unitCode.value.toUpperCase(); // convert to uppercase
    });

    // event-driven programming:
    // block runs when the user clicks the create button
    form.addEventListener("submit", function (event) {
        const unitCodeValue = unitCode.value.trim();
        const unitNameValue = unitName.value.trim();
        const topicValue = topic.value.trim();
        const membersValue = Number(members.value);

        // UWA unit code format
        const unitCodePattern = /^[A-Z]{4}[0-9]{4}$/;

        // check that the main required fields are not empty
        // show alert if something is missing and prevent form submission
        if (unitCodeValue === "" || unitNameValue === "" || topicValue === "" || members.value === "") {
            event.preventDefault();
            alert("Please fill in Unit Code, Unit Name, Study Topic, and Maximum Members.");
            return;
        }

        // check whether the unit code matches the required format
        if (!unitCodePattern.test(unitCodeValue)) {
            event.preventDefault();
            alert("Please enter a valid unit code, for example CITS3403.");
            return;
        }
        
        // make max and min threshold for members, show alert if the value is out of range \
        if (membersValue < 1 || membersValue > 50) {
            event.preventDefault();
            alert("Please enter a valid number of members.");
            return;
        }

        // Confirmation before submitting
        const confirmed = confirm("Are you sure you want to create this study group?");

        // If the user clicks Cancel, stop the form from submitting
        if (!confirmed) {
            event.preventDefault();
            return;
        }

        // Disable submit button after submit to prevent multiple submissions
        submitButton.disabled = true;
        submitButton.textContent = "Creating...";
    });
}

// Browser event: run setupCreateGroupForm after the HTML page has loaded.
document.addEventListener("DOMContentLoaded", setupCreateGroupForm);