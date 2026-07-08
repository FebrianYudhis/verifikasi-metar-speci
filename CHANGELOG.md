# Changelog

Semua perubahan yang signifikan pada proyek ini akan didokumentasikan di file ini.

Format changelog ini didasarkan pada [Keep a Changelog](https://keepachangelog.com/id/1.0.0/),
dan proyek ini menganut [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-08

### Added
- **Peningkatan UX**: Penambahan fitur konversi huruf besar otomatis (*Auto-uppercase*) saat pengguna mengetik sandi.
- **Peningkatan UX**: Tombol validasi kini memiliki animasi dan status *loading* saat sedang memproses data.
- **Peningkatan UX**: Penambahan tombol utilitas mungil "Salin" (untuk menyalin teks ke *clipboard*) dan "Bersihkan" (untuk menghapus teks) di sudut kanan form input.
- **API Backend**: File `proses.php` kini dapat diakses sebagai *Public Endpoint API* oleh aplikasi eksternal karena telah dibekali perlindungan CORS (`Access-Control-Allow-Origin: *`).
- **API Backend**: API kini mendukung penerimaan data via method HTTP `GET` (melalui URL) di samping method `POST`.
- **API Backend**: Implementasi balasan kode status HTTP (*HTTP Status Code*) standar seperti 200 OK, 400 Bad Request, dan 500 Server Error.
- **Dokumentasi**: Menambahkan seksi panduan dan tata cara penggunaan API pada file `README.md`.

### Changed
- **Optimasi Form (AJAX)**: Pengiriman formulir kini dieksekusi secara asinkron (*background*) tanpa memuat ulang halaman (*no-reload*) menggunakan `fetch` API.
- **Optimasi Variabel**: Mengubah nama parameter input form dan API dari `metar` menjadi `sandi` agar lebih fleksibel/umum untuk METAR maupun SPECI.
- **Refactor PHP**: Menghapus total ketergantungan pada *Session PHP* (`session_start()`) karena arsitektur komunikasi antara *frontend* dan *backend* kini sepenuhnya *stateless* (berbasis JSON).

## [1.0.0] - 2026-07-08

Ini adalah rilis awal (versi 1.0.0) dari Aplikasi Verifikasi METAR dan SPECI.

### Added
- Antarmuka web kustom menggunakan murni HTML dan CSS (Vanilla) dengan desain premium *Dark Mode Glassmorphism*.
- Efek animasi interaktif pada latar belakang (*floating blobs*), tombol, dan transisi layar.
- Sistem validasi backend menggunakan Python dan library `metar` untuk mengecek format ICAO, waktu, angin, visibilitas, fenomena cuaca, awan, suhu, dewpoint, tekanan, dan kelompok trend.
- Implementasi pengiriman data secara aman dari PHP ke Python melalui argumen *Command Line* (CLI) menggunakan `escapeshellarg()`.
- Pengamanan celah *Cross-Site Scripting* (XSS) di antarmuka web dengan memanfaatkan `json_encode()` saat menampilkan respons dari backend.
- *Modal Alert* kustom berbasis Vanilla Javascript (`script.js`) untuk menampilkan hasil verifikasi secara dinamis dan elegan tanpa bergantung pada library tambahan.
- Struktur *Clean Code* pada script Python (`verifikasi.py`) dengan pemisahan *helper functions* spesifik untuk masing-masing blok validasi cuaca.
