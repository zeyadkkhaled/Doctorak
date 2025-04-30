//by edit pp
            function updateProfilePicture() {
                const fileInput = document.getElementById('editProfilePic');
                const profilePicture = document.getElementById('profilePicture');
                const file = fileInput.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        profilePicture.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            }

            document.getElementById('saveChanges').addEventListener('click', function() {
                const name = document.getElementById('inputName').value;
                const dob = document.getElementById('inputDOB').value;
                const gender = document.getElementById('inputGender').value;
                const contact = document.getElementById('inputContact').value;
                const address = document.getElementById('inputAddress').value;

                // Calculate age based on date of birth
                const dobDate = new Date(dob);
                const today = new Date();
                let age = today.getFullYear() - dobDate.getFullYear();
                const monthDiff = today.getMonth() - dobDate.getMonth();
                if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dobDate.getDate())) {
                    age--;
                }

                // Update the display fields
                document.getElementById('displayName').innerText = name;
                document.getElementById('displayDOB').innerText = dob;
                document.getElementById('displayAge').innerText = age;
                document.getElementById('displayGender').innerText = gender;

                const modal = bootstrap.Modal.getInstance(document.getElementById('editInfoModal'));
                modal.hide();
            });

            document.getElementById('scheduleAppointment').addEventListener('click', function() {
                // Get values from the form
                const date = document.getElementById('appointmentDate').value;
                const time = document.getElementById('appointmentTime').value;
                const doctor = document.getElementById('doctorName').value;

                // Validate inputs
                if (!date || !time || !doctor) {
                    alert('Please fill in all fields.');
                    return;
                }

                // Create a new row in the appointments table
                const table = document.getElementById('appointmentsTable').getElementsByTagName('tbody')[0];
                const newRow = table.insertRow();

                // Insert new cells for the new row
                const dateCell = newRow.insertCell(0);
                const timeCell = newRow.insertCell(1);
                const doctorCell = newRow.insertCell(2);
                const statusCell = newRow.insertCell(3);
                const actionCell = newRow.insertCell(4);

                // Set the cell values
                dateCell.innerText = date;
                timeCell.innerText = time;
                doctorCell.innerText = doctor;
                statusCell.innerText = 'Pending'; // Default status

                // Create a cancel button
                const cancelButton = document.createElement('button');
                cancelButton.innerText = 'Cancel';
                cancelButton.className = 'btn btn-danger btn-sm cancel-appointment';
                cancelButton.onclick = function() {
                    table.deleteRow(newRow.rowIndex - 1); // Remove the row from the table
                };

                // Append the cancel button to the action cell
                actionCell.appendChild(cancelButton);

                // Close the modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('makeAppointmentModal'));
                modal.hide();                // Clear the form inputs                document.getElementById('makeAppointmentForm').reset();            });//by7sb el 3omr mn data of birth        document.getElementById('dob').addEventListener('change', function () {        const dob = new Date(this.value);        const today = new Date();        let age = today.getFullYear() - dob.getFullYear();        const m = today.getMonth() - dob.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
        }

        // Update the displayAge span with calculated age
        document.getElementById('displayAge').textContent = age;
        });

//byedit info el 3yada

document.getElementById('saveClinicInfo').addEventListener('click', function() {
    const phone = document.getElementById('inputClinicPhone').value;
    const location = document.getElementById('inputClinicLocation').value;
    const startHour = document.getElementById('inputClinicStartHour').value;
    const endHour = document.getElementById('inputClinicEndHour').value;

    // Collect selected working days
    const days = [];
    document.querySelectorAll('#editClinicInfoModal .form-check-input:checked').forEach((checkbox) => {
        days.push(checkbox.value);
    });

    // Update the display fields
    document.getElementById('clinicPhone').innerText = phone;
    document.getElementById('clinicLocation').innerText = location;
    document.getElementById('clinicDays').innerText = days.join(', ');
    document.getElementById('clinicHours').innerText = `${startHour} - ${endHour}`;

    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('editClinicInfoModal'));
    modal.hide();
});