# Berkontribusi ke Loka Plugin

1. Baca [docs/CONTENT_POLICY.md](docs/CONTENT_POLICY.md) (kriteria penerimaan) dan [docs/SOURCE_PLUGIN_SPEC.md](docs/SOURCE_PLUGIN_SPEC.md).
2. Salin `templates/` ke `sources/<id>/` (folder harus sama dengan `id` di manifest).
3. Isi manifest dan `source.js`. Izin dan host seminimal mungkin. `unit.id` harus stabil.
4. `python3 tools/validate.py` harus lulus.
5. Ajukan PR dengan templat PR. Naikkan `version` setiap `source.js` berubah.

Source **tidak boleh** mencoba melewati CAPTCHA, paywall, DRM, atau pembatasan akses; bila situs memintanya, lempar `NEEDS_VERIFICATION`, `PAID`, atau `DRM` dan berhenti. Peninjau menolak source yang melakukannya.

## Ketentuan kontribusi (draf; perlu tinjauan hukum)

Dengan mengirim kontribusi, Anda menyatakan Anda berhak mengirimkannya, dan memberi pemilik proyek lisensi yang tidak eksklusif, bebas royalti, tanpa batas waktu, untuk menggunakan, mengubah, dan melisensikan ulang kontribusi itu, termasuk untuk penggunaan komersial dan di bawah lisensi lain. Anda tetap memegang hak cipta kontribusi Anda. Kontribusi tersedia untuk publik di bawah lisensi proyek (PolyForm Noncommercial 1.0.0).

## Penghapusan

Pemilik hak atau pemilik situs yang ingin sebuah source dicabut dapat membuka issue atau menghubungi alamat laporan (belum ditetapkan; isi di sini sebelum rilis publik).
