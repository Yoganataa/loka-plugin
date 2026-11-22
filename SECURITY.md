# Keamanan

Source adalah kode pihak ketiga yang berjalan di aplikasi pengguna. Karena itu setiap source ditinjau, dibatasi izin dan host-nya, dan paketnya diterbitkan dengan `sha256`.

Melaporkan kerentanan atau source berbahaya: gunakan fitur *private vulnerability reporting* GitHub di repositori ini (aktifkan di Settings > Security), atau alamat kontak yang akan ditetapkan pemilik. Jangan membuka issue publik untuk kerentanan yang belum diperbaiki.

Aturan keras: tanpa telemetri, tanpa `eval`/`Function` dari string, tanpa memuat skrip dari luar `hosts`, tanpa jalan pintas verifikasi/paywall/DRM.
