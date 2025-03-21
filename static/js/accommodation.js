document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    // Handle filter buttons
    const filterButtons = document.querySelectorAll('.room-filters button');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            filterRooms(this.dataset.filter);
        });
    });

    // Handle sticky header
    window.addEventListener('scroll', function() {
        const sticky = document.querySelector('.sticky-top');
        if (window.scrollY > 100) {
            sticky.classList.add('scrolled');
        } else {
            sticky.classList.remove('scrolled');
        }
    });
});

function filterRooms(filter) {
    const rooms = document.querySelectorAll('.room-card');
    rooms.forEach(room => {
        if (filter === 'all') {
            room.style.display = 'block';
            return;
        }
        const roomType = room.dataset.type;
        room.style.display = roomType === filter ? 'block' : 'none';
    });
}

function openGallery(roomId) {
    const modal = new bootstrap.Modal(document.getElementById('galleryModal'));
    const carousel = document.querySelector('.carousel-inner');
    carousel.innerHTML = ''; // Clear existing images

    // Add gallery images (you would typically load these from your database)
    for (let i = 1; i <= 3; i++) {
        const item = document.createElement('div');
        item.className = `carousel-item${i === 1 ? ' active' : ''}`;
        item.innerHTML = `
            <img src="/static/images/room${roomId}_${i}.jpg" 
                 class="d-block w-100" 
                 alt="Room ${roomId} View ${i}">
        `;
        carousel.appendChild(item);
    }

    modal.show();
}

function bookRoom(roomId) {
    // Add loading state to button
    const button = event.target.closest('button');
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    button.disabled = true;

    // Simulate API call
    setTimeout(() => {
        window.location.href = `/apply?room=${roomId}`;
    }, 1000);
}