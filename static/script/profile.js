document.addEventListener('DOMContentLoaded', function () {
    // Profile picture handling
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

    // Cities data
    const citiesByCountry = {
        'egypt': ['Cairo', 'Alexandria', 'Giza', 'Port Said', 'Suez'],
        'saudi': ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam']
    };

    // Regions data
    const regionsByCity = {
        'Cairo': ['Nasr City', 'Maadi', 'Heliopolis', 'Downtown'],
        'Alexandria': ['Miami', 'Montaza', 'Sidi Gaber'],
        'Riyadh': ['Al Olaya', 'Al Malaz', 'Al Murabba'],
        'Jeddah': ['Al Balad', 'Al Hamra', 'Al Andalus']
    };

    const countrySelect = document.getElementById('country');
    const citySelect = document.getElementById('city');
    const regionSelect = document.getElementById('region');

    // Store initial values
    const previousCity = citySelect.getAttribute('data-previous');
    const previousRegion = regionSelect.getAttribute('data-previous');

    function populateCities() {
        const country = countrySelect.value;
        citySelect.innerHTML = '<option value="">Select City</option>';
        regionSelect.innerHTML = '<option value="">Select Region</option>';

        if (country && citiesByCountry[country]) {
            citiesByCountry[country].forEach(city => {
                const option = new Option(city, city);
                if (city === previousCity) {
                    option.selected = true;
                }
                citySelect.add(option);
            });
        }

        if (previousCity) {
            populateRegions();
        }
    }

    function populateRegions() {
        const city = citySelect.value;
        regionSelect.innerHTML = '<option value="">Select Region</option>';

        if (city && regionsByCity[city]) {
            regionsByCity[city].forEach(region => {
                const option = new Option(region, region);
                if (region === previousRegion) {
                    option.selected = true;
                }
                regionSelect.add(option);
            });
        }
    }

    // Event listeners
    countrySelect.addEventListener('change', populateCities);
    citySelect.addEventListener('change', populateRegions);

    // Initial population if country is already selected
    if (countrySelect.value) {
        populateCities();
    }

    // Prescription handling
    const appointmentsTable = document.getElementById('appointmentsTable');
    const addPrescriptionModal = document.getElementById('addPrescriptionModal');
    const savePrescriptionButton = document.getElementById('savePrescription');

    if (appointmentsTable) {
        appointmentsTable.addEventListener('click', function (event) {
            if (event.target.classList.contains('add-prescription')) {
                const row = event.target.closest('tr');
                const patientId = row.cells[2].innerText;
                const patientName = row.cells[3].innerText;

                document.getElementById('patientId').value = patientId;
                document.getElementById('patientName').value = patientName;
                document.getElementById('prescriptionText').value = '';
                document.getElementById('prescriptionFile').value = '';
            }
        });
    }

    if (savePrescriptionButton) {
        savePrescriptionButton.addEventListener('click', function () {
            const patientId = document.getElementById('patientId').value;
            const patientName = document.getElementById('patientName').value;
            const prescriptionText = document.getElementById('prescriptionText').value;
            const prescriptionFile = document.getElementById('prescriptionFile').files[0];

            if (!prescriptionText && !prescriptionFile) {
                alert('Please write a prescription or upload a file.');
                return;
            }

            alert(`Prescription saved for ${patientName} (ID: ${patientId}).`);
            bootstrap.Modal.getInstance(addPrescriptionModal).hide();
        });
    }

    // Call initializeWorkingHours
    initializeWorkingHours();


})

// Working hours management
function initializeWorkingHours() {
    const workingDaysContainer = document.getElementById('working-days-container');
    const selectedDaysContainer = document.getElementById('selected-days-container');
    const applyHoursBtn = document.getElementById('apply-hours');
    const workingHoursStart = document.getElementById('working-hours-start');
    const workingHoursEnd = document.getElementById('working-hours-end');

    let workingHours = {};

    const dayCheckboxes = document.querySelectorAll('.working-day-checkbox');
    dayCheckboxes.forEach(checkbox => {
        const day = checkbox.value;
        const dayContainer = document.createElement('div');
        dayContainer.id = `time-inputs-${day}`;
        dayContainer.style.display = 'none';
        dayContainer.innerHTML = `
            <div class="row mt-2">
                <div class="col-md-6">
                    <input type="time" class="form-control" id="start-${day}"
                           placeholder="Start time for ${day}">
                </div>
                <div class="col-md-6">
                    <input type="time" class="form-control" id="end-${day}"
                           placeholder="End time for ${day}">
                </div>
            </div>
        `;
        checkbox.parentNode.after(dayContainer);

        checkbox.addEventListener('change', function () {
            dayContainer.style.display = this.checked ? 'block' : 'none';
        });
    });

    applyHoursBtn.addEventListener('click', function () {
        const checkedDays = document.querySelectorAll('.working-day-checkbox:checked');
        const defaultStart = workingHoursStart.value;
        const defaultEnd = workingHoursEnd.value;

        checkedDays.forEach(dayCheckbox => {
            const day = dayCheckbox.value;
            const dayId = `selected-${day}`;

            const individualStart = document.getElementById(`start-${day}`).value;
            const individualEnd = document.getElementById(`end-${day}`).value;

            const startTime = individualStart || defaultStart;
            const endTime = individualEnd || defaultEnd;

            if (!startTime || !endTime) {
                alert(`Please select both start and end times for ${day}`);
                return;
            }

            const existingSlot = document.getElementById(dayId);
            if (existingSlot) {
                existingSlot.remove();
            }

            const timeSlot = document.createElement('div');
            timeSlot.id = dayId;
            timeSlot.innerHTML = `
                <strong>${day}:</strong> ${startTime} - ${endTime}
                <input type="hidden" name="${day.toLowerCase()}_start" value="${startTime}">
                <input type="hidden" name="${day.toLowerCase()}_end" value="${endTime}">
            `;

            selectedDaysContainer.appendChild(timeSlot);
            workingHours[day] = {start: startTime, end: endTime};
        });
    });

    dayCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            if (!this.checked) {
                const dayId = `selected-${this.value}`;
                const existingSlot = document.getElementById(dayId);
                if (existingSlot) {
                    existingSlot.remove();
                }
                delete workingHours[this.value];
            }
        });
    });
}

// Function to remove exception
function removeException(id) {
    const exceptionElement = document.getElementById(`exception-${id}`);
    if (exceptionElement) {
        exceptionElement.remove();
    }
}