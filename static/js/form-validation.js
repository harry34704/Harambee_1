class FormValidator {
    constructor() {
        this.forms = document.querySelectorAll('form[data-validate]');
        this.validationRules = {
            name: {
                pattern: /^[a-zA-Z\s]{2,}$/,
                message: 'Please enter a valid name (minimum 2 characters, letters only)'
            },
            email: {
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Please enter a valid email address'
            },
            phone: {
                pattern: /^(\+27|0)[1-9][0-9]{8}$/,
                message: 'Please enter a valid South African phone number'
            },
            id_number: {
                pattern: /^[0-9]{13}$/,
                message: 'Please enter a valid 13-digit ID number'
            },
            student_number: {
                pattern: /^[0-9A-Z]{6,12}$/,
                message: 'Please enter a valid student number'
            },
            password: {
                pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/,
                message: 'Password must be at least 8 characters with letters and numbers'
            }
        };

        this.initialize();
    }

    initialize() {
        this.forms.forEach(form => {
            // Add real-time validation
            form.querySelectorAll('input, select, textarea').forEach(field => {
                field.addEventListener('input', () => this.validateField(field));
                field.addEventListener('blur', () => this.validateField(field));
            });

            // Add form submission handling
            form.addEventListener('submit', (e) => this.handleSubmit(e, form));
        });
    }

    validateField(field) {
        const fieldName = field.getAttribute('name');
        const rule = this.validationRules[fieldName];
        
        if (!rule) return true;

        const isValid = rule.pattern.test(field.value);
        this.toggleFieldValidation(field, isValid, rule.message);
        return isValid;
    }

    toggleFieldValidation(field, isValid, message) {
        const feedback = field.nextElementSibling?.classList.contains('invalid-feedback') 
            ? field.nextElementSibling 
            : this.createFeedbackElement();

        field.classList.toggle('is-valid', isValid);
        field.classList.toggle('is-invalid', !isValid);
        
        if (!isValid) {
            feedback.textContent = message;
            if (!field.nextElementSibling?.classList.contains('invalid-feedback')) {
                field.parentNode.insertBefore(feedback, field.nextSibling);
            }
        } else {
            feedback.remove();
        }
    }

    createFeedbackElement() {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        return feedback;
    }

    async handleSubmit(e, form) {
        e.preventDefault();
        
        const isValid = Array.from(form.elements).every(field => {
            if (field.getAttribute('name')) {
                return this.validateField(field);
            }
            return true;
        });

        if (!isValid) {
            this.showFormError('Please correct the errors before submitting');
            return;
        }

        const submitButton = form.querySelector('button[type="submit"]');
        this.setSubmitButtonLoading(submitButton, true);

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    this.showFormSuccess('Form submitted successfully!');
                    form.reset();
                }
            } else {
                throw new Error('Form submission failed');
            }
        } catch (error) {
            this.showFormError('An error occurred. Please try again.');
            console.error('Form submission error:', error);
        } finally {
            this.setSubmitButtonLoading(submitButton, false);
        }
    }

    setSubmitButtonLoading(button, isLoading) {
        if (!button) return;
        
        const originalText = button.dataset.originalText || button.textContent;
        if (isLoading) {
            button.dataset.originalText = originalText;
            button.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Processing...
            `;
            button.disabled = true;
        } else {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    showFormError(message) {
        this.showToast(message, 'danger');
    }

    showFormSuccess(message) {
        this.showToast(message, 'success');
    }

    showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        const container = document.querySelector('.toast-container') || this.createToastContainer();
        container.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }
}

// Initialize form validation
document.addEventListener('DOMContentLoaded', () => {
    new FormValidator();
});
