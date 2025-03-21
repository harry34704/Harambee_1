document.addEventListener('DOMContentLoaded', function() {
    // Handle file uploads with preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const preview = document.createElement('div');
            preview.className = 'file-preview mt-2';
            
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.className = 'img-thumbnail';
                img.style.maxHeight = '100px';
                img.src = URL.createObjectURL(file);
                preview.appendChild(img);
            } else {
                preview.innerHTML = `<i class="fas fa-file-pdf"></i> ${file.name}`;
            }
            
            const container = input.parentElement;
            const oldPreview = container.querySelector('.file-preview');
            if (oldPreview) container.removeChild(oldPreview);
            container.appendChild(preview);
        });
    });
});