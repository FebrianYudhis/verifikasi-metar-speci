# Changelog

Semua perubahan yang signifikan pada proyek ini akan didokumentasikan di file ini.

Format changelog ini didasarkan pada [Keep a Changelog](https://keepachangelog.com/id/1.0.0/),
dan proyek ini menganut [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
