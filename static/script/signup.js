document.addEventListener("DOMContentLoaded", function () {
    const cityOptions = {
        egypt: ["Cairo", "Alexandria", "Giza", "Luxor", "Aswan"],
        saudi: ["Riyadh", "Jeddah", "Dammam", "Medina", "Mecca"]
    };

    const regionOptions = {
        Cairo: ["Nasr City", "Heliopolis", "Maadi"],
        Alexandria: ["Sidi Gaber", "Gleem", "Smouha"],
        Giza: ["Dokki", "Mohandessin", "Faisal"],
        Riyadh: ["Olaya", "Al Malaz", "King Fahd District"],
        Jeddah: ["Al Andalus", "Al Hamra", "Al Faisaliyah"],
        Dammam: ["Al Faisaliyah", "Al Khobar", "Al Mazruiyah"]
    };

    const countrySelect = document.getElementById("country");
    const citySelect = document.getElementById("city");
    const regionSelect = document.getElementById("region");

    // Disable city and region dropdowns initially
    citySelect.disabled = true;
    regionSelect.disabled = true;

    // Populate cities based on selected country
    countrySelect.addEventListener("change", function () {
        const country = countrySelect.value;

        // Reset and disable city and region dropdowns
        citySelect.innerHTML = `<option value="">Select City</option>`;
        regionSelect.innerHTML = `<option value="">Select Region</option>`;
        regionSelect.disabled = true;

        // Populate cities if a valid country is selected
        if (cityOptions[country]) {
            cityOptions[country].forEach(function (city) {
                const option = document.createElement("option");
                option.value = city;
                option.text = city;
                citySelect.appendChild(option);
            });
            citySelect.disabled = false; // Enable city dropdown
        } else {
            citySelect.disabled = true; // Keep city dropdown disabled if no valid options
        }
    });

    // Populate regions based on selected city
    citySelect.addEventListener("change", function () {
        const city = citySelect.value;

        // Reset and disable region dropdown
        regionSelect.innerHTML = `<option value="">Select Region</option>`;

        // Populate regions if a valid city is selected
        if (regionOptions[city]) {
            regionOptions[city].forEach(function (region) {
                const option = document.createElement("option");
                option.value = region;
                option.text = region;
                regionSelect.appendChild(option);
            });
            regionSelect.disabled = false; // Enable region dropdown
        } else {
            regionSelect.disabled = true; // Keep region dropdown disabled if no valid options
        }
    });

    // Ensure dropdowns are enabled when valid options are present
    countrySelect.dispatchEvent(new Event("change"));
    citySelect.dispatchEvent(new Event("change"));
});






// Add this at the top with your other const declarations
const workingHoursStart = document.getElementById('working-hours-start');
const workingHoursEnd = document.getElementById('working-hours-end');
const applyHoursButton = document.getElementById('apply-hours');
applyHoursButton.addEventListener('click', function () {
    const startTime = workingHoursStart.value;
    const endTime = workingHoursEnd.value;

    selectedDays.forEach(day => {
        const dayLower = day.toLowerCase();

        // Create or update hidden inputs
        let startInput = document.querySelector(`input[name="${dayLower}_start"]`);
        let endInput = document.querySelector(`input[name="${dayLower}_end"]`);

        if (!startInput) {
            startInput = document.createElement('input');
            startInput.type = 'hidden';
            startInput.name = `${dayLower}_start`;
            selectedDaysContainer.appendChild(startInput);
        }

        if (!endInput) {
            endInput = document.createElement('input');
            endInput.type = 'hidden';
            endInput.name = `${dayLower}_end`;
            selectedDaysContainer.appendChild(endInput);
        }

        startInput.value = startTime;
        endInput.value = endTime;

        // Update visual display
        let dayEntry = document.getElementById(`selected-${day}`);
        if (!dayEntry) {
            dayEntry = document.createElement('div');
            dayEntry.id = `selected-${day}`;
            dayEntry.classList.add('mb-2');
            selectedDaysContainer.appendChild(dayEntry);
        }
        dayEntry.innerHTML = `<strong>${day}:</strong> ${startTime} - ${endTime}`;
    });
});