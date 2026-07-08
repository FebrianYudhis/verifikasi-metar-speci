document.addEventListener('DOMContentLoaded', () => {
    // Mengecek apakah PHP mengirimkan variabel sesi (pesan) ke Javascript
    if (typeof window.appMessage !== 'undefined' && window.appMessage) {
        showModal(window.appType, window.appMessage);
    }
});

function showModal(type, message) {
    const overlay = document.getElementById('modalOverlay');
    const title = document.getElementById('modalTitle');
    const icon = document.getElementById('modalIcon');

    title.innerText = message;
    
    // Reset icon class
    icon.className = 'modal-icon';
    icon.innerHTML = '';

    if (type === 'error') {
        icon.classList.add('icon-error');
        // SVG Icon untuk Error (X)
        icon.innerHTML = `<svg width="30" height="30" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path></svg>`;
    } else {
        // SVG Icon untuk Info/Success (Centang)
        icon.classList.add('icon-info');
        icon.innerHTML = `<svg width="30" height="30" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg>`;
    }

    // Tampilkan modal
    overlay.classList.add('active');
}

function closeModal() {
    const overlay = document.getElementById('modalOverlay');
    overlay.classList.remove('active');
}
