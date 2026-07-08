# Aplikasi Verifikasi METAR dan SPECI

Aplikasi ini adalah sebuah tool berbasis web sederhana yang digunakan untuk memvalidasi format dan logika dari laporan cuaca **METAR** atau **SPECI**. Aplikasi ini dibangun menggunakan antarmuka PHP untuk kemudahan input dan script Python di backend untuk melakukan parsing dan validasi data secara mendalam.

## Fitur Utama

- **Antarmuka Web Premium**: Desain UI modern dengan efek _Glassmorphism Dark Mode_, dibangun sepenuhnya menggunakan Vanilla CSS tanpa framework eksternal.
- **Validasi Komprehensif**: Melakukan pengecekan terhadap berbagai komponen METAR/SPECI, antara lain:
  - Format awal laporan (`METAR` atau `SPECI`).
  - Kode ICAO Stasiun (4 karakter).
  - Format waktu dan kesesuaian menit laporan untuk SPECI/METAR.
  - Data angin (Arah, Kecepatan, _Gust_).
  - Jarak pandang (_Visibility_) dan kondisi CAVOK/NSC.
  - Fenomena cuaca (WW) dan kesesuaiannya dengan jarak pandang (misal: FG, HZ, BR, TS).
  - Format pelaporan awan, cakupan, dan urutan awan signifikan (CB/TCU).
  - Suhu Udara dan Titik Embun (Suhu tidak boleh lebih rendah dari titik embun).
  - Tekanan Udara (QNH) dalam batas normal (900 - 1100).
  - Kelompok _Trend_.
  - Karakter penutup `=` di akhir sandi.
- **Notifikasi Interaktif**: Custom Vanilla JS Modal untuk menampilkan hasil validasi (Valid/Tidak Valid beserta alasannya) dengan animasi yang mulus.

## Alur Kerja (How it Works)

1. Pengguna memasukkan teks sandi METAR atau SPECI pada form di halaman utama (`index.php`).
2. Data form dikirim ke `proses.php`.
3. `proses.php` mem-parsing data string dengan aman menggunakan `escapeshellarg()` dan mengeksekusi script Python (`verifikasi.py`) via _Command Line Interface_ (CLI).
4. Script Python membaca argumen tersebut, menggunakan library `metar` untuk mem-parsing data, dan menjalankan serangkaian validasi logika.
5. Hasil validasi (berupa teks) dikembalikan ke PHP dan ditampilkan kepada pengguna sebagai popup _alert_ yang aman dari XSS.

## Persyaratan Sistem (Prerequisites)

Untuk menjalankan aplikasi ini, Anda membutuhkan:

1. **Web Server dengan PHP**: Seperti Apache atau Nginx (bisa menggunakan perangkat lunak seperti XAMPP, Laragon, MAMP, dsb).
2. **Python 3.x**: Harus terinstal di sistem dan dapat dipanggil dari _Command Prompt_ atau _Terminal_ web server.
3. **Library Python `metar`**:
   Aplikasi ini mengandalkan library `metar` dari Python. Di dalam direktori proyek ini terdapat folder `.venv` yang merupakan _virtual environment_ Python. Pastikan _environment_ ini memiliki library yang dibutuhkan dengan menjalankan perintah berikut di terminal:
   `pip install -r requirements.txt`

## Cara Instalasi (Installation)

1. _Clone_ repositori ini atau salin seluruh folder proyek ke dalam direktori _document root_ web server Anda (misalnya folder `htdocs`, `www`, atau `public_html`).
2. Buka _Command Prompt_ atau _Terminal_ dan arahkan (menggunakan `cd`) ke direktori proyek tersebut.
3. Buat _Virtual Environment_ Python baru (jika belum ada) dengan menjalankan perintah:
   ```bash
   python -m venv .venv
   ```
4. Aktifkan _Virtual Environment_ tersebut:
   - **Di Windows (CMD / PowerShell):**
     ```cmd
     .venv\Scripts\activate
     ```
   - **Di Windows (Git Bash):**
     ```bash
     source .venv/Scripts/activate
     ```
   - **Di Linux/Mac:**
     ```bash
     source .venv/bin/activate
     ```
     ```bash
     source .venv/bin/activate
     ```
5. _Install_ semua dependensi _library_ yang dibutuhkan dengan mengeksekusi:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Penggunaan

1. Pastikan servis web server (PHP & Apache/Nginx) Anda dalam keadaan aktif.
2. Akses aplikasi melalui browser (contoh: `http://localhost/nama-folder-proyek`).
3. Masukkan sandi METAR/SPECI secara lengkap, diakhiri dengan tanda sama dengan (`=`).
   - Contoh valid: `METAR WAGS 080230Z 13007KT 090V180 9999 FEW009 30/24 Q1013 NOSIG=`
4. Klik tombol **Verifikasi**.
5. Notifikasi popup akan muncul memberitahu apakah METAR tersebut Valid atau jika Tidak Valid, bagian mana yang salah.

## Struktur File

- `index.php`: Halaman antarmuka utama (form input).
- `proses.php`: File PHP untuk menangani _submit_ form dan meneruskan argumen secara langsung (CLI) ke Python.
- `verifikasi.py`: Inti dari aplikasi, script Python yang berisi logika validasi METAR terstruktur.
- `style.css`: File kustom CSS (Vanilla) yang memuat gaya animasi dan tata letak _glassmorphism_.
- `script.js`: File kustom JavaScript untuk menangani logika kemunculan _modal alert_.
- `.venv/`: Direktori _virtual environment_ Python untuk mengeksekusi script secara terisolasi.
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan (_package list_).
- `.gitignore`: Aturan pengabaian file untuk Git (mengabaikan `.venv` dan file sementara lainnya).
