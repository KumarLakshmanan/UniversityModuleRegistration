// Custom JavaScript for University Module Registration System

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Count up animation for stats
    animateCountUp();

    // AJAX Module Registration/Unregistration
    setupModuleRegistration();

    // Form validation
    setupFormValidation();

    // Search functionality
    setupSearch();
});

// Count up animation for statistics
function animateCountUp() {
    $('.count-up').each(function() {
        var $this = $(this);
        var countTo = $this.attr('data-count');
        
        $({ countNum: $this.text() }).animate({
            countNum: countTo
        }, {
            duration: 2000,
            easing: 'linear',
            step: function() {
                $this.text(Math.floor(this.countNum));
            },
            complete: function() {
                $this.text(this.countNum);
            }
        });
    });
}

// AJAX Module Registration/Unregistration
function setupModuleRegistration() {
    // Registration button
    $(document).on('click', '.btn-register', function(e) {
        e.preventDefault();
        var $btn = $(this);
        var moduleCode = $btn.data('module');
        var url = $btn.data('url');
        
        $btn.prop('disabled', true);
        $btn.html('<span class="spinner-border spinner-border-custom me-2"></span>Registering...');
        
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    showAlert('success', response.message);
                    updateRegistrationButton($btn, 'unregister');
                    updateStudentCount(moduleCode, 1);
                } else {
                    showAlert('error', response.message);
                }
            },
            error: function() {
                showAlert('error', 'An error occurred. Please try again.');
            },
            complete: function() {
                $btn.prop('disabled', false);
            }
        });
    });
    
    // Unregistration button
    $(document).on('click', '.btn-unregister', function(e) {
        e.preventDefault();
        var $btn = $(this);
        var moduleCode = $btn.data('module');
        var url = $btn.data('url');
        
        if (!confirm('Are you sure you want to unregister from this module?')) {
            return;
        }
        
        $btn.prop('disabled', true);
        $btn.html('<span class="spinner-border spinner-border-custom me-2"></span>Unregistering...');
        
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    showAlert('success', response.message);
                    updateRegistrationButton($btn, 'register');
                    updateStudentCount(moduleCode, -1);
                } else {
                    showAlert('error', response.message);
                }
            },
            error: function() {
                showAlert('error', 'An error occurred. Please try again.');
            },
            complete: function() {
                $btn.prop('disabled', false);
            }
        });
    });
}

// Update registration button state
function updateRegistrationButton($btn, action) {
    if (action === 'register') {
        $btn.removeClass('btn-danger btn-unregister')
            .addClass('btn-primary btn-register')
            .html('<i class="fas fa-user-plus me-2"></i>Register')
            .data('url', $btn.data('register-url'));
    } else {
        $btn.removeClass('btn-primary btn-register')
            .addClass('btn-danger btn-unregister')
            .html('<i class="fas fa-user-minus me-2"></i>Unregister')
            .data('url', $btn.data('unregister-url'));
    }
}

// Update student count display
function updateStudentCount(moduleCode, change) {
    var $count = $('.student-count[data-module="' + moduleCode + '"]');
    if ($count.length) {
        var currentCount = parseInt($count.text()) || 0;
        $count.text(currentCount + change);
    }
}

// Show alert messages
function showAlert(type, message) {
    var alertClass = type === 'error' ? 'alert-danger' : 'alert-' + type;
    var iconClass = type === 'success' ? 'fa-check-circle' : 
                   type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    
    var alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas ${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.alert').remove(); // Remove existing alerts
    $('main').prepend('<div class="container mt-3">' + alertHtml + '</div>');
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 5000);
}

// Form validation
function setupFormValidation() {
    // Add custom validation styling
    $('form').on('submit', function() {
        var isValid = true;
        $(this).find('input[required], select[required], textarea[required]').each(function() {
            if (!$(this).val()) {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid').addClass('is-valid');
            }
        });
        
        if (!isValid) {
            showAlert('error', 'Please fill in all required fields.');
            return false;
        }
    });
    
    // Remove validation styling on input
    $('input, select, textarea').on('input change', function() {
        $(this).removeClass('is-invalid is-valid');
    });
}

// Search functionality
function setupSearch() {
    var searchTimer;
    
    $('#searchInput').on('input', function() {
        clearTimeout(searchTimer);
        var query = $(this).val();
        
        searchTimer = setTimeout(function() {
            if (query.length >= 2 || query.length === 0) {
                filterModules(query);
            }
        }, 300);
    });
}

// Filter modules based on search query
function filterModules(query) {
    $('.module-card').each(function() {
        var $card = $(this);
        var moduleName = $card.find('.card-title').text().toLowerCase();
        var moduleCode = $card.find('.module-code').text().toLowerCase();
        var moduleDescription = $card.find('.card-text').text().toLowerCase();
        
        if (query === '' || 
            moduleName.includes(query.toLowerCase()) || 
            moduleCode.includes(query.toLowerCase()) || 
            moduleDescription.includes(query.toLowerCase())) {
            $card.parent().show();
        } else {
            $card.parent().hide();
        }
    });
}

// Smooth scrolling for anchor links
$('a[href^="#"]').on('click', function(e) {
    e.preventDefault();
    var target = $(this.getAttribute('href'));
    if (target.length) {
        $('html, body').animate({
            scrollTop: target.offset().top - 70
        }, 1000);
    }
});

// Auto-hide alerts after 5 seconds
setTimeout(function() {
    $('.alert').not('.alert-important').fadeOut();
}, 5000);

// File upload preview
function setupFileUpload() {
    $('input[type="file"]').on('change', function() {
        var file = this.files[0];
        if (file && file.type.startsWith('image/')) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var preview = $(this).siblings('.preview-image');
                if (preview.length === 0) {
                    preview = $('<img class="preview-image img-thumbnail mt-2" style="max-width: 200px;">');
                    $(this).after(preview);
                }
                preview.attr('src', e.target.result);
            }.bind(this);
            reader.readAsDataURL(file);
        }
    });
}

// Initialize file upload on page load
$(document).ready(function() {
    setupFileUpload();
});

// Loading overlay
function showLoading() {
    var loadingHtml = `
        <div class="loading-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
             background: rgba(0,0,0,0.5); z-index: 9999; display: flex; align-items: center; justify-content: center;">
            <div class="spinner-border text-light" style="width: 3rem; height: 3rem;"></div>
        </div>
    `;
    $('body').append(loadingHtml);
}

function hideLoading() {
    $('.loading-overlay').remove();
}
