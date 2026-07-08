<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $_SESSION['tipeAlert'] = "error";
    $metar = $_POST['metar'] ?? '';

    // Gunakan escapeshellarg untuk keamanan passing argumen di command line
    $arg = escapeshellarg($metar);
    // Menggunakan Python dari dalam virtual environment (.venv) agar terisolasi dan mandiri
    $pythonPath = ".venv\Scripts\python.exe"; // Untuk Windows
    // Jika nanti di-hosting ke server Linux, ubah menjadi: $pythonPath = ".venv/bin/python";

    $output = shell_exec("$pythonPath verifikasi.py $arg");
    
    if ($output !== null) {
        $pesan = trim($output);
        $_SESSION['pesan'] = $pesan;
        
        // Sesuaikan ikon berdasarkan pesan kembalian Python
        if (strpos($pesan, 'Tidak Valid') !== false) {
            $_SESSION['tipeAlert'] = "error";
        } else {
            $_SESSION['tipeAlert'] = "success";
        }
    } else {
        $_SESSION['pesan'] = "Gagal memproses validasi dengan Python.";
    }

    header("Location: index.php");
}
