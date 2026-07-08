<?php
// Mengembalikan data dalam format JSON
header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $metar = $_POST['metar'] ?? '';

    // Gunakan escapeshellarg untuk keamanan passing argumen di command line
    $arg = escapeshellarg($metar);
    
    // Menggunakan Python dari dalam virtual environment (.venv) agar terisolasi dan mandiri
    $pythonPath = ".venv\Scripts\python.exe"; // Untuk Windows
    // Jika nanti di-hosting ke server Linux, ubah menjadi: $pythonPath = ".venv/bin/python";

    $output = shell_exec("$pythonPath verifikasi.py $arg");
    
    if ($output !== null) {
        $pesan = trim($output);
        
        // Sesuaikan ikon/status berdasarkan pesan kembalian Python
        if (strpos($pesan, 'Tidak Valid') !== false) {
            echo json_encode(["status" => "error", "message" => $pesan]);
        } else {
            echo json_encode(["status" => "success", "message" => $pesan]);
        }
    } else {
        echo json_encode(["status" => "error", "message" => "Gagal memproses validasi dengan Python."]);
    }
}
