// Main JavaScript for Course Module Registration System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Materialize components
    initializeMaterialize();
    
    // Setup message handling
    setupMessages();
    
    // Setup AJAX forms
    setupAjaxForms();
    
    // Setup module registration
    setupModuleRegistration();
});

function initializeMaterialize() {
    // Initialize sidenav
    const sidenavElems = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenavElems);
    
    // Initialize modals
    const modalElems = document.querySelectorAll('.modal');
    M.Modal.init(modalElems);
    
    // Initialize tooltips
    const tooltipElems = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltipElems);
    
    // Initialize dropdowns
    const dropdownElems = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(dropdownElems);
    
    // Initialize select elements
    const selectElems = document.querySelectorAll('select');
    M.FormSelect.init(selectElems);
    
    // Initialize datepicker
    const datepickerElems = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepickerElems, {
        format: 'yyyy-mm-dd',
        yearRange: [1950, new Date().getFullYear() - 16]
    });
    
    // Initialize character counter
    const characterCounterElems = document.querySelectorAll('input[data-length], textarea[data-length]');
    M.CharacterCounter.init(characterCounterElems);
}

function setupMessages() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('#messages .card-panel');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Close message on click
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const message = this.closest('.card-panel');
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        });
    });
}

function setupAjaxForms() {
    // Contact form AJAX submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitContactForm(this);
        });
    }
    
    // Profile form AJAX submission
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitProfileForm(this);
        });
    }
}

function setupModuleRegistration() {
    // Module registration buttons
    const registerButtons = document.querySelectorAll('.register-btn');
    registerButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const moduleCode = this.dataset.moduleCode;
            registerForModule(moduleCode, this);
        });
    });
    
    // Module unregistration buttons
    const unregisterButtons = document.querySelectorAll('.unregister-btn');
    unregisterButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const moduleCode = this.dataset.moduleCode;
            unregisterFromModule(moduleCode, this);
        });
    });
}

function submitContactForm(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';
    
    fetch('/api/contact/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('Message sent successfully!', 'success');
            form.reset();
        } else {
            showMessage('Error sending message. Please try again.', 'error');
        }
    })
    .catch(error => {
        showMessage('Error sending message. Please try again.', 'error');
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.textContent = 'Send Message';
    });
}

function submitProfileForm(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = 'Updating...';
    
    fetch('/api/students/' + getCurrentUserId() + '/', {
        method: 'PATCH',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            showMessage('Profile updated successfully!', 'success');
        } else {
            showMessage('Error updating profile. Please try again.', 'error');
        }
    })
    .catch(error => {
        showMessage('Error updating profile. Please try again.', 'error');
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.textContent = 'Update Profile';
    });
}

function registerForModule(moduleCode, button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.textContent = 'Registering...';
    
    fetch(`/api/modules/${moduleCode}/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "enrolled" || data.student || data.id) {
            showMessage('Successfully registered for module!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showMessage(data.message || 'Error registering for module.', 'error');
            button.disabled = false;
            button.textContent = originalText;
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        showMessage('Error registering for module. Please try again.', 'error');
        button.disabled = false;
        button.textContent = originalText;
    });
}

function unregisterFromModule(moduleCode, button) {
    // Show confirmation dialog only once
    if (!confirm('Are you sure you want to unregister from this module?')) {
        return;
    }
    
    const originalText = button.textContent;
    button.disabled = true;
    button.textContent = 'Unregistering...';
    
    fetch(`/api/modules/${moduleCode}/unregister/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "unregistered") {
            showMessage('Successfully unregistered from module!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showMessage(data.message || 'Error unregistering from module.', 'error');
            button.disabled = false;
            button.textContent = originalText;
        }
    })
    .catch(error => {
        console.error('Unregistration error:', error);
        showMessage('Error unregistering from module. Please try again.', 'error');
        button.disabled = false;
        button.textContent = originalText;
    });
}

function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `card-panel ${type === 'success' ? 'green' : 'red'} lighten-1 white-text`;
    messageDiv.innerHTML = `
        <span>${message}</span>
        <i class="material-icons right close-message" style="cursor: pointer;">close</i>
    `;
    
    const messagesContainer = document.getElementById('messages') || createMessagesContainer();
    messagesContainer.appendChild(messageDiv);
    
    // Setup close button
    const closeButton = messageDiv.querySelector('.close-message');
    closeButton.addEventListener('click', function() {
        messageDiv.style.opacity = '0';
        setTimeout(() => messageDiv.remove(), 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.style.opacity = '0';
            setTimeout(() => messageDiv.remove(), 300);
        }
    }, 5000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.id = 'messages';
    document.body.appendChild(container);
    return container;
}

function getCSRFToken() {
    // First try to get from window variable set in template
    if (window.csrfToken) {
        return window.csrfToken;
    }
    
    // Fallback to cookie method
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

function getCurrentUserId() {
    // This should be set in the template or retrieved from an API
    return window.currentUserId || null;
}

// Search functionality
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }
}

function performSearch(query) {
    if (!query.trim()) {
        return;
    }
    
    fetch(`/api/modules/?search=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
        updateSearchResults(data.results);
    })
    .catch(error => {
        console.error('Search error:', error);
    });
}

function updateSearchResults(modules) {
    const container = document.getElementById('search-results');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (modules.length === 0) {
        container.innerHTML = '<p class="center">No modules found.</p>';
        return;
    }
    
    modules.forEach(module => {
        const moduleCard = createModuleCard(module);
        container.appendChild(moduleCard);
    });
}

function createModuleCard(module) {
    const card = document.createElement('div');
    card.className = 'col s12 m6 l4';
    card.innerHTML = `
        <div class="card module-card">
            <div class="card-content">
                <span class="card-title">${module.name}</span>
                <p><strong>Code:</strong> ${module.code}</p>
                <p><strong>Credits:</strong> ${module.credits}</p>
                <p><strong>Category:</strong> ${module.category}</p>
                <p>${module.description.substring(0, 100)}...</p>
            </div>
            <div class="card-action">
                <a href="/modules/${module.code}/" class="btn blue">View Details</a>
            </div>
        </div>
    `;
    return card;
}
