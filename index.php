<?php
session_start();
?>

<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifikasi METAR dan SPECI</title>
    <link href="style.css" rel="stylesheet">
</head>

<body>
    <!-- Animasi Background Latar Belakang -->
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>

    <div class="glass-container">
        <div class="header">
            <h1>Verifikasi METAR & SPECI</h1>
            <p>Masukkan sandi laporan cuaca Anda di bawah ini</p>
        </div>

        <form action="proses.php" method="post">
            <div class="form-group">
                <label for="metar" class="form-label">Teks Sandi Laporan :</label>
                <input type="text" class="form-control" id="metar" placeholder="Cth: METAR WAGS 080230Z 13007KT..." name="metar" required autocomplete="off" spellcheck="false">
            </div>
            <button type="submit" class="btn">Validasi Sekarang</button>
        </form>
    </div>

    <div class="modal-overlay" id="modalOverlay">
        <div class="modal-content">
            <div id="modalIcon" class="modal-icon"></div>
            <h3 class="modal-title" id="modalTitle">Pesan Validasi</h3>
            <button class="modal-close" onclick="closeModal()">Tutup</button>
        </div>
    </div>

    <?php if (isset($_SESSION['pesan'])) : ?>
        <script>
            // Pass the PHP session data to JavaScript variables safely
            window.appMessage = <?= json_encode($_SESSION['pesan']) ?>;
            window.appType = <?= json_encode($_SESSION['tipeAlert']) ?>;
        </script>
        <?php unset($_SESSION['pesan']); ?>
        <?php unset($_SESSION['tipeAlert']); ?>
    <?php endif; ?>

    <script src="script.js"></script>
</body>

</html>