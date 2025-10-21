// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });

    // Confirmation for delete actions
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.getAttribute('onsubmit').match(/'([^']+)'/)[1];
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form.form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = this.querySelectorAll('[required]');
            let isValid = true;

            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#ef4444';
                } else {
                    input.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });

    // Auto-focus first input on form pages
    const firstInput = document.querySelector('.form input:not([type="hidden"]):not([disabled])');
    if (firstInput) {
        firstInput.focus();
    }

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Grade input validation
    const gradeInput = document.getElementById('grade');
    const assignmentSelect = document.getElementById('assignment_id');

    if (gradeInput && assignmentSelect) {
        assignmentSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const maxPoints = selectedOption.text.match(/Max: (\d+)/);
            if (maxPoints) {
                gradeInput.setAttribute('max', maxPoints[1]);
                gradeInput.placeholder = `Enter grade (0-${maxPoints[1]})`;
            }
        });

        gradeInput.addEventListener('input', function() {
            const max = parseFloat(this.getAttribute('max'));
            const value = parseFloat(this.value);

            if (value > max) {
                this.value = max;
            }
            if (value < 0) {
                this.value = 0;
            }
        });
    }

    // Search form enhancement
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('.search-input');
        searchForm.addEventListener('submit', function(e) {
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
});

// Utility function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Add loading state to buttons
document.addEventListener('DOMContentLoaded', function() {
    const submitButtons = document.querySelectorAll('button[type="submit"]');

    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.disabled = true;
                this.textContent = 'Processing...';

                setTimeout(() => {
                    this.disabled = false;
                    this.textContent = this.getAttribute('data-original-text') || 'Submit';
                }, 3000);
            }
        });

        button.setAttribute('data-original-text', button.textContent);
    });
});
