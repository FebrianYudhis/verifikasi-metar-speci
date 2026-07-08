<?php
// Mengembalikan data dalam format JSON
header('Content-Type: application/json');
// Mengizinkan aplikasi lain/domain lain untuk melakukan fetch (CORS)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight request (CORS)
if ($_SERVER["REQUEST_METHOD"] == "OPTIONS") {
    http_response_code(200);
    exit(0);
}

// Menerima input metar dari method POST maupun GET (sehingga bisa diakses via URL)
$metar = $_POST['sandi'] ?? $_GET['sandi'] ?? '';

if (empty(trim($metar))) {
    http_response_code(400); // Bad Request
    echo json_encode(["status" => "error", "message" => "Parameter 'sandi' tidak boleh kosong."]);
    exit;
}

// Gunakan escapeshellarg untuk keamanan passing argumen di command line
$arg = escapeshellarg($metar);

// Menggunakan Python dari dalam virtual environment (.venv) agar terisolasi dan mandiri
$pythonPath = ".venv\Scripts\python.exe"; // Untuk Windows
// Jika nanti di-hosting ke server Linux, ubah menjadi: $pythonPath = ".venv/bin/python";

$output = shell_exec("$pythonPath verifikasi.py $arg");

if ($output !== null) {
    $pesan = trim($output);
    
    // Sesuaikan ikon/status dan HTTP Response Code berdasarkan pesan kembalian Python
    if (strpos($pesan, 'Tidak Valid') !== false) {
        http_response_code(400); // Bad Request (Validasi gagal)
        echo json_encode(["status" => "error", "message" => $pesan]);
    } else {
        http_response_code(200); // OK
        echo json_encode(["status" => "success", "message" => $pesan]);
    }
} else {
    http_response_code(500); // Internal Server Error
    echo json_encode(["status" => "error", "message" => "Gagal memproses validasi dengan Python."]);
}
