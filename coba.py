
import pygame
import sys

# 1. Inisialisasi Pygame
pygame.init()

# 2. Ukuran layar
WIDTH = 1200
HEIGHT = 760

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Pathfinding Visualizer - BFS, Dijkstra, A*"
)

# 3. Warna
BACKGROUND = (12, 20, 35)
PANEL = (22, 34, 55)
GRID_COLOR = (55, 70, 90)
CELL_COLOR = (17, 27, 42)
WHITE = (255, 255, 255)
GREEN = (0, 210, 100)
RED = (230, 65, 75)
GRAY = (100, 110, 125)

# 4. Font
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 28, bold=True)

# 5. Pengaturan grid
ROWS = 20
COLS = 20
CELL_SIZE = 25

GRID_X = 290
GRID_Y = 120

# 6. Fungsi menampilkan teks
def draw_text(text, x, y, font_size=font, color=WHITE):
    image = font_size.render(text, True, color)
    screen.blit(image, (x, y))


# 7. Fungsi membuat panel
def draw_panel(x, y, width, height):
    pygame.draw.rect(
        screen,
        PANEL,
        (x, y, width, height),
        border_radius=12
    )


# 8. Fungsi menggambar grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):

            x = GRID_X + col * CELL_SIZE
            y = GRID_Y + row * CELL_SIZE

            pygame.draw.rect(
                screen,
                CELL_COLOR,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )


# 9. Tampilan utama
def draw_window():

    screen.fill(BACKGROUND)

    # Judul aplikasi
    draw_text(
        "PATHFINDING VISUALIZER",
        30, 25, title_font, GREEN
    )

    # Panel kiri
    draw_panel(20, 80, 245, 640)

    draw_text("KONTROL GRID", 40, 105)
    draw_text("Ukuran: 20 x 20", 40, 150, small_font)

    draw_text("MODE EDIT", 40, 210)
    draw_text("[1] START", 40, 250)
    draw_text("[2] GOAL", 40, 285)
    draw_text("[3] OBSTACLE", 40, 320)
    draw_text("[4] ERASE", 40, 355)

    draw_text("ALGORITMA", 40, 420)
    draw_text("[5] BFS", 40, 460)
    draw_text("[6] DIJKSTRA", 40, 495)
    draw_text("[7] A*", 40, 530)

    draw_text("SPACE : JALANKAN", 40, 600, small_font)
    draw_text("R : RESET", 40, 635, small_font)

    # Panel tengah
    draw_panel(280, 80, 525, 590)

    draw_text("AREA LABIRIN", 300, 90)
    draw_grid()

    # Panel kanan
    draw_panel(820, 80, 360, 300)

    draw_text("HASIL PENCARIAN", 845, 105)
    draw_text("Algoritma : -", 845, 160, small_font)
    draw_text("Waktu : - ms", 845, 200, small_font)
    draw_text("Node : -", 845, 240, small_font)
    draw_text("Panjang jalur : -", 845, 280, small_font)
    draw_text("Status : Menunggu", 845, 320, small_font)

    # Panel legenda
    draw_panel(820, 395, 360, 275)

    draw_text("LEGENDA WARNA", 845, 420)
    draw_text("Hijau : START", 845, 475, small_font, GREEN)
    draw_text("Merah : GOAL", 845, 515, small_font, RED)
    draw_text("Abu-abu : OBSTACLE", 845, 555, small_font, GRAY)
    draw_text("Biru : NODE DIPERIKSA", 845, 595, small_font)
    draw_text("Kuning : JALUR AKHIR", 845, 635, small_font, (255, 220, 0))

    pygame.display.update()


# 10. Loop utama program
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    draw_window()

pygame.quit()
sys.exit()