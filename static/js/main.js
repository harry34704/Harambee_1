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
    if (element.classList.contains('room-unavailable')) {
        return;
    }
    
    // Remove selected class from all rooms
    document.querySelectorAll('.room-selectable').forEach(room => {
        room.classList.remove('room-selected');
    });
    
    // Add selected class to clicked room
    element.classList.add('room-selected');
    
    // Update hidden input
    const roomId = element.getAttribute('data-room-id');
    document.getElementById('accommodation_preference').value = roomId;

    // Handle PI asset attachment
    fetch(`/static/attached_assets/pi/${roomId}`)
        .then(response => response.json())
        .then(data => {
            if (data.pi_assets) {
                // Update UI with PI assets if needed
                console.log('PI assets loaded:', data.pi_assets);
            }
        })
        .catch(error => console.error('Error loading PI assets:', error));
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

// Initialize any other necessary JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here
    console.log('DOM fully loaded and parsed');
});