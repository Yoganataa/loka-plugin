# Kebijakan konten dan privasi (draf)

> **Salinan** dari repositori aplikasi `yoganataa/loka-browser` (sumber kebenaran ada di sana). Rujukan seperti `docs/ARCHITECTURE.md` atau `HANDOFF.md` mengarah ke repositori itu.

Status: **draf teknis dari tim produk, bukan nasihat hukum.** Minta peninjauan hukum sebelum rilis publik, terutama soal hak cipta, kewajiban penghapusan (takedown), dan syarat toko aplikasi. Pemilik yang memutuskan kebijakan akhirnya.

## Posisi Loka

Loka adalah browser dan pembaca. Loka tidak menyediakan, menghosting, atau mengunggah konten pihak ketiga. Source membaca situs seperti yang bisa dilakukan pengguna di browser, memakai sesi pengguna sendiri.

## Yang tidak dilakukan Loka (produk)

- Tidak melewati CAPTCHA, paywall, atau DRM. Verifikasi selesai oleh pengguna di tab.
- Tidak memutar konten DRM dan tidak mengunduh konten berlangganan/berbayar.
- Tidak menyertakan katalog bawaan yang berisi source untuk situs yang melanggar hak cipta (keputusan pemilik; lihat di bawah).
- Tidak memuat iklan atau pelacak milik Loka; tidak ada telemetri.

## Katalog bawaan (diputuskan 2026-11-21)

Seperti Mihon: Loka menyertakan satu katalog bawaan **dan** pengguna dapat menambah katalog pihak ketiga lewat URL. Katalog bawaan hidup di repositori terpisah `yoganataa/loka-plugin` (GitHub: indeks dan paket lewat Pages; lihat `docs/PLUGIN_REPO.md` dan `docs/DATA_FORMATS.md`).

Pemilik masih perlu menetapkan: isi awal katalog bawaan, siapa pemeliharanya, dan kriteria penerimaan (usulan di bawah). Katalog dan source di prototipe hanya demo fiktif untuk memudahkan agen; bukan isi katalog nyata.

**Catatan jujur tentang risiko.** Posisi "saya hanya menyediakan alat" paling kuat bila Loka tidak memilih isi katalog. Katalog bawaan yang dipelihara pemilik adalah kurasi oleh pemilik sendiri, sehingga isinya lebih mudah dikaitkan dengan pemilik daripada katalog pihak ketiga. Konsekuensi praktis: isi katalog bawaan sebaiknya ketat (kriteria di bawah), dan pertimbangkan katalog bawaan kecil yang hanya berisi source untuk konten legal, sementara katalog lain ditambah pengguna. Peninjauan hukum disarankan sebelum rilis publik.

## Kriteria penerimaan source (bila ada katalog bawaan)

- Izin minimal; host sesuai situs yang dibaca.
- Tidak mencoba melewati verifikasi, paywall, DRM, atau pembatasan akses.
- Tidak mengirim data pengguna ke pihak ketiga; tanpa telemetri.
- Tidak mengambil dari situs yang jelas melanggar hak cipta.
- Pemelihara dapat dihubungi; ada proses laporan dan penghapusan.

## Tanggung jawab (posisi pemilik)

Pemilik menyediakan alat. Penggunaan alat untuk melanggar hukum, hak cipta, atau ketentuan situs oleh pengguna, penyedia katalog pihak ketiga, atau pihak yang mem-fork proyek adalah tanggung jawab mereka sendiri, bukan pemilik. Pernyataan ini perlu muncul di README, di layar menambah katalog, dan di ketentuan penggunaan. Catatan: pernyataan seperti ini tidak otomatis membebaskan dari kewajiban hukum (mis. menanggapi laporan penghapusan, syarat toko aplikasi, hukum setempat); pengacara perlu memeriksa teks dan prosesnya.

## Katalog pihak ketiga

Tidak tepercaya. Loka menampilkan peringatan jelas saat menambah dan menampilkan izin/host saat memasang. Tanggung jawab atas isi katalog pihak ketiga ada pada penerbitnya; Loka menyediakan mekanisme melaporkan dan menghapus source.

## Penghapusan dan laporan

Tentukan: alamat laporan, waktu tanggap, dan mekanisme pencabutan source dari katalog bawaan dan, bila bisa, dari perangkat (Keputusan C di arsitektur). Belum ada.

## Privasi (prinsip)

- Tanpa telemetri atau analitik secara bawaan. Bila kelak ada pelaporan galat, harus opt-in dan terdokumentasi.
- Data pustaka, progres, dan riwayat tersimpan di perangkat. Sinkronisasi belum ada; bila ditambah, enkripsi ujung ke ujung dan opt-in.
- Loka Privat tidak menyimpan riwayat dan membuang progres saat keluar.
- Cadangan dibuat pengguna, disimpan di tempat pilihan pengguna.
- Fitur yang mengirim teks ke layanan luar (Tanya Loka, ringkasan) harus berlabel, atas tindakan pengguna, dan menyebut ke mana data pergi. Belum diputuskan.
- Siapkan kebijakan privasi publik sebelum rilis toko aplikasi.

## Rilis toko aplikasi

Kebijakan toko (mis. Play) mengatur browser, konten pihak ketiga, dan izin. Verifikasi syarat terbaru sebelum memilih jalur distribusi; F-Droid dan APK langsung punya aturan berbeda.
