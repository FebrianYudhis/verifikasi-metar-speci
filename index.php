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

        <form id="metarForm">
            <div class="form-group">
                <div class="label-row">
                    <label for="metar" class="form-label">Teks Sandi Laporan :</label>
                    <div class="utility-buttons">
                        <button type="button" class="btn-small" id="btnCopy">Salin</button>
                        <button type="button" class="btn-small" id="btnClear">Bersihkan</button>
                    </div>
                </div>
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



    <script src="script.js"></script>
</body>

</html>