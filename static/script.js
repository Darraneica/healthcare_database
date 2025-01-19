// Toggle the edit form visibility
function toggleEdit() {
    const profileDetails = document.querySelectorAll('.profile-detail .detail-value');
    const editForm = document.getElementById('edit-form');
    const editButton = document.querySelector('button');

    // Toggle between edit and view mode
    if (editForm.style.display === 'none') {
        // Switch to edit mode
        editForm.style.display = 'block';
        profileDetails.forEach((element, index) => {
            document.getElementById('edit-name').value = document.getElementById('patient-name').textContent;
            document.getElementById('edit-dob').value = document.getElementById('patient-dob').textContent;
            document.getElementById('edit-phone').value = document.getElementById('patient-phone').textContent;
            document.getElementById('edit-email').value = document.getElementById('patient-email').textContent;
        });
        editButton.textContent = 'Cancel'; // Change button text to 'Cancel'
    } else {
        // Switch back to view mode
        editForm.style.display = 'none';
        editButton.textContent = 'Edit'; // Reset button text to 'Edit'
    }
}

// Save the changes from the edit form
function saveChanges(event) {
    event.preventDefault(); // Prevent form submission

    // Get the new values from the edit form
    const newName = document.getElementById('edit-name').value;
    const newDob = document.getElementById('edit-dob').value;
    const newPhone = document.getElementById('edit-phone').value;
    const newEmail = document.getElementById('edit-email').value;

    // Update the profile details with the new values
    document.getElementById('patient-name').textContent = newName;
    document.getElementById('patient-dob').textContent = newDob;
    document.getElementById('patient-phone').textContent = newPhone;
    document.getElementById('patient-email').textContent = newEmail;

    // Hide the edit form
    toggleEdit();
}

// Edit record function (for demonstration)
function editRecord(recordId) {
    alert("Editing record: " + recordId);
}

// Delete record function (for demonstration)
function deleteRecord(recordId) {
    const confirmed = confirm("Are you sure you want to delete this record?");
    if (confirmed) {
        document.getElementById('patient-records').removeChild(document.getElementById('patient-records').children[recordId - 1]);
    }
}


// scripts.js

// Function to check window size and hide/show the table
function checkWindowSize() {
    const table = document.getElementById('patients-table');
    
    // Check if the window width is less than 768px (small screens)
    if (window.innerWidth < 768) {
        table.style.display = 'none';  // Hide the table
    } else {
        table.style.display = 'block';  // Show the table
    }
}

// Listen for window resizing
window.addEventListener('resize', checkWindowSize);

// Initial check when the page loads
checkWindowSize();

