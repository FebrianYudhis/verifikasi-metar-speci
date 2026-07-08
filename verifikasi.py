from metar import Metar
import re
import sys

def check_basic_format(metar_str, metar):
    if not metar.type:
        return "METAR Tidak Valid: Format Tulisan METAR Tidak Valid"
    if len(metar.station_id) != 4:
        return "METAR Tidak Valid: Kode ICAO Harus Terdiri Dari 4 Karakter"
    if not metar_str.endswith("="):
        return "METAR Tidak Valid: METAR Harus Diakhiri Dengan Karakter '='"
    if " =" in metar_str:
        return "METAR Tidak Valid: Tidak Boleh Ada Spasi Antara '=' Dan Karakter Sebelumnya"
    return None

def check_time(metar):
    if not metar.time:
        return "METAR Tidak Valid: Waktu Tidak Valid"
    
    time_str = metar.time.strftime("%d%H%M")
    minute = time_str[4:6]
    
    if metar.type == "SPECI" and minute in ['00', '30']:
        return "METAR Tidak Valid: Waktu SPECI Tidak Boleh Pada Menit 00 Dan 30"
    if metar.type == "METAR" and minute not in ['00', '30']:
        return "METAR Tidak Valid: Penulisan METAR Dilaporkan Dalam Jam Penuh Dan Setengah"
    return None

def check_wind(metar):
    speed_str = str(metar.wind_speed)
    if "knots" not in speed_str:
        return "METAR Tidak Valid: Kelompok DDDFF Terdiri Dari 5 Karakter Diakhiri Satuan KT"

    if metar.wind_gust:
        gust_speed = metar.wind_gust.value()
        avg_speed = metar.wind_speed.value()
        if gust_speed - avg_speed < 10:
            return "METAR Tidak Valid: Nilai Gusty Harus >= 10 Knot Dari Kecepatan Angin Rata-Rata"
    return None

def check_visibility_and_weather(metar, metar_str):
    if not metar.vis:
        return "METAR Tidak Valid: Nilai Visibility Tidak Ada"

    visibility = metar.vis.value()
    
    if visibility <= 5000 and not metar.weather:
        return "METAR Tidak Valid: Kelompok WW Belum Dilaporkan Ketika Jarak Pandang 5000 M Atau Kurang"

    ww_fg = False
    ww_hz_br = False
    for weather_component in metar.weather:
        if len(weather_component) >= 4:
            if weather_component[3] == 'FG':
                ww_fg = True
            elif weather_component[3] in ['HZ', 'BR']:
                ww_hz_br = True
                
    if visibility > 1000 and ww_fg:
        return "METAR Tidak Valid: Sandi FG Dilaporkan Jika Jarak Pandang Kurang Dari 1000 M"
        
    if (visibility < 1000 or visibility > 5000) and ww_hz_br:
        return "METAR Tidak Valid: Sandi HZ Dan BR Dilaporkan Jika Jarak Pandang 5000 M Atau Kurang"
        
    return None

def check_clouds(metar, metar_str):
    if 'CAVOK' in metar_str:
        if metar.vis and re.search(r'\b\d{4}\b', metar_str):
            return "METAR Tidak Valid: Jika CAVOK Dilaporkan, Format Visibility Dikosongkan"
        if any(cloud in metar_str for cloud in ['FEW', 'SCT', 'BKN', 'OVC']):
            return "METAR Tidak Valid: Jika CAVOK Dilaporkan, Format Awan Dikosongkan"
        return None
        
    if 'NSC' in metar_str:
        if not metar.vis:
            return "METAR Tidak Valid: Jika NSC Dilaporkan, Visibility Harus Ada"
        if metar.vis.value() > 9000:
            return "METAR Tidak Valid: Jika NSC Dilaporkan, Visibility Maksimal 9000"
        if any(cloud in metar_str for cloud in ['FEW', 'SCT', 'BKN', 'OVC']):
            return "METAR Tidak Valid: Jika NSC Dilaporkan, Format Awan Dikosongkan"
        return None

    # Normal clouds check
    pattern_awan = re.compile(r'\b(FEW|SCT|BKN|OVC)\d{3}(CB|TCU)?\b')
    if not pattern_awan.findall(metar_str):
        return "METAR Tidak Valid: Format Pelaporan Kelompok Awan Tidak Sesuai"
        
    cloud_coverage_priority = {'FEW': 1, 'SCT': 2, 'BKN': 3, 'OVC': 4}
    cloud_data = [
        (cloud[0], cloud[1].value(), 'CB' if cloud[2] and 'CB' in cloud[2] else 'TCU' if cloud[2] and 'TCU' in cloud[2] else '') 
        for cloud in metar.sky 
        if cloud[1] is not None and cloud[1].value() is not None
    ]
    
    if len(cloud_data) >= 2:
        sorted_cloud_data = sorted(
            cloud_data,
            key=lambda x: (x[2] == '', x[1], cloud_coverage_priority.get(x[0], 5))
        )
        if cloud_data != sorted_cloud_data:
            return "METAR Tidak Valid: Urutan Pelaporan Kelompok Awan Harus Dimulai Dari Awan Signifikan Dan Lapisan Terendah Ke Tertinggi"
            
        for i in range(1, len(sorted_cloud_data)):
            current_cloud = sorted_cloud_data[i]
            previous_cloud = sorted_cloud_data[i-1]
            if current_cloud[2] == '' and previous_cloud[2] == '':
                if cloud_coverage_priority[previous_cloud[0]] > cloud_coverage_priority[current_cloud[0]]:
                    return "METAR Tidak Valid: Lapisan Awan Dengan Ketinggian Lebih Rendah Tidak Boleh Memiliki Cakupan Lebih Luas Dari Lapisan Awan Yang Lebih Tinggi"
                    
    # Check TS requires CB
    has_ts = False
    has_cb = any(len(c) >= 3 and c[2] == 'CB' for c in metar.sky)
    
    for weather_component in metar.weather:
        if len(weather_component) >= 3:
            w = weather_component
            if (w[0] in ['+', '-'] and w[1] == 'TS' and w[2] == 'RA') or \
               (w[1] == 'TS' and w[2] == 'RA') or \
               (w[0] == 'VC' and w[1] in ['TS', 'SH']) or \
               (w[1] == 'TS'):
                has_ts = True
                break
                
    if has_ts and not has_cb:
        return "METAR Tidak Valid: Jika Ada +TSRA, TSRA, -TSRA, VCTS, VCSH, Dan TS Maka Kelompok Awan Perlu Ditambahkan CB Di Bagian Akhir"

    return None

def check_temp_dewpoint(metar, metar_str):
    if not metar.temp:
        return "METAR Tidak Valid: Nilai Suhu Udara Tidak Ada"
    if not metar.dewpt:
        return "METAR Tidak Valid: Nilai Titik Embun Tidak Ada"
        
    temp = metar.temp.value()
    dew_point = metar.dewpt.value()
    if temp < dew_point:
        return "METAR Tidak Valid: Suhu Udara Tidak Boleh Lebih Tinggi Dari Titik Embun"

    pattern_suhu_dewpoint = re.compile(r'\b\d{2}/\d{2}\b')
    if not pattern_suhu_dewpoint.search(metar_str):
        return "METAR Tidak Valid: Format Pelaporan Kelompok Temp-Dewpt Tidak Sesuai"
        
    return None

def check_pressure(metar, metar_str):
    pressure = metar.press.value()
    if pressure < 900 or pressure > 1100:
        return "METAR Tidak Valid: Nilai Tekanan Udara Dilaporkan Di Luar Batas Yang Diharapkan"

    pattern_tekanan_udara = re.compile(r'\bQ\d{4}\b')
    if not pattern_tekanan_udara.search(metar_str):
        return "METAR Tidak Valid: Format Pelaporan Kelompok Tekanan Udara Tidak Sesuai"
        
    return None

def check_trend(metar, metar_str):
    if 'AUTO' not in metar_str:
        trend = metar._trend_groups
        if not trend:
            return "METAR Tidak Valid: Tidak Ada Kelompok Trend Yang Ditemukan"
        elif len(trend) == 1 and trend[0] != 'NOSIG':
            return "METAR Tidak Valid: Kelompok Trend Tidak Sesuai"
        elif len(trend) == 4:
            jam_metar = metar.time.strftime("%d%H%M")[-4:]
            jam_trend = metar._trend_groups[1][-4:]
            if int(jam_trend) <= int(jam_metar):
                return "METAR Tidak Valid: Jam Pengiriman METAR Dan Jam Trend Sama"
    return None

def validate_metar(metar_str):
    try:
        metar_str = metar_str.strip()
        
        # Format awal checking
        if not (metar_str.startswith("METAR") or metar_str.startswith("SPECI")):
            return "METAR Tidak Valid: Teks Harus Dimulai Dengan 'METAR' Atau 'SPECI'"
            
        metar = Metar.Metar(metar_str)
        
        checks = [
            lambda: check_basic_format(metar_str, metar),
            lambda: check_time(metar),
            lambda: check_wind(metar),
            lambda: check_visibility_and_weather(metar, metar_str),
            lambda: check_clouds(metar, metar_str),
            lambda: check_temp_dewpoint(metar, metar_str),
            lambda: check_pressure(metar, metar_str),
            lambda: check_trend(metar, metar_str)
        ]
        
        for check in checks:
            error = check()
            if error:
                return error
                
        return "METAR Valid"

    except Metar.ParserError as e:
        return f"METAR Tidak Valid: Format Sandi METAR Tidak Sesuai ({e})"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mengambil input METAR dari command line argument
        metar_string = sys.argv[1]
        result = validate_metar(metar_string)
        print(result)
    else:
        print("Tidak ada data METAR yang diberikan. Gunakan: python verifikasi.py 'METAR ...'")
