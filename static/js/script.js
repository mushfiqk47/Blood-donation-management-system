/**
 * ============================================================
 * BloodLife - Frontend JavaScript
 * ============================================================
 * This script runs in the browser and handles user interactions:
 * 1. Mobile navigation menu toggle
 * 2. Finding and filtering donors on the Donors page
 * 3. Validating and submitting the Donor Registration form
 * 4. Handling Admin login authentication
 * 5. Managing the Admin Dashboard (viewing stats, adding, deleting donors)
 * ============================================================
 */

// Wait for the HTML document to finish loading before running our code
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initDonorsPage();
    initRegisterPage();
    initAdminLoginPage();
    initDashboardPage();
});

/* ============================================================
   1. NAVIGATION MODULE (Mobile Menu)
   ============================================================ */
function initNavigation() {
    var navToggle = document.getElementById('navToggle');
    var navLinks = document.getElementById('navLinks');

    // Only run if the navigation elements exist on the page
    if (!navToggle || !navLinks) return;

    // Toggle menu open/closed when user clicks the "Menu" button
    navToggle.addEventListener('click', function() {
        var isOpen = navLinks.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close menu when clicking anywhere outside of the navbar
    document.addEventListener('click', function(event) {
        if (!navToggle.contains(event.target) && !navLinks.contains(event.target)) {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
}

/* ============================================================
   2. FIND DONORS PAGE MODULE
   ============================================================ */
function initDonorsPage() {
    var searchInput = document.getElementById('searchInput');
    var bloodBtns = document.getElementById('bloodBtns');
    var donorsBody = document.getElementById('donorsBody');

    // Only run if we are currently on the Find Donors page
    if (!searchInput || !bloodBtns || !donorsBody) return;

    var selectedBlood = '';

    /**
     * loadDonors() - Fetches donor data from the Flask API (/api/donors)
     * and renders the rows into the HTML table.
     */
    function loadDonors() {
        var search = searchInput.value.trim();
        var blood = selectedBlood;

        // Step 1: Build the API request URL with query parameters
        var url = '/api/donors?';
        if (search) url += 'search=' + encodeURIComponent(search) + '&';
        if (blood) url += 'blood=' + encodeURIComponent(blood) + '&';

        // Step 2: Fetch data from Flask backend
        fetch(url)
            .then(function(response) {
                return response.json();
            })
            .then(function(donors) {
                // Step 3: Handle empty results
                if (!Array.isArray(donors) || donors.length === 0) {
                    donorsBody.innerHTML = '<tr><td colspan="8" class="no-results">No donors found matching your search.</td></tr>';
                    return;
                }

                // Step 4: Render donor rows into the table
                donorsBody.innerHTML = donors.map(function(donor) {
                    var messageText = donor.message 
                        ? (donor.message.length > 40 ? donor.message.substring(0, 40) + '...' : donor.message) 
                        : '--';

                    return '<tr>' +
                        '<td><strong>' + escapeHtml(donor.name) + '</strong></td>' +
                        '<td><span class="donor-blood">' + escapeHtml(donor.blood_group) + '</span></td>' +
                        '<td>' + escapeHtml(donor.phone) + '</td>' +
                        '<td>' + (donor.email ? escapeHtml(donor.email) : '--') + '</td>' +
                        '<td>' + escapeHtml(donor.location) + '</td>' +
                        '<td>' + (donor.age != null ? escapeHtml(String(donor.age)) : '--') + '</td>' +
                        '<td>' + (donor.gender ? escapeHtml(donor.gender) : '--') + '</td>' +
                        '<td title="' + escapeHtml(donor.message || '') + '">' + escapeHtml(messageText) + '</td>' +
                    '</tr>';
                }).join('');
            })
            .catch(function(error) {
                console.error('Error fetching donors:', error);
                donorsBody.innerHTML = '<tr><td colspan="8" class="no-results">Unable to load donor list. Please try again.</td></tr>';
            });
    }

    // Step 5: Check if a blood group was passed via URL query parameter (e.g. ?blood=A+)
    var urlParams = new URLSearchParams(window.location.search);
    var urlBlood = urlParams.get('blood');
    if (urlBlood) {
        selectedBlood = urlBlood;
        document.querySelectorAll('.blood-btn').forEach(function(btn) {
            btn.classList.toggle('active', btn.getAttribute('data-blood') === urlBlood);
        });
    }

    // Step 6: Handle Blood Group filter button clicks
    bloodBtns.addEventListener('click', function(event) {
        var clickedBtn = event.target.closest('.blood-btn');
        if (!clickedBtn) return;

        selectedBlood = clickedBtn.getAttribute('data-blood') || '';

        // Update active highlight on buttons
        document.querySelectorAll('.blood-btn').forEach(function(btn) {
            btn.classList.toggle('active', btn === clickedBtn);
        });

        loadDonors();
    });

    // Step 7: Handle Search Button click and live typing in Search input
    var searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', loadDonors);
    }
    searchInput.addEventListener('input', loadDonors);

    // Initial load when page opens
    loadDonors();
}

/* ============================================================
   3. DONOR REGISTRATION MODULE
   ============================================================ */
function initRegisterPage() {
    var registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    // Define validation rules for required fields
    var validationRules = [
        { id: 'regName', validate: function(val) { return val.trim().length > 0; } },
        { id: 'regBlood', validate: function(val) { return val.length > 0; } },
        { id: 'regPhone', validate: function(val) { return /^01[3-9]\d{8}$/.test(val.trim()); } },
        { id: 'regLocation', validate: function(val) { return val.trim().length > 0; } }
    ];

    // Real-time input validation on blur (when user clicks out of a field)
    validationRules.forEach(function(rule) {
        var inputEl = document.getElementById(rule.id);
        if (!inputEl) return;

        inputEl.addEventListener('blur', function() {
            var formGroup = this.closest('.form-group');
            if (formGroup) {
                if (!rule.validate(this.value)) {
                    formGroup.classList.add('has-error');
                } else {
                    formGroup.classList.remove('has-error');
                }
            }
        });

        // Clear error styling when user starts typing again
        inputEl.addEventListener('input', function() {
            if (rule.validate(this.value)) {
                var formGroup = this.closest('.form-group');
                if (formGroup) formGroup.classList.remove('has-error');
            }
        });
    });

    // Handle Form Submit Event
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var isValid = true;

        // Check all required fields before submitting
        validationRules.forEach(function(rule) {
            var inputEl = document.getElementById(rule.id);
            if (!inputEl) return;
            var formGroup = inputEl.closest('.form-group');
            if (!rule.validate(inputEl.value)) {
                if (formGroup) formGroup.classList.add('has-error');
                isValid = false;
            }
        });

        // Stop if any required field is invalid
        if (!isValid) return;

        var submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Registering...';
        }

        // Collect form data into a JavaScript object
        var ageInput = document.getElementById('regAge');
        var donorData = {
            name: document.getElementById('regName').value.trim(),
            blood_group: document.getElementById('regBlood').value,
            phone: document.getElementById('regPhone').value.trim(),
            email: document.getElementById('regEmail').value.trim(),
            location: document.getElementById('regLocation').value.trim(),
            age: ageInput && ageInput.value ? parseInt(ageInput.value, 10) : null,
            gender: document.getElementById('regGender').value,
            message: document.getElementById('regMessage').value.trim()
        };

        // Send POST request with JSON body to Flask backend API
        fetch('/api/donors', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(donorData)
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(result) {
            var alertBox = document.getElementById('formAlert');

            if (result.id) {
                // Success: Show confirmation alert & clear form
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Registered Successfully!';
                }

                if (alertBox) {
                    alertBox.className = 'alert alert-success';
                    alertBox.textContent = 'Registration successful! Thank you for becoming a donor.';
                    alertBox.classList.remove('hidden');
                }

                registerForm.reset();

                // Reset button text after 4 seconds
                setTimeout(function() {
                    if (submitBtn) submitBtn.textContent = 'Register Now';
                    if (alertBox) alertBox.classList.add('hidden');
                }, 4000);

            } else {
                // Backend returned validation error
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Register Now';
                }
                if (alertBox) {
                    alertBox.className = 'alert alert-error';
                    alertBox.textContent = result.error || 'Registration failed. Please check your inputs.';
                    alertBox.classList.remove('hidden');
                }
            }
        })
        .catch(function(error) {
            console.error('Registration network error:', error);
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Register Now';
            }
            var alertBox = document.getElementById('formAlert');
            if (alertBox) {
                alertBox.className = 'alert alert-error';
                alertBox.textContent = 'Error connecting to the server. Please check your connection.';
                alertBox.classList.remove('hidden');
            }
        });
    });
}

/* ============================================================
   4. ADMIN LOGIN MODULE
   ============================================================ */
function initAdminLoginPage() {
    var loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var loginBtn = document.getElementById('loginBtn');
        if (loginBtn) loginBtn.disabled = true;

        var usernameInput = document.getElementById('username');
        var passwordInput = document.getElementById('password');

        // Send login credentials to backend
        fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: usernameInput ? usernameInput.value : '',
                password: passwordInput ? passwordInput.value : ''
            })
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.message && data.message.toLowerCase().includes('success')) {
                // Redirect to dashboard upon successful login
                window.location = '/admin/dashboard';
            } else {
                // Show error message
                var alertBox = document.getElementById('alert');
                if (alertBox) {
                    alertBox.className = 'alert alert-error';
                    alertBox.textContent = data.error || 'Invalid username or password';
                    alertBox.classList.remove('hidden');
                }
                if (loginBtn) loginBtn.disabled = false;
            }
        })
        .catch(function(error) {
            console.error('Login error:', error);
            var alertBox = document.getElementById('alert');
            if (alertBox) {
                alertBox.className = 'alert alert-error';
                alertBox.textContent = 'Network error. Please try again.';
                alertBox.classList.remove('hidden');
            }
            if (loginBtn) loginBtn.disabled = false;
        });
    });
}

/* ============================================================
   5. ADMIN DASHBOARD MODULE
   ============================================================ */
function initDashboardPage() {
    var addModal = document.getElementById('addModal');
    var openModalBtn = document.getElementById('openModalBtn');
    var addForm = document.getElementById('addForm');
    var dTotal = document.getElementById('dTotal');

    // Only run if we are on the admin dashboard
    if (!addModal && !dTotal) return;

    var modalCloseBtn = document.getElementById('modalClose');
    var cancelBtn = document.querySelector('.cancelBtn');

    // Open Modal function
    function openModal() {
        if (!addModal) return;
        addModal.classList.remove('hidden');
        document.body.classList.add('modal-open');
        var firstInput = addModal.querySelector('input, select, textarea');
        if (firstInput) firstInput.focus();
    }

    // Close Modal function
    function closeModal() {
        if (!addModal) return;
        addModal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }

    // Event listeners to open and close the modal
    if (openModalBtn) openModalBtn.addEventListener('click', openModal);
    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

    // Close modal when clicking on the dark overlay background
    if (addModal) {
        addModal.addEventListener('click', function(event) {
            if (event.target === addModal) closeModal();
        });
    }

    // Close modal when pressing the Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && addModal && !addModal.classList.contains('hidden')) {
            closeModal();
        }
    });

    /**
     * loadDashboard() - Refreshes statistics and the donor list table.
     */
    function loadDashboard() {
        // Step 1: Fetch overall stats (/api/stats)
        fetch('/api/stats')
            .then(function(response) { return response.json(); })
            .then(function(stats) {
                var totalEl = document.getElementById('dTotal');
                var availEl = document.getElementById('dAvail');
                if (totalEl) totalEl.textContent = stats.total != null ? stats.total : '--';
                if (availEl) availEl.textContent = stats.available != null ? stats.available : '--';
            })
            .catch(function(error) {
                console.error('Error loading stats:', error);
            });

        // Step 2: Fetch all donors (/api/donors)
        var tableBody = document.getElementById('donorsBody');
        if (!tableBody) return;

        fetch('/api/donors')
            .then(function(response) { return response.json(); })
            .then(function(donors) {
                if (!Array.isArray(donors) || donors.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="10" class="no-results">No donor records found.</td></tr>';
                    return;
                }

                tableBody.innerHTML = donors.map(function(donor) {
                    var messageText = donor.message 
                        ? (donor.message.length > 40 ? donor.message.substring(0, 40) + '...' : donor.message) 
                        : '--';

                    return '<tr>' +
                        '<td>#' + escapeHtml(String(donor.id)) + '</td>' +
                        '<td><strong>' + escapeHtml(donor.name) + '</strong></td>' +
                        '<td><span class="donor-blood">' + escapeHtml(donor.blood_group) + '</span></td>' +
                        '<td>' + escapeHtml(donor.phone) + '</td>' +
                        '<td>' + (donor.email ? escapeHtml(donor.email) : '--') + '</td>' +
                        '<td>' + (donor.age != null ? escapeHtml(String(donor.age)) : '--') + '</td>' +
                        '<td>' + (donor.gender ? escapeHtml(donor.gender) : '--') + '</td>' +
                        '<td>' + escapeHtml(donor.location) + '</td>' +
                        '<td title="' + escapeHtml(donor.message || '') + '">' + escapeHtml(messageText) + '</td>' +
                        '<td><button type="button" onclick="deleteDonor(' + donor.id + ')" class="btn btn-sm btn-danger-outline" aria-label="Delete ' + escapeHtml(donor.name) + '">Delete</button></td>' +
                    '</tr>';
                }).join('');
            })
            .catch(function(error) {
                console.error('Error loading dashboard donors:', error);
                tableBody.innerHTML = '<tr><td colspan="10" class="no-results">Error loading donor list.</td></tr>';
            });
    }

    // Step 3: Handle Add Donor Modal form submission
    if (addForm) {
        addForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var ageInput = document.getElementById('a_age');

            var newDonor = {
                name: document.getElementById('a_name').value.trim(),
                blood_group: document.getElementById('a_blood').value,
                phone: document.getElementById('a_phone').value.trim(),
                location: document.getElementById('a_location').value.trim(),
                email: document.getElementById('a_email').value.trim(),
                age: ageInput && ageInput.value ? parseInt(ageInput.value, 10) : null,
                gender: document.getElementById('a_gender').value,
                message: document.getElementById('a_message').value.trim()
            };

            fetch('/api/donors', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newDonor)
            })
            .then(function(response) { return response.json(); })
            .then(function() {
                closeModal();
                addForm.reset();
                loadDashboard(); // Refresh table and stats
            })
            .catch(function(error) {
                console.error('Error adding donor:', error);
            });
        });
    }

    /**
     * deleteDonor(id) - Deletes a donor record after confirmation.
     * Attached to window so the inline onclick on the button can call it.
     */
    window.deleteDonor = function(id) {
        if (!confirm('Are you sure you want to delete donor #' + id + '?')) return;

        fetch('/api/donors/' + id, { method: 'DELETE' })
            .then(function() {
                loadDashboard(); // Refresh table and stats
            })
            .catch(function(error) {
                console.error('Error deleting donor:', error);
            });
    };

    // Initial load when opening dashboard
    loadDashboard();
}

/* ============================================================
   6. UTILITY FUNCTIONS
   ============================================================ */

/**
 * escapeHtml(str) - Prevents Cross-Site Scripting (XSS) by sanitizing
 * special HTML characters before rendering them into the page.
 */
function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
