// Handle file input display
document.querySelectorAll('.custom-file-input').forEach(input => {
    input.addEventListener('change', function(e) {
        const fileName = e.target.files[0].name;
        const label = this.nextElementSibling;
        label.textContent = fileName;
    });
});

// Handle maintenance request form
const maintenanceForm = document.getElementById('maintenanceForm');
if (maintenanceForm) {
    maintenanceForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(maintenanceForm);
        try {
            const response = await fetch('/maintenance/request', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.success) {
                alert('Maintenance request submitted successfully');
                maintenanceForm.reset();
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to submit maintenance request');
        }
    });
}

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Handle document upload preview
function previewDocument(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(input.getAttribute('data-preview'));
            if (preview) {
                preview.src = e.target.result;
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Handle room booking modal
const bookingModal = document.getElementById('bookingModal');
if (bookingModal) {
    bookingModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const roomId = button.getAttribute('data-room-id');
        const roomNumber = button.getAttribute('data-room-number');
        const modalTitle = bookingModal.querySelector('.modal-title');
        const roomInput = bookingModal.querySelector('#roomNumber');
        
        modalTitle.textContent = `Book Room ${roomNumber}`;
        roomInput.value = roomId;
    });
}

// Handle stripe payment
let stripe = Stripe(STRIPE_PUBLIC_KEY);
const paymentForm = document.getElementById('payment-form');
if (paymentForm) {
    paymentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const response = await fetch('/create-payment-intent', {
            method: 'POST',
        });
        const data = await response.json();
        const result = await stripe.confirmCardPayment(data.clientSecret, {
            payment_method: {
                card: elements.getElement('card'),
                billing_details: {
                    name: document.getElementById('name').value,
                }
            }
        });
        if (result.error) {
            alert(result.error.message);
        } else {
            window.location.href = '/payment-success';
        }
    });
}
