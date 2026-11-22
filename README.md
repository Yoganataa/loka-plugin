# Loka Plugin

Katalog Source Plugin untuk [Loka Browser](https://github.com/yoganataa/loka-browser): browser Android berbasis GeckoView dengan katalog source ala Mihon.

> **Status: rancangan awal.** Repositori ini belum berisi source nyata. Katalog dan source di prototipe Loka Browser hanyalah demo fiktif dan **tidak** dipindahkan ke sini.

## Cara kerja

Satu source = satu folder berisi `manifest.json` (metadata, host, izin) dan `source.js` (logika membaca satu situs). CI memvalidasi setiap source, membangun paket zip dan `index.json` (dengan `sha256`), lalu menerbitkannya lewat GitHub Pages. Kontrak source: [docs/SOURCE_PLUGIN_SPEC.md](docs/SOURCE_PLUGIN_SPEC.md) (dimiliki repositori aplikasi; salinan di sini).

URL katalog setelah Pages aktif (konfirmasi dulu): `https://yoganataa.github.io/loka-plugin/index.json`

## Struktur

```
sources/<id>/            manifest.json + source.js (+ README.md opsional)
templates/               templat source baru (tidak ikut diterbitkan)
tools/validate.py        validasi semua source
tools/build_index.py     bangun dist/index.json + dist/packages/*.zip
docs/                    kontrak source, format data, kebijakan konten
.github/workflows/       validate (tiap PR), publish (merge ke main)
```

## Perintah

```bash
python3 tools/validate.py
python3 tools/build_index.py https://yoganataa.github.io/loka-plugin --out dist
```

Python 3.10+, tanpa dependensi.

## Menambah source

Baca [CONTRIBUTING.md](CONTRIBUTING.md) dan [docs/CONTENT_POLICY.md](docs/CONTENT_POLICY.md). Salin `templates/` ke `sources/<id>/`, isi, jalankan validator, ajukan PR.

## Pernyataan tanggung jawab

Pengembang hanya menyediakan alat ini. Penggunaan alat untuk melanggar hukum, hak cipta, atau ketentuan situs oleh pengguna, penyedia katalog pihak ketiga, atau pihak yang mem-fork proyek adalah tanggung jawab mereka sendiri. Source tidak melewati CAPTCHA, paywall, atau DRM. (Teks ini draf; peninjauan hukum disarankan sebelum rilis publik.)

## Lisensi

PolyForm Noncommercial 1.0.0: penggunaan komersial membutuhkan izin tertulis dari pemilik. Lihat [LICENSE](LICENSE). **Penting:** berkas LICENSE saat ini masih berisi catatan, bukan teks lengkap; jalankan `sh scripts/fetch-license.sh` untuk melengkapinya.
