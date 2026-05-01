# Detective Game — CLI Python

Game detektif berbasis teks dengan kasus prosedural acak.  
A text-based detective game with fully randomized procedural cases.

---

## Cara Menjalankan / How to Run

```bash
python main.py
```

Tidak ada dependensi eksternal. Cukup Python 3.8+.  
No external dependencies. Python 3.8+ only.

---

## Struktur Proyek / Project Structure

```
detective_game/
> main.py
> game.py
> generator.py
> state.py
> utils.py
> data/
>    > lang_id.json
>    > lang_en.json
```

---

## Cara Bermain / Gameplay

1. Pilih bahasa (Indonesia / English)
2. Baca detail kasus yang muncul
3. Gunakan menu untuk:
   - **1** → Kunjungi TKP → dapatkan petunjuk (maks 3x)
   - **2** → Temui saksi → dengar pernyataan (maks 3x)
   - **3** → Lihat semua tersangka
   - **4** → Tangkap tersangka — keputusan final!
   - **5** → Keluar
4. Kumpulkan petunjuk, deduksi siapa pelakunya, lalu tangkap!

> **Perhatian**: Saksi tidak selalu berkata jujur. Noise clue bisa menyesatkan!

---

## Sistem Skor / Scoring

| Aksi              | Efek Skor |
|-------------------|-----------|
| Tangkap benar     | Base 1000 |
| Per petunjuk      | -50 poin  |
| Per saksi         | -30 poin  |
| Minimum skor      | 100 poin  |

---

## Menambah Bahasa / Adding a Language

Buat file `data/lang_XX.json` dengan struktur yang sama seperti `lang_id.json`.  
Lalu tambahkan opsi di `game.py → select_language()`.

---

## Menambah Konten / Adding Content

Semua data game ada di `data/lang_id.json` dan `data/lang_en.json`:
- **`names`** → daftar nama tersangka
- **`locations`** → daftar lokasi TKP
- **`weapons`** → daftar senjata
- **`clue_templates.valid`** → petunjuk yang mengarah ke pelaku
- **`clue_templates.noise`** → petunjuk pengalih
- **`witness_templates`** → pernyataan saksi (accurate / misleading / vague)

## Note: Nama, tempat, kejadian, atau semacamnya hanyalah fiktif belaka tanpa maksud tertentu.
