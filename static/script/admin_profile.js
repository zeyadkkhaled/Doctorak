// search buuton
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId).value.toUpperCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName("tr");
  
    for (let i = 1; i < rows.length; i++) {
      const rowText = rows[i].textContent.toUpperCase();
      rows[i].style.display = rowText.includes(input) ? "" : "none";
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    // Add Patient
    document.querySelector('#addPatientModal .btn-success').addEventListener('click', () => {
      const name = document.getElementById('addPatientName').value;
      const id = document.getElementById('addPatientId').value;
      const phone = document.getElementById('addPatientContact').value;
  
      const table = document.getElementById('patientsTable').querySelector('tbody');
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${name}</td>
        <td>${id}</td>
        <td>${phone}</td>
        <td>
          <button class="btn btn-info btn-sm">View</button>
          <button class="btn btn-warning btn-sm">Edit</button>
          <button class="btn btn-danger btn-sm">Delete</button>
        </td>
      `;
      table.appendChild(row);
      bootstrap.Modal.getInstance(document.getElementById('addPatientModal')).hide();
    });
  
    // Add Doctor
    document.querySelector('#addDoctorModal .btn-success').addEventListener('click', () => {
      const name = document.getElementById('addDoctorName').value;
      const id = document.getElementById('addDoctorId').value;
      const phone = document.getElementById('addDoctorContact').value;
  
      const table = document.getElementById('doctorsTable').querySelector('tbody');
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${name}</td>
        <td>${id}</td>
        <td>${phone}</td>
        <td>
          <button class="btn btn-info btn-sm">View</button>
          <button class="btn btn-warning btn-sm">Edit</button>
          <button class="btn btn-danger btn-sm">Delete</button>
        </td>
      `;
      table.appendChild(row);
      bootstrap.Modal.getInstance(document.getElementById('addDoctorModal')).hide();
    });
  
    // Add Appointment
    document.querySelector('#addAppointmentModal .btn-success').addEventListener('click', () => {
      const doctorName = document.getElementById('addAppDoctorName').value;
      const doctorId = document.getElementById('addAppDoctorId').value;
      const patientName = document.getElementById('addAppPatientName').value;
      const patientId = document.getElementById('addAppPatientId').value;
      const date = document.getElementById('addAppDate').value;
      const time = document.getElementById('addAppTime').value;
  
      const table = document.getElementById('appointmentsTable').querySelector('tbody');
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${doctorName} (${doctorId})</td>
        <td>${patientName} (${patientId})</td>
        <td>${date}</td>
        <td>${time}</td>
        <td>
          <button class="btn btn-success btn-sm">Accept</button>
          <button class="btn btn-danger btn-sm">Cancel</button>
        </td>
      `;
      table.appendChild(row);
      bootstrap.Modal.getInstance(document.getElementById('addAppointmentModal')).hide();
    });
  });
  // admin_profile.js

document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    document.getElementById('adminSearch').addEventListener('input', searchAdmins);
    document.getElementById('doctorSearch').addEventListener('input', searchDoctors);
    document.getElementById('patientSearch').addEventListener('input', searchPatients);
    document.getElementById('appointmentSearch').addEventListener('input', searchAppointments);
});

function searchAdmins() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#adminTable tbody tr');
    filterRows(rows, searchTerm);
}

function searchDoctors() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#doctorsTable tbody tr');
    filterRows(rows, searchTerm);
}

function searchPatients() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#patientsTable tbody tr');
    filterRows(rows, searchTerm);
}

function searchAppointments() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#appointmentsTable tbody tr');
    filterRows(rows, searchTerm);
}

function filterRows(rows, searchTerm) {
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// Delete functions
function confirmDeleteAdmin(adminId) {
    if (confirm('Are you sure you want to delete this admin?')) {
        deleteEntity(`/admin/delete-admin/${adminId}/`, 'Admin');
    }
}

function confirmDeleteDoctor(doctorId) {
    if (confirm('Are you sure you want to delete this doctor?')) {
        deleteEntity(`/admin/delete-doctor/${doctorId}/`, 'Doctor');
    }
}

function confirmDeletePatient(patientId) {
    if (confirm('Are you sure you want to delete this patient?')) {
        deleteEntity(`/admin/delete-patient/${patientId}/`, 'Patient');
    }
}

function confirmDeleteAppointment(appointmentId) {
    if (confirm('Are you sure you want to delete this appointment?')) {
        deleteEntity(`/admin/delete-appointment/${appointmentId}/`, 'Appointment');
    }
}

function deleteEntity(url, entityType) {
    fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${entityType} deleted successfully`);
            location.reload();
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting');
    });
}

function getCSRFToken() {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfTokenElement ? csrfTokenElement.value : '';
}