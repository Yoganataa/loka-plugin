# Format data

> **Salinan** dari repositori aplikasi `yoganataa/loka-browser` (sumber kebenaran ada di sana). Rujukan seperti `docs/ARCHITECTURE.md` atau `HANDOFF.md` mengarah ke repositori itu.

Dua bagian: yang **sudah ada di prototipe** (cadangan v1) dan yang **usulan** (indeks katalog, paket source). Usulan harus divalidasi di fase 3 dan boleh berubah; naikkan versinya bila berubah.

## Cadangan v1 (ada di prototipe)

```json
{
  "app": "loka",
  "version": 1,
  "exported": "2026-11-21T12:00:00.000Z",
  "installed": ["id-source"],
  "catalogs": ["https://contoh.org/katalog.json"],
  "cats": ["Favorit"],
  "lib": [
    { "source": "id-source", "title": "Judul", "read": ["unit-id"], "mute": false, "cats": ["Favorit"] }
  ],
  "settings": { "theme": "dark", "engine": "Google", "days": 1, "rdDir": "ltr" }
}
```

Aturan pemulihan (ikuti di native):
- Tolak bila `app !== "loka"`, `version !== 1`, atau `lib` bukan larik.
- `settings` hanya menerima kunci yang dikenal dengan nilai dari daftar putih; kunci lain diabaikan.
- `catalogs` **tidak** otomatis ditambahkan; tampilkan sebagai saran dengan konfirmasi.
- Nama kategori dipangkas (24 karakter) dan dedup tanpa peka huruf besar/kecil.
- Entri dari source yang belum terpasang/tak kompatibel dilewati dan dilaporkan jumlahnya.
- Posisi progres tidak termasuk di v1 (lihat Keputusan F di `docs/ARCHITECTURE.md`).
- Di native, `lib` mengacu entri lewat `source` + id entri yang stabil, bukan judul. Judul di prototipe hanya karena data demo; versi 2 harus menyertakan `entryId`.

## Indeks katalog (usulan v1)

```json
{
  "catalogVersion": 1,
  "name": "Nama Katalog",
  "sources": [
    {
      "id": "contoh-komik",
      "name": "Contoh Komik",
      "version": "1.0.0",
      "lang": "id",
      "type": "komik",
      "apiVersion": 1,
      "package": "https://contoh.org/pkg/contoh-komik-1.0.0.zip",
      "sha256": "<hash paket>",
      "hosts": ["https://komik.example.org/*"],
      "permissions": ["session"]
    }
  ]
}
```

- `hosts` dan `permissions` di indeks adalah **tampilan awal** untuk pengguna; yang berlaku adalah `manifest.json` di dalam paket. Jika berbeda, tolak pemasangan.
- `sha256` wajib diperiksa sebelum memasang. Tanda tangan (mis. kunci penerbit) belum diputuskan (Keputusan C).
- Katalog diambil lewat HTTPS saja.
- Hosting katalog bawaan (diputuskan): GitHub Pages menyajikan indeks JSON dan paket zip (`packages/`); CI di GitHub Actions membangun indeks, menghitung `sha256`, dan menjalankan validator manifest pada setiap source sebelum terbit. Repositori katalog: `yoganataa/loka-plugin` (lihat `docs/PLUGIN_REPO.md`).

## Paket source (usulan v1)

Berkas zip berisi tepat `manifest.json` dan `source.js` (tanpa berkas lain pada v1). Batas ukuran (mis. 1 MB) dan penolakan jalur berbahaya (`..`, jalur absolut) ditetapkan saat implementasi. Validasi manifest: `.agents/skills/source-plugin/scripts/validate_manifest.py` sebagai rujukan aturan.

## Skema basis data (usulan)

Lihat "Model data" di `docs/ARCHITECTURE.md`. Tambahkan nomor versi skema Room dan uji migrasi sejak migrasi pertama.
