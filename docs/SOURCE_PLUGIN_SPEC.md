# Spesifikasi Source Plugin

> **Salinan** dari repositori aplikasi `yoganataa/loka-browser` (sumber kebenaran ada di sana). Rujukan seperti `docs/ARCHITECTURE.md` atau `HANDOFF.md` mengarah ke repositori itu.

Status: **rancangan v1, `apiVersion` 1**. Prototipe mensimulasikan kontrak ini; runtime nyata belum ada.

Source adalah paket dua berkas yang memberi tahu Loka cara membaca satu situs. Source **tidak** memuat UI; Loka (native) yang menggambar pustaka, pembaca, dan pemutar.

```
<id>/
  manifest.json   metadata, izin, host
  source.js       logika membaca situs
```

## manifest.json

| Bidang | Tipe | Aturan |
|---|---|---|
| `id` | string | `^[a-z0-9][a-z0-9-]{1,39}$`, unik di katalog |
| `name` | string | nama tampil |
| `version` | string | semver `MAJOR.MINOR.PATCH` |
| `lang` | string | kode bahasa (`id`, `en`, `ja`, atau `multi`) |
| `type` | string | salah satu: `komik anime film novel berita audio umum` |
| `apiVersion` | integer | versi kontrak yang dituju source |
| `hosts` | string[] | pola `https://domain/*`; hanya HTTPS |
| `permissions` | string[] | subset dari `session`, `storage` |
| `entry` | string | harus `source.js` |
| `description` | string | opsional, satu kalimat |

Izin:
- `session`: boleh memakai sesi masuk/cookie yang sama dengan tab untuk `hosts` miliknya.
- `storage`: penyimpanan kecil per-source (preferensi).
Tidak ada izin untuk host lain, berkas, atau jaringan bebas.

## Tipe dan jenis unit

| `type` | `unit.kind` bawaan | Pembaca/pemutar |
|---|---|---|
| `komik` | `pages` | pembaca halaman / webtoon |
| `anime`, `film` | `video` | pemutar video |
| `novel`, `berita` | `article` | pembaca artikel |
| `audio` | `audio` | pemutar audio |
| `umum` | salah satu | sesuai `kind` |

Tipe hanya mengatur pengorganisasian dan tampilan; perilaku pustaka/progres/pembaruan **sama** untuk semua tipe.

## source.js: antarmuka

Source mengekspor objek dengan fungsi asinkron. Semua mengembalikan data biasa (JSON-serializable); galat dilempar sebagai `SourceError`.

```js
export default {
  async search(query, page)    // -> { entries: Entry[], hasMore: boolean }
  async latest(page)           // -> { entries: Entry[], hasMore: boolean }   (opsional)
  async entry(entryId)         // -> EntryDetail
  async units(entryId)         // -> Unit[]            (urutan terbaru dulu atau lama dulu; Loka mengurutkan)
  async open(entryId, unitId)  // -> pages: {pages:[url]} | video: {streams:[{url,quality,type}]} | article: {html|text} | audio: {streams}
}
```

Tipe data:

```
Entry       { id, title, cover?, status? }
EntryDetail { id, title, cover?, status: "berlangsung"|"tamat", description?, tags?: string[] }
Unit        { id, number, title?, date?, kind?, dur?, tracks?, skip? }
```

- **`unit.id` stabil.** Deteksi pembaruan membandingkan himpunan `id`; id yang berubah dianggap unit baru. Jangan memakai indeks atau stempel waktu sebagai id.
- `status: "tamat"` menghentikan pengecekan pembaruan untuk entri itu.
- `dur` (detik), `tracks` (subtitle/audio), `skip` (`{from,to}` detik intro) opsional.

## Galat

`SourceError.code`:

| Kode | Arti | Perilaku Loka |
|---|---|---|
| `NEEDS_VERIFICATION` | situs meminta CAPTCHA/cek browser | tampilkan kartu verifikasi, buka tab; pengguna menyelesaikan sendiri; sesi dipakai bersama |
| `NEEDS_LOGIN` | butuh masuk | buka tab situs |
| `PAID` | konten berbayar/berlangganan | kartu berbayar; tidak diunduh/diakali |
| `DRM` | konten terproteksi DRM | tidak diputar; tampilkan penjelasan |
| `NOT_FOUND` | entri/unit hilang | tandai; tawarkan migrasi |
| `PARSE` | struktur situs berubah | source ditandai `rusak`; tawarkan lapor |
| `NETWORK` | jaringan | coba lagi nanti |

**Source tidak boleh** mencoba melewati `NEEDS_VERIFICATION`, `PAID`, atau `DRM`. Validator dan review menolak source yang melakukannya.

## Pembaruan

Pemeriksa (terjadwal) memanggil `units(entryId)` per entri pustaka dan membandingkan `id`. Dilewati: entri `tamat`, entri senyap (mute), source yang butuh verifikasi, rusak, atau tidak kompatibel (`apiVersion` di luar yang didukung Loka). Hasil masuk ke umpan "Pembaruan" dengan penghitung belum dibaca.

## Versi dan kompatibilitas

- Loka menyatakan rentang `apiVersion` yang didukung. Source di luar rentang tampil sebagai "tidak kompatibel" dan tidak dipanggil.
- Perubahan yang **menambah** bidang opsional: tetap `apiVersion` yang sama. Perubahan yang mengubah/menghapus bidang atau perilaku: naikkan `apiVersion`.
- Setiap perubahan kontrak memperbarui dokumen ini, `README.md`, validator, dan templat di skill `source-plugin`.

## Katalog

Katalog adalah tautan ke indeks JSON daftar source (id, nama, versi, tipe, bahasa, `apiVersion`, URL paket). Ditambah sekali lewat URL; source dipasang/dihapus di dalam Loka. Katalog pihak ketiga **tidak tepercaya**: pemasangan menampilkan izin dan host, dan memulihkan cadangan tidak menambah katalog.

Format indeks, penandatanganan, dan pemeriksaan integritas (hash) belum ditetapkan; lihat `docs/SECURITY.md` dan Keputusan di `docs/ARCHITECTURE.md`.

## Contoh minimal

Lihat `templates/` dan validasi dengan `python3 tools/validate.py`.
