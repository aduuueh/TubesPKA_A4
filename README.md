# Tubes Pengantar Kecerdasan Artifisial (PKA) - Kelompok A4

Proyek visualisasi dan komparasi algoritma pencarian jalur terpendek (Breadth-First Search, Dijkstra, A* Standar, dan A* Tie-Breaking) pada grid labirin 2D menggunakan Python/Pygame dan Google Colab.

## Anggota Kelompok A4
- Abduh Robbani (11251085)
- Andre Hermawan (11251021)
- Muhammad Khayru Rizki (11251033)
- Fati Wahid (11251079)
- Reynaldo Farisha (11251097)

## Struktur Modul Kode
- `main.py` : Berkas antarmuka grafis Pygame, representasi sel `Spot`, tombol UI interaktif (skenario, 4 algoritma, mode edit, aksi), dan loop utama.
- `algorithms.py` : Implementasi algoritma pencarian (BFS, Dijkstra, A* Standar, A* Tie-Breaking), generator animasi visual, serta pengujian benchmark 30x.
- `scenarios.py` : Pembangkit labirin DFS dengan seed tetap dan konfigurasi Skenario 1 sampai 6 sesuai Bab 3.2 Proposal.
- `Tubes_PKA_A4_GoogleColab.ipynb` : Notebook Jupyter mandiri untuk Google Colab (visualisasi grid matplotlib, tabel pandas, dan ekspor grafik perbandingan).
- `create_colab_notebook.py` : Skrip pembuat berkas notebook `.ipynb`.

## Menjalankan Program Pygame (Lokal)
1. Di VS Code: Buka `main.py` lalu tekan tombol **Run (segitiga hijau)** di pojok kanan atas.
2. Melalui Terminal:
```bash
py main.py
```

## Menjalankan di Google Colab
1. Buka [Google Colab](https://colab.research.google.com).
2. Pilih tab **Upload** -> pilih berkas `Tubes_PKA_A4_GoogleColab.ipynb`.
3. Jalankan menu **Runtime -> Run all** (`Ctrl+F9`). Seluruh visualisasi grid, tabel rekapitulasi, dan grafik performa `.png` akan ter-generate otomatis.

## Kontrol Interaktif Pygame (Mouse & Keyboard)
Program dapat dioperasikan penuh menggunakan **klik mouse pada panel kanan** atau menggunakan **keyboard shortcut**:

- **Pilihan Skenario (Klik Tombol S1–S6 atau F1–F6):**
  - `S1: Terbuka [F1]` : Grid terbuka 31x31 tanpa obstacle.
  - `S2: 20% Obstacle [F2]` : Grid 31x31 dengan 20% obstacle acak (seed 2026, jalur terjamin).
  - `S3: Labirin Simpel [F3]` : Labirin 31x31 denah tetap dengan koridor dan jalur alternatif.
  - `S4: Labirin Kompleks [F4]` : Labirin 31x31 sempit dengan banyak dead-end.
  - `S5: Ukuran [F5]` : Variasi ukuran grid (klik berulang untuk siklus 21x21, 31x31, 51x51).
  - `S6: Goal Terkurung [F6]` : Sel sekitar GOAL ditutup untuk menguji status pencarian tidak ditemukan.

- **Pilihan Algoritma:**
  - Klik tombol `1. BFS`, `2. Dijkstra`, `3. A* Standar`, atau `4. A* Tie-Break (Usulan)` (atau tekan angka `1`, `2`, `3`, `4`).

- **Mode Gambar Grid:**
  - Klik `[S] Start`, `[G] Goal`, atau `[O] Dinding` (atau tekan `S`, `G`, `O`).
  - `Klik Kiri / Drag` : Menempatkan titik atau menggambar dinding.
  - `Klik Kanan` : Menghapus sel kembali menjadi jalan.

- **Tombol Eksekusi:**
  - `▶ Visualisasi (SPACE)` : Memulai pencarian animasi langkah demi langkah.
  - `⚡ Benchmark 30x (B)` : Menjalankan pengujian 30x instan tanpa rendering, hasilnya langsung tersusun di tabel panel.
  - `🔄 Reset (C)` : Membersihkan rute visual / reset pencarian.
