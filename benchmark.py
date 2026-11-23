
import random
import time
import heapq
import csv
import statistics
from collections import deque

JUMLAH_UJI = 30

ARAH = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]


def buat_grid(baris, kolom):
    return [[0 for _ in range(kolom)] for _ in range(baris)]


def tetangga(posisi, grid):
    baris, kolom = posisi
    hasil = []

    for dr, dc in ARAH:
        nr = baris + dr
        nc = kolom + dc

        if (0 <= nr < len(grid)
                and 0 <= nc < len(grid[0])
                and grid[nr][nc] == 0):
            hasil.append((nr, nc))

    return hasil


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def rekonstruksi(parent, start, goal):
    if goal not in parent and goal != start:
        return []

    jalur = []
    posisi = goal

    while posisi != start:
        jalur.append(posisi)
        posisi = parent[posisi]

    jalur.append(start)
    jalur.reverse()

    return jalur


# =========================
# ALGORITMA BFS
# =========================

def bfs(grid, start, goal):
    antrean = deque([start])
    ditemukan = {start}
    parent = {}
    dikunjungi = set()

    while antrean:
        posisi = antrean.popleft()

        if posisi in dikunjungi:
            continue

        dikunjungi.add(posisi)

        if posisi == goal:
            break

        for nxt in tetangga(posisi, grid):
            if nxt not in ditemukan:
                ditemukan.add(nxt)
                parent[nxt] = posisi
                antrean.append(nxt)

    return rekonstruksi(parent, start, goal), len(dikunjungi)


# =========================
# ALGORITMA DIJKSTRA
# =========================

def dijkstra(grid, start, goal):
    antrean = [(0, start)]
    jarak = {start: 0}
    parent = {}
    dikunjungi = set()

    while antrean:
        biaya, posisi = heapq.heappop(antrean)

        if posisi in dikunjungi:
            continue

        dikunjungi.add(posisi)

        if posisi == goal:
            break

        for nxt in tetangga(posisi, grid):
            biaya_baru = biaya + 1

            if biaya_baru < jarak.get(nxt, float("inf")):
                jarak[nxt] = biaya_baru
                parent[nxt] = posisi
                heapq.heappush(antrean, (biaya_baru, nxt))

    return rekonstruksi(parent, start, goal), len(dikunjungi)


# =========================
# ALGORITMA A*
# =========================

def astar(grid, start, goal):
    nomor = 0
    antrean = [(manhattan(start, goal), nomor, 0, start)]
    jarak = {start: 0}
    parent = {}
    dikunjungi = set()

    while antrean:
        f, _, biaya, posisi = heapq.heappop(antrean)

        if posisi in dikunjungi:
            continue

        dikunjungi.add(posisi)

        if posisi == goal:
            break

        for nxt in tetangga(posisi, grid):
            biaya_baru = biaya + 1

            if biaya_baru < jarak.get(nxt, float("inf")):
                jarak[nxt] = biaya_baru
                parent[nxt] = posisi
                nomor += 1

                nilai_f = biaya_baru + manhattan(nxt, goal)

                heapq.heappush(
                    antrean,
                    (nilai_f, nomor, biaya_baru, nxt)
                )

    return rekonstruksi(parent, start, goal), len(dikunjungi)


# =========================
# PEMBUATAN SKENARIO
# =========================

def buat_obstacle_acak(ukuran, seed):
    grid = buat_grid(ukuran, ukuran)
    start = (0, 0)
    goal = (ukuran - 1, ukuran - 1)

    rng = random.Random(seed)
    jumlah = int(ukuran * ukuran * 0.20)

    kandidat = [
        (r, c)
        for r in range(ukuran)
        for c in range(ukuran)
        if (r, c) != start and (r, c) != goal
    ]

    rng.shuffle(kandidat)

    for posisi in kandidat[:jumlah]:
        grid[posisi[0]][posisi[1]] = 1

    jalur, _ = bfs(grid, start, goal)

    if not jalur:
        return buat_obstacle_acak(ukuran, seed + 1)

    return grid


def skenario_terbuka():
    return buat_grid(30, 30)


def skenario_obstacle():
    return buat_obstacle_acak(30, 2026)


def skenario_labirin_sederhana():
    grid = buat_grid(30, 30)

    for c in range(1, 25):
        if c != 5:
            grid[6][c] = 1

    for c in range(5, 29):
        if c != 23:
            grid[13][c] = 1

    for c in range(1, 25):
        if c != 7:
            grid[20][c] = 1

    return grid


def skenario_labirin_kompleks():
    grid = buat_grid(30, 30)

    for c in range(4, 28, 4):
        celah = 28 if (c // 4) % 2 == 0 else 1

        for r in range(30):
            if r != celah:
                grid[r][c] = 1

    return grid


def skenario_variasi_ukuran(ukuran):
    return buat_obstacle_acak(ukuran, 2026)


# =========================
# PROSES BENCHMARK
# =========================

def uji_algoritma(nama, fungsi, grid, start, goal):
    daftar_waktu = []
    jumlah_node = []
    panjang_jalur = []
    status = "Tidak ditemukan"

    for _ in range(JUMLAH_UJI):
        awal = time.perf_counter()

        jalur, node = fungsi(grid, start, goal)

        akhir = time.perf_counter()

        waktu_ms = (akhir - awal) * 1000

        daftar_waktu.append(waktu_ms)
        jumlah_node.append(node)

        if jalur:
            panjang_jalur.append(len(jalur) - 1)
            status = "Ditemukan"
        else:
            panjang_jalur.append(0)

    return {
        "nama": nama,
        "waktu": statistics.median(daftar_waktu),
        "node": statistics.median(jumlah_node),
        "jalur": statistics.median(panjang_jalur),
        "status": status
    }


def jalankan_benchmark(nama_skenario, grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    algoritma = [
        ("BFS", bfs),
        ("Dijkstra", dijkstra),
        ("A*", astar)
    ]

    print("\n" + "=" * 75)
    print("SKENARIO:", nama_skenario)
    print("Ukuran Grid:", len(grid), "x", len(grid[0]))
    print("Pengujian:", JUMLAH_UJI, "kali")
    print("=" * 75)

    print(
        f"{'Algoritma':<12}"
        f"{'Waktu (ms)':<16}"
        f"{'Node':<12}"
        f"{'Panjang':<12}"
        f"{'Status'}"
    )

    hasil = []

    for nama, fungsi in algoritma:
        data = uji_algoritma(
            nama, fungsi, grid, start, goal
        )

        data["skenario"] = nama_skenario
        data["ukuran_grid"] = f"{len(grid)}x{len(grid[0])}"

        hasil.append(data)

        print(
            f"{data['nama']:<12}"
            f"{data['waktu']:<16.6f}"
            f"{data['node']:<12}"
            f"{data['jalur']:<12}"
            f"{data['status']}"
        )

    return hasil


# =========================
# SIMPAN HASIL KE CSV
# =========================

def simpan_csv(semua_hasil):
    nama_file = "hasil_benchmark.csv"

    kolom = [
        "skenario",
        "ukuran_grid",
        "nama",
        "waktu",
        "node",
        "jalur",
        "status"
    ]

    with open(
        nama_file,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=kolom
        )

        writer.writeheader()
        writer.writerows(semua_hasil)

    print("\nHasil berhasil disimpan ke:", nama_file)


# =========================
# PROGRAM UTAMA
# =========================

def main():
    print("BENCHMARK BFS, DIJKSTRA, DAN A*")
    print("Pengujian tanpa animasi Pygame.")

    skenario = [
        ("1 - Grid Terbuka", skenario_terbuka()),
        ("2 - Obstacle 20% Seed 2026", skenario_obstacle()),
        ("3 - Labirin Sederhana", skenario_labirin_sederhana()),
        ("4 - Labirin Kompleks", skenario_labirin_kompleks()),
        ("5 - Grid 20x20", skenario_variasi_ukuran(20)),
        ("5 - Grid 30x30", skenario_variasi_ukuran(30)),
        ("5 - Grid 50x50", skenario_variasi_ukuran(50))
    ]

    semua_hasil = []

    for nama, grid in skenario:
        hasil = jalankan_benchmark(nama, grid)
        semua_hasil.extend(hasil)

    simpan_csv(semua_hasil)

    print("\nSEMUA PENGUJIAN SELESAI.")


if __name__ == "__main__":
    main()
