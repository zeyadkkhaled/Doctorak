//temp header we footer
function updateHeaderButton() {
    const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
    const userRole = document.body.dataset.userRole;

    const headerButtons = document.querySelector('.h .d-flex');
    if (headerButtons) {
        headerButtons.innerHTML = isAuthenticated ? `
            <a href="/profile/" class="btn btn-outline-light me-2 d-flex align-items-center">
                <i class="bi bi-person-circle me-2"></i>
                <span>Profile</span>
            </a>
            <button id="logoutButton" class="btn btn-outline-light d-flex align-items-center">
                <i class="bi bi-box-arrow-right me-2"></i>
                <span>Logout</span>
            </button>
        ` : `
            <button id="loginButton" class="btn btn-outline-light d-flex align-items-center"
                    data-bs-toggle="modal" data-bs-target="#loginModal">
                <i class="bi bi-box-arrow-in-right me-2"></i>
                <span>Sign In</span>
            </button>
        `;

        // Add event listener for logout button if authenticated
        if (isAuthenticated) {
            const logoutButton = document.getElementById('logoutButton');
            if (logoutButton) {
                logoutButton.addEventListener('click', () => {
                    window.location.href = '/logout/';
                });
            }
        }
    }
}

// Add this line right after the function definition
document.addEventListener('DOMContentLoaded', () => {
    // Only run updateHeaderButton() if we're on the homepage
    if (window.location.pathname === '/' || window.location.pathname === '/home/') {
        updateHeaderButton();
    }
});

// Rest of your code (myheader class definition, etc.) follows...
class myPatientHeader extends HTMLElement {
  connectedCallback() {
    const userName = document.body.dataset.userName || 'User';

    this.innerHTML = `
      <!-- Patient Header -->
      <div class="h" style="background-color: #00c4b4;">
        <div class="py-2 px-3 d-flex justify-content-between align-items-center">
          <!-- Logo (left) -->
          <a href="/">
            <img src="${static_url}imgs/logoso88.png" alt="Doctorak" style="height: 80px;" />
          </a>

          <!-- Welcome Message (center) -->
          <div class="text-white fw-bold fs-3 flex-grow-1 text-center">
            Welcome, ${userName}
          </div>

          <!-- Logout Button (right) -->
          <form action="/logout/" method="post" class="mb-0">
            <input type="hidden" name="csrfmiddlewaretoken" value="${CSRF_TOKEN}">
            <button type="submit" class="btn btn-outline-light ms-auto">
              Logout
            </button>
          </form>
        </div>
      </div>
    `;
  }
}

customElements.define('my-patient-header', myPatientHeader);

class myheader extends HTMLElement {
    connectedCallback() {
        const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
        const userRole = document.body.dataset.userRole;

        this.innerHTML = `
            <!-- Header -->
            <div class="h">
                <div class="py-2 px-3 container-fluid">
                  <div class="row align-items-center justify-content-between">
                    <div class="col-auto">
                      <a href="/">
                        <img src="${static_url}imgs/logoso88.png" alt="Doctorak" style="height: 80px;" />
                      </a>
                    </div>
                    <div class="col-auto d-flex">
                      ${isAuthenticated ? `
                        <a href="/profile/" class="btn btn-outline-light me-2 d-flex align-items-center">
                          <i class="bi bi-person-circle me-2"></i>
                          <span>Profile</span>
                        </a>
                        <button id="logoutButton" class="btn btn-outline-light d-flex align-items-center">
                          <i class="bi bi-box-arrow-right me-2"></i>
                          <span>Logout</span>
                        </button>
                      ` : `
                        <button id="loginButton" class="btn btn-outline-light d-flex align-items-center"
                                data-bs-toggle="modal" data-bs-target="#loginModal">
                          <i class="bi bi-box-arrow-in-right me-2"></i>
                          <span>Sign In</span>
                        </button>
                      `}
                    </div>
                  </div>
                </div>
                </div>

            <!-- Logo and Title -->
            <div class="text-center mt-4">
                <h1 class="fw-bold mt-3">Book with the Best Doctors in the World</h1>
                <p class="text-muted">Choose a doctor based on location, specialty, or ratings.</p>
            </div>

            <!-- Search Filters -->
            <div class="container mt-4 py-3 px-4 rounded" style="background-color:rgba(8, 196, 180, 0.87);">
                <div class="row g-2 mb-2 align-items-end">
                    <div class="col-md-3">
                        <label class="form-label d-flex align-items-center">
                            <i class="bi bi-globe-americas"></i>
                            Country
                        </label>
                        <select id="country" class="form-select">
                            <option value="">Select Country</option>
                            <option value="egypt">Egypt</option>
                            <option value="saudi">Saudi Arabia</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label d-flex align-items-center">
                            <i class="bi bi-geo-fill"></i>
                            City
                        </label>
                        <select id="city" class="form-select" disabled>
                            <option value="">Select City</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label d-flex align-items-center">
                            <i class="bi bi-geo-alt-fill"></i>
                            Region
                        </label>
                        <select id="region" class="form-select" disabled>
                            <option value="">Select Region</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label d-flex align-items-center">
                            <img src="${static_url}imgs/spec.png" alt="Specialty Icon" style="width: 20px; height: 20px; margin-right: 6px;">
                            Specialty
                        </label>
                        <select class="form-select">
                            <option value="">Specialty</option>
                            <option>Pediatrics & Newborn</option>
                            <option>Internal Medicine</option>
                            <option>Obstetrics & Gynecology</option>
                            <option>Dentistry</option>
                            <option>Cardiology</option>
                            <option>Orthopedics</option>
                            <option>ENT</option>
                            <option>General Surgery</option>
                            <option>Neurology</option>
                            <option>Dermatology</option>
                            <option>Oncology</option>
                            <option>Ophthalmology</option>
                        </select>
                    </div>
                </div>

                <div class="row g-2 align-items-end">
                    <div class="col-md-10">
                        <input type="text" class="form-control" placeholder="Search by doctor name (optional)" />
                    </div>
                    <div class="col-md-2 text-end">
                        <button class="btn btn-primary w-100 d-flex align-items-center justify-content-center" 
                                style="background-color: #d9edea;" 
                                onclick="window.location.href='../pages/spec.html'">
                            <i class="bi bi-search" style="color:black;"></i>
                            <span style="color: black;">Search</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Login Modal -->
            <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content" style="background-color: #e8fffc;">
                        <div class="modal-header" style="background-color: #00c4b4;">
                            <h5 class="modal-title" id="loginModalLabel">Login</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form action="${LOGIN_URL}" method="post">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${CSRF_TOKEN}">
                                <div class="alert alert-warning">Enter your account details!</div>
                                <div class="form-group mb-3">
                                    <label for="email">Email address</label>
                                    <input type="email" name="email" class="form-control" placeholder="Enter email" required>
                                </div>
                                <div class="form-group mb-3">
                                    <label for="password">Password</label>
                                    <input type="password" name="password" class="form-control" placeholder="Password" required>
                                </div>
                                <button type="submit" class="btn btn-primary btn-block w-100" style="background-color: #00c4b4;">Login</button>
                            </form>
                            <hr>
                            <p class="text-center">Don't have an account? <a href="/register">Sign up</a></p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add event listeners
        if (isAuthenticated) {
            const logoutButton = this.querySelector('#logoutButton');
            if (logoutButton) {
                logoutButton.addEventListener('click', () => {
                    window.location.href = '/logout/';
                });
            }
        }

        // Initialize location dropdowns
        this.initializeLocationDropdowns();
    }

    initializeLocationDropdowns() {
        const countrySelect = this.querySelector('#country');
        const citySelect = this.querySelector('#city');
        const regionSelect = this.querySelector('#region');

        if (countrySelect && citySelect && regionSelect) {
            countrySelect.addEventListener('change', () => {
                this.updateCityOptions(countrySelect.value);
            });

            citySelect.addEventListener('change', () => {
                this.updateRegionOptions(citySelect.value);
            });
        }
    }

    updateCityOptions(country) {
        const citySelect = this.querySelector('#city');
        const regionSelect = this.querySelector('#region');

        citySelect.innerHTML = '<option value="">Select City</option>';
        regionSelect.innerHTML = '<option value="">Select Region</option>';

        citySelect.disabled = !country;
        regionSelect.disabled = true;

        if (cityOptions[country]) {
            cityOptions[country].forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        }
    }

    updateRegionOptions(city) {
        const regionSelect = this.querySelector('#region');

        regionSelect.innerHTML = '<option value="">Select Region</option>';
        regionSelect.disabled = !city;

        if (regionOptions[city]) {
            regionOptions[city].forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                regionSelect.appendChild(option);
            });
        }
    }
}

customElements.define('my-header', myheader);

class mysheader extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <!-- Header -->
            <div class="h">
            <div class=" py-2 px-3 d-flex justify-content-between align-items-center">
                <a href="/">
                <img src="${static_url}imgs/logoso88.png" alt="Doctorak" style="height: 80px;" />
                </a>
                <button id="profileButton" class="btn btn-outline-light ms-auto d-flex align-items-center" type="button" data-bs-toggle="modal" data-bs-target="#loginModal" aria-controls="loginModal">
                                <i class="bi bi-person-circle me-2"></i>
                                <span id="profileButtonText">Sign In</span>
                </button>
            </div>
            </div>
            
            
            <!-- Login Modal -->
                <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true" >
                    <div class="modal-dialog">
                        <div class="modal-content"style="background-color: #e8fffc;">
                            <div class="modal-header"style="background-color: #00c4b4;">
                                <h5 class="modal-title" id="loginModalLabel">Login</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                  <form action="${LOGIN_URL}" method="post">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${CSRF_TOKEN}">
                                    <div class="alert alert-warning">Enter your account details!!!</div>
                                    <div class="form-group mb-3">
                                        <label for="email">Email address</label>
                                        <input type="email" name="email" class="form-control" placeholder="Enter email" required>
                                    </div>
                                    <div class="form-group mb-3">
                                        <label for="password">Password</label>
                                        <input type="password" name="password" class="form-control" placeholder="Password" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary btn-block w-100" style="background-color: #00c4b4;">Login</button>
                                </form>
                                <hr>
                                <p class="text-center">Don't have an account? <a href="/register" ">Sign up</a></p>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Make Appointment Modal -->
                <div class="modal fade" id="makeAppointmentModal" tabindex="-1" aria-labelledby="makeAppointmentModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="makeAppointmentModalLabel">Schedule a New Appointment</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="makeAppointmentForm">
                                    <div class="mb-3">
                                        <label for="appointmentDate" class="form-label">Date</label>
                                        <input type="date" class="form-control" id="appointmentDate" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="appointmentTime" class="form-label">Time</label>
                                        <input type="time" class="form-control" id="appointmentTime" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="doctorName" class="form-label">Doctor</label>
                                        <input type="text" class="form-control" id="doctorName" required>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-success" id="scheduleAppointment">Schedule Appointment</button>
                            </div>
                        </div>
                    </div>
                </div>
            
                `;
        updateHeaderButton();
    }
}

customElements.define('my-sheader', mysheader);


class myfooter extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
                        <footer class="text-center">
                    <div class="container">
                        <p style="margin: 5px;"><strong>Contact Us</strong></p>
                        <p style="margin: 5px;">Email: <a href="mailto:Doctorak@gmail.com" style="color: white;">Doctorak@gmail.com</a></p>
                        <p style="margin: 5px;">Phone: <a href="tel:0100010010000" style="color: white;">0100010010000</a></p>
                        <div class="social-icons" style="margin: 10px;">
                            <a href="https://www.facebook.com/gamahospitalofficial/" target="_blank"><i class="bi bi-facebook"></i></a>
                            <a href="https://www.facebook.com/doctorakdotcom/" target="_blank"><i class="bi bi-twitter"></i></a>
                            <a href="https://www.instagram.com/doctorakdotcom/" target="_blank"><i class="bi bi-linkedin"></i></a>
                            <a href="https://www.instagram.com/doctorakdotcom/" target="_blank"><i class="bi bi-instagram"></i></a>
                        </div>
                    </div>
                </footer>
                `;
    }
}

customElements.define('my-footer', myfooter);


//7war lama ydos book yktb esm el dr.


document.querySelectorAll('.book-btn').forEach(button => {
    button.addEventListener('click', function () {
        const doctorName = this.getAttribute('data-doctor');
        const doctorInput = document.getElementById('doctorName');
        if (doctorInput && doctorName) {
            doctorInput.value = doctorName;
        }
    });
});


document.querySelectorAll('.specialty-card').forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => {
        const specialty = encodeURIComponent(card.getAttribute('data-specialty'));
        window.location.href = `spec.html?specialty=${specialty}`;
    });
});

const urlParams = new URLSearchParams(window.location.search);
const specialty = urlParams.get('specialty');
console.log("Searching for doctors in:", specialty);

//7war el region
document.addEventListener("DOMContentLoaded", function () {
    const cityOptions = {
        egypt: [
            "Cairo",
            "Alexandria",
            "Giza",
            "Dakahlia",
            "Sharqia",
            "Qalyubia",
            "Sohag",
            "Assiut"
        ],
        saudi: [
            "Riyadh",
            "Jeddah",
            "Dammam",
            "Mecca",
            "Medina",
            "Khobar"
        ]
    };

    const regionOptions = {
        Cairo: ["Nasr City", "Heliopolis", "Maadi", "Zamalek", "New Cairo", "Shubra", "Mokattam"],
        Alexandria: ["Sidi Gaber", "Gleem", "Smouha", "Mandara", "Agami", "Stanley"],
        Giza: ["Dokki", "Mohandessin", "Faisal", "Haram", "6th of October", "Sheikh Zayed"],
        Dakahlia: ["Mansoura", "Talkha", "Mit Ghamr"],
        Sharqia: ["Zagazig", "10th of Ramadan", "Belbeis"],
        Qalyubia: ["Banha", "Qalyub", "Shubra El Kheima"],
        Sohag: ["Sohag City", "Tahta", "Akhmim"],
        Assiut: ["Assiut City", "Manfalut", "Dairut"],

        Riyadh: ["Olaya", "Al Malaz", "King Fahd District", "Al Nakheel", "Al Murabba", "Al Yasmin"],
        Jeddah: ["Al Andalus", "Al Hamra", "Al Faisaliyah", "Al Rawdah", "Al Salamah", "Al Safa"],
        Dammam: ["Al Faisaliyah", "Al Shati", "Al Mazruiyah", "Al Khalij"],
        Mecca: ["Al Aziziyah", "Al Shoqiyah", "Al Awali"],
        Medina: ["Al Haram", "Al Qiblatain", "Al Aqiq"],
        Khobar: ["Al Ulaya", "Al Aqrabiyah", "Al Thuqbah"]
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
        citySelect.disabled = !country;
        regionSelect.disabled = true;

        // Populate cities if a valid country is selected
        if (cityOptions[country]) {
            cityOptions[country].forEach(function (city) {
                const option = document.createElement("option");
                option.value = city;
                option.text = city;
                citySelect.appendChild(option);
            });
        }
    });

    // Populate regions based on selected city
    citySelect.addEventListener("change", function () {
        const city = citySelect.value;
        const country = countrySelect.value;

        // Reset and disable region dropdown
        regionSelect.innerHTML = `<option value="">Select Region</option>`;
        regionSelect.disabled = !city;

        // Validate that the city belongs to the selected country
        if (city && country && cityOptions[country]?.includes(city)) {
            if (regionOptions[city]) {
                regionOptions[city].forEach(function (region) {
                    const option = document.createElement("option");
                    option.value = region;
                    option.text = region;
                    regionSelect.appendChild(option);
                });
            }
        }
    });
});


//sort card
function sortCards() {
    const sortOption = document.getElementById('sortOption').value;
    const grid = document.getElementById('doctorGrid');
    const cards = Array.from(grid.getElementsByClassName('card'));

    if (sortOption === 'nearest') {
        cards.sort((a, b) => {
            const originalOrderA = cards.indexOf(a);
            const originalOrderB = cards.indexOf(b);
            return originalOrderA - originalOrderB;
        });
    } else if (sortOption === 'cost-asc') {
        cards.sort((a, b) => {
            const costA = parseInt(a.getAttribute('data-cost'));
            const costB = parseInt(b.getAttribute('data-cost'));
            return costA - costB;
        });
    } else if (sortOption === 'cost-desc') {
        cards.sort((a, b) => {
            const costA = parseInt(a.getAttribute('data-cost'));
            const costB = parseInt(b.getAttribute('data-cost'));
            return costB - costA;
        });
    } else if (sortOption === 'stars-desc') {
        cards.sort((a, b) => {
            const starsA = parseInt(a.getAttribute('data-stars'));
            const starsB = parseInt(b.getAttribute('data-stars'));
            return starsB - starsA;
        });
    }

    grid.innerHTML = '';
    cards.forEach(card => grid.appendChild(card));
}

//bycheck password of signup
const form = document.querySelector('.signup-form');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm-password');

form.addEventListener('submit', function (e) {
    // Check if passwords match
    if (password.value !== confirmPassword.value) {
        e.preventDefault();
        confirmPassword.classList.add('is-invalid');
    } else {
        confirmPassword.classList.remove('is-invalid');
    }
});

// Live correction
confirmPassword.addEventListener('input', function () {
    if (password.value === confirmPassword.value) {
        confirmPassword.classList.remove('is-invalid');
    }
});

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

document.getElementById('saveChanges').addEventListener('click', function () {
    const name = document.getElementById('inputName').value;
    const age = document.getElementById('inputAge').value;
    const gender = document.getElementById('inputGender').value;
    const contact = document.getElementById('inputContact').value;
    const address = document.getElementById('inputAddress').value;

    document.getElementById('displayName').innerText = name;
    document.getElementById('displayAge').innerText = age;
    document.getElementById('displayGender').innerText = gender;

    const modal = bootstrap.Modal.getInstance(document.getElementById('editInfoModal'));
    modal.hide();
});

document.getElementById('scheduleAppointment').addEventListener('click', function () {
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
    cancelButton.onclick = function () {
        table.deleteRow(newRow.rowIndex - 1); // Remove the row from the table
    };

    // Append the cancel button to the action cell
    actionCell.appendChild(cancelButton);

    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('makeAppointmentModal'));
    modal.hide();

    // Clear the form inputs
    document.getElementById('makeAppointmentForm').reset();
});

//by7sb el 3omr mn data of birth

document.getElementById('dob').addEventListener('change', function () {
    const dob = new Date(this.value);
    const today = new Date();

    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    // Update the displayAge span with calculated age
    document.getElementById('displayAge').textContent = age;
});

//byedit info el 3yada