// Custom JavaScript for the chat application

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Show error messages using daisyUI toast
                const firstInvalidInput = form.querySelector(':invalid');
                if (firstInvalidInput) {
                    showToast(firstInvalidInput.validationMessage, 'error');
                }
            }
        });

        // Real-time validation feedback
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (!this.checkValidity()) {
                    this.classList.add('input-error');
                    const label = this.closest('.form-control').querySelector('.label-text-alt');
                    if (label) {
                        label.classList.remove('text-info');
                        label.classList.add('text-error');
                    }
                } else {
                    this.classList.remove('input-error');
                    const label = this.closest('.form-control').querySelector('.label-text-alt');
                    if (label) {
                        label.classList.remove('text-error');
                        label.classList.add('text-info');
                    }
                }
            });
        });
    });
});

// Theme toggle
function toggleTheme() {
    const html = document.querySelector('html');
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    // Update the theme toggle button state
    const themeController = document.querySelector('.theme-controller');
    if (themeController) {
        themeController.checked = newTheme === 'light';
    }
}

// Initialize theme from localStorage
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.querySelector('html').setAttribute('data-theme', savedTheme);
    
    // Initialize theme toggle button state
    const themeController = document.querySelector('.theme-controller');
    if (themeController) {
        themeController.checked = savedTheme === 'light';
    }
});

// Toast notification helper
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} fade-in fixed bottom-4 right-4 z-50`;
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Password strength indicator
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updatePasswordStrengthIndicator(strength);
        });
    }
});

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    return strength;
}

function updatePasswordStrengthIndicator(strength) {
    const indicator = document.getElementById('password-strength');
    if (indicator) {
        const strengthText = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong'];
        const strengthColors = ['error', 'warning', 'info', 'success', 'success'];
        indicator.textContent = `Password Strength: ${strengthText[strength - 1] || ''}`;
        indicator.className = `text-sm text-${strengthColors[strength - 1] || 'error'}`;
    }
} 