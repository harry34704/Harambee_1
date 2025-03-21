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

function selectRoom(element) {
    console.log('Selecting room:', element.dataset.roomId);
    
    if (element.classList.contains('room-unavailable')) {
        console.log('Room is unavailable');
        return;
    }
    
    // Remove selected class from all rooms
    document.querySelectorAll('.room-block').forEach(room => {
        room.classList.remove('selected');
    });
    
    // Add selected class to clicked room
    element.classList.add('selected');
    
    // Update hidden input
    const roomId = element.dataset.roomId;
    const preferenceInput = document.getElementById('accommodation_preference');
    if (preferenceInput) {
        preferenceInput.value = roomId;
        console.log('Updated preference to:', roomId);
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

// Handle payment proof upload preview
const paymentProofInput = document.getElementById('payment_proof');
// Payment proof upload preview
if (paymentProofInput) {
    paymentProofInput.addEventListener('change', function() {
        previewDocument(this);
    });
}

function enlargeImage(img) {
    var enlargedImage = document.createElement('div');
    enlargedImage.className = 'enlarged-image';
    enlargedImage.innerHTML = '<img src="' + img.src + '" alt="' + img.alt + '">';
    document.body.appendChild(enlargedImage);
    enlargedImage.style.display = 'block';
    enlargedImage.onclick = function() {
        document.body.removeChild(enlargedImage);
    };
}

function applyForAccommodation() {
    // Implement the logic to apply for accommodation
    alert('Application process started.');
}

// Initialize any other necessary JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here
    console.log('DOM fully loaded and parsed');
    
    // Check application state and redirect if necessary
    fetch('/api/check_application_state')
        .then(response => response.json())
        .then(data => {
            if (data.incomplete_application) {
                window.location.href = '/resume_application';
            }
        })
        .catch(error => console.error('Error checking application state:', error));
    
    console.log('Checking for room blocks...');
    const roomBlocks = document.querySelectorAll('.room-block');
    console.log('Found room blocks:', roomBlocks.length);

    // Initialize Bootstrap tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    // Handle flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            const alert = bootstrap.Alert.getInstance(message);
            if (alert) {
                alert.close();
            }
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading indicator to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });

    // Responsive image handling
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            this.src = '/static/images/placeholder.png';
        });
    });
});

// Add page transition effects
window.addEventListener('beforeunload', function() {
    document.body.classList.add('page-transition');
});