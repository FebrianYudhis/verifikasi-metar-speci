document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('metarForm');
    const input = document.getElementById('metar');
    const btn = form.querySelector('.btn');

    // 1. Auto-Uppercase (Huruf Besar Otomatis)
    input.addEventListener('input', function(e) {
        this.value = this.value.toUpperCase();
    });

    // 1.5. Bersihkan Sandi (Clear Input)
    const btnClear = document.getElementById('btnClear');
    if (btnClear) {
        btnClear.addEventListener('click', () => {
            input.value = '';
            input.focus();
        });
    }

    // 1.6. Salin Sandi (Copy Input)
    const btnCopy = document.getElementById('btnCopy');
    if (btnCopy) {
        btnCopy.addEventListener('click', async () => {
            if (!input.value.trim()) return;
            try {
                await navigator.clipboard.writeText(input.value);
                const originalText = btnCopy.textContent;
                btnCopy.textContent = 'Tersalin!';
                setTimeout(() => {
                    btnCopy.textContent = originalText;
                }, 1500);
            } catch (err) {
                console.error('Gagal menyalin teks: ', err);
            }
        });
    }

    // 2. Fetch API (AJAX Submit)
    form.addEventListener('submit', async (e) => {
        // Mencegah halaman me-reload
        e.preventDefault();

        // Tampilkan efek loading
        btn.classList.add('loading');
        const originalText = btn.textContent;
        btn.textContent = 'Memvalidasi...';
        btn.disabled = true;

        const formData = new FormData(form);

        try {
            // Mengirim request ke backend secara asinkron
            const response = await fetch('proses.php', {
                method: 'POST',
                body: formData
            });

            // Mendapatkan balasan JSON
            const data = await response.json();
            
            // Tampilkan custom modal
            showModal(data.status, data.message);
        } catch (error) {
            console.error('Error:', error);
            showModal('error', 'Terjadi kesalahan pada jaringan atau server.');
        } finally {
            // Kembalikan tombol ke kondisi semula
            btn.classList.remove('loading');
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });
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
