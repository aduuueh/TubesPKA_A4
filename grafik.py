
import csv
import matplotlib.pyplot as plt

# Membaca data dari CSV
data = []

with open("hasil_benchmark.csv", "r", encoding="utf-8-sig") as file:
    pembaca = csv.DictReader(file)

    for baris in pembaca:
        data.append(baris)


# Mengambil nama skenario
skenario = []

for baris in data:
    if baris["skenario"] not in skenario:
        skenario.append(baris["skenario"])


# Nama algoritma
algoritma = ["BFS", "Dijkstra", "A*"]

# Menyiapkan data grafik
waktu = {nama: [] for nama in algoritma}
node = {nama: [] for nama in algoritma}

for nama_skenario in skenario:
    for nama_algoritma in algoritma:

        hasil = next(
            baris for baris in data
            if baris["skenario"] == nama_skenario
            and baris["nama"] == nama_algoritma
        )

        waktu[nama_algoritma].append(
            float(hasil["waktu"])
        )

        node[nama_algoritma].append(
            float(hasil["node"])
        )


# Posisi batang grafik
posisi = list(range(len(skenario)))
lebar = 0.25


# ==================================
# GRAFIK 1: WAKTU EKSEKUSI
# ==================================

plt.figure(figsize=(13, 6))

for i, nama in enumerate(algoritma):
    posisi_batang = [
        p + (i - 1) * lebar for p in posisi
    ]

    plt.bar(
        posisi_batang,
        waktu[nama],
        width=lebar,
        label=nama
    )

plt.title("Perbandingan Waktu Eksekusi Algoritma")
plt.xlabel("Skenario Pengujian")
plt.ylabel("Waktu Median (ms)")

plt.xticks(
    posisi,
    skenario,
    rotation=25,
    ha="right"
)

plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig("grafik_waktu.png", dpi=300)
plt.show()


# ==================================
# GRAFIK 2: JUMLAH NODE DIEKSPANSI
# ==================================

plt.figure(figsize=(13, 6))

for i, nama in enumerate(algoritma):
    posisi_batang = [
        p + (i - 1) * lebar for p in posisi
    ]

    plt.bar(
        posisi_batang,
        node[nama],
        width=lebar,
        label=nama
    )

plt.title("Perbandingan Jumlah Node Diekspansi")
plt.xlabel("Skenario Pengujian")
plt.ylabel("Jumlah Node")

plt.xticks(
    posisi,
    skenario,
    rotation=25,
    ha="right"
)

plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig("grafik_node.png", dpi=300)
plt.show()


print("Kedua grafik berhasil dibuat!")
print("File: grafik_waktu.png")
print("File: grafik_node.png")