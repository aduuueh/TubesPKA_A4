"""
TUGAS BESAR PENGANTAR KECERDASAN ARTIFISIAL (PKA)
Kelompok A4 - Institut Teknologi Kalimantan (2026)
Visualisasi dan Komparasi BFS, Dijkstra, A* Standar, dan A* Tie-Breaking pada Grid Labirin Menggunakan Pygame

Struktur Proyek:
- algorithms.py : Implementasi BFS, Dijkstra, A* Standar, A* Tie-Breaking, dan benchmark 30x.
- scenarios.py  : Generator labirin DFS dan 6 skenario pengujian.
- main.py       : Antarmuka Pygame, tombol interaktif skenario/kontrol, dan loop utama.
"""

import sys
import pygame
from algorithms import (
    run_bfs,
    run_dijkstra,
    run_astar_standard,
    run_astar_tiebreak,
    run_benchmark_30x
)
from scenarios import apply_scenario

# ================= KONFIGURASI TAMPILAN & WARNA =================
GRID_AREA_SIZE = 600
GRID_VIEW_MARGIN = 10
PANEL_X = GRID_AREA_SIZE + GRID_VIEW_MARGIN * 2
PANEL_WIDTH = 430
WINDOW_WIDTH = PANEL_X + PANEL_WIDTH
WINDOW_HEIGHT = 660

# Palet warna sesuai dokumen Proposal Bab 3.1.2
COLOR_ROAD = (24, 64, 36)          # a. Hijau tua: sel jalan
COLOR_WALL = (44, 46, 52)          # b. Abu-abu gelap: obstacle / tembok
COLOR_START = (46, 213, 115)       # c. Hijau terang: posisi START
COLOR_GOAL = (255, 71, 87)         # d. Merah: posisi GOAL
COLOR_FRONTIER = (84, 160, 255)    # e. Biru muda: node frontier
COLOR_EXPANDED = (16, 52, 128)     # f. Biru tua: node diekspansi
COLOR_PATH = (254, 211, 48)        # g. Kuning: jalur terpendek

COLOR_GRID_LINE = (30, 32, 38)
COLOR_PANEL_BG = (18, 20, 24)
COLOR_PANEL_BORDER = (45, 48, 56)
COLOR_TEXT_MAIN = (235, 235, 235)
COLOR_TEXT_MUTED = (155, 160, 170)
COLOR_TEXT_ACCENT = (110, 200, 255)
COLOR_TEXT_WARN = (255, 195, 18)

# Warna tombol UI
COLOR_BTN_BG = (32, 35, 42)
COLOR_BTN_ACTIVE = (24, 80, 135)
COLOR_BTN_BORDER = (60, 65, 78)
COLOR_BTN_BORDER_ACTIVE = (110, 200, 255)


class Spot:
    """Representasi satu sel (node) pada grid - gaya Tech With Tim"""
    def __init__(self, row, col, cell_size, total_rows, offset_x=0, offset_y=0):
        self.row = row
        self.col = col
        self.x = col * cell_size + offset_x
        self.y = row * cell_size + offset_y
        self.color = COLOR_ROAD
        self.neighbors = []
        self.cell_size = cell_size
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLOR_EXPANDED

    def is_open(self):
        return self.color == COLOR_FRONTIER

    def is_barrier(self):
        return self.color == COLOR_WALL

    def is_start(self):
        return self.color == COLOR_START

    def is_goal(self):
        return self.color == COLOR_GOAL

    def reset(self):
        self.color = COLOR_ROAD

    def make_start(self):
        self.color = COLOR_START

    def make_goal(self):
        self.color = COLOR_GOAL

    def make_closed(self):
        self.color = COLOR_EXPANDED

    def make_open(self):
        self.color = COLOR_FRONTIER

    def make_barrier(self):
        self.color = COLOR_WALL

    def make_path(self):
        self.color = COLOR_PATH

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.cell_size, self.cell_size))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Urutan 4 arah konsisten: Atas, Kanan, Bawah, Kiri (tanpa diagonal)
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


# ================= GENERATOR GRID =================
def make_grid(rows, cell_size, offset_x=0, offset_y=0):
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(rows):
            spot = Spot(r, c, cell_size, rows, offset_x, offset_y)
            grid[r].append(spot)
    return grid


def draw_grid(win, rows, cell_size, offset_x=0, offset_y=0):
    width = rows * cell_size
    for r in range(rows + 1):
        pygame.draw.line(win, COLOR_GRID_LINE, (offset_x, offset_y + r * cell_size), (offset_x + width, offset_y + r * cell_size))
    for c in range(rows + 1):
        pygame.draw.line(win, COLOR_GRID_LINE, (offset_x + c * cell_size, offset_y), (offset_x + c * cell_size, offset_y + width))


def get_clicked_pos(pos, rows, cell_size, offset_x=0, offset_y=0):
    x, y = pos
    if not (offset_x <= x < offset_x + rows * cell_size and offset_y <= y < offset_y + rows * cell_size):
        return None
    row = (y - offset_y) // cell_size
    col = (x - offset_x) // cell_size
    if 0 <= row < rows and 0 <= col < rows:
        return row, col
    return None


def clear_search_visuals(grid, start, end):
    for row in grid:
        for spot in row:
            if not spot.is_barrier() and spot != start and spot != end:
                spot.reset()
    if start:
        start.make_start()
    if end:
        end.make_goal()


# ================= KOMPONEN TOMBOL UI =================
def draw_button(win, font, rect, text, active=False, color_override=None, border_color_override=None):
    bg_color = color_override if color_override else (COLOR_BTN_ACTIVE if active else COLOR_BTN_BG)
    border_color = border_color_override if border_color_override else (COLOR_BTN_BORDER_ACTIVE if active else COLOR_BTN_BORDER)
    
    pygame.draw.rect(win, bg_color, rect, border_radius=4)
    pygame.draw.rect(win, border_color, rect, width=1, border_radius=4)
    
    text_color = COLOR_TEXT_ACCENT if active else COLOR_TEXT_MAIN
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    win.blit(text_surf, text_rect)


# ================= PANEL INFORMASI & TAMPILAN =================
def draw_panel(win, font, font_bold, font_small, state, buttons):
    panel_rect = pygame.Rect(PANEL_X, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(win, COLOR_PANEL_BG, panel_rect)
    pygame.draw.line(win, COLOR_PANEL_BORDER, (PANEL_X, 0), (PANEL_X, WINDOW_HEIGHT), 2)

    x = PANEL_X + 16
    y = 10

    # 1. Header
    win.blit(font_bold.render("TUBES PKA - KELOMPOK A4", True, COLOR_TEXT_ACCENT), (x, y))
    y += 16
    win.blit(font_small.render("Komparasi BFS, Dijkstra, A* Std & A* Tie-Break", True, COLOR_TEXT_MUTED), (x, y))
    y += 14
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 5

    # 2. Tombol Pilihan Skenario
    win.blit(font_bold.render("PILIH SKENARIO PENGUJIAN (Klik):", True, COLOR_TEXT_WARN), (x, y))
    y += 18

    sc_labels = {
        1: "S1: Terbuka [F1]",
        2: "S2: 20% Obstacle [F2]",
        3: "S3: Labirin Simpel [F3]",
        4: "S4: Labirin Kompleks [F4]",
        5: f"S5: Ukuran {state['rows']}x{state['rows']} [F5]",
        6: "S6: Goal Terkurung [F6]"
    }
    for sc_id, rect in buttons['scenarios'].items():
        is_active = (state['scenario'] == sc_id)
        draw_button(win, font_small, rect, sc_labels[sc_id], active=is_active)

    y = 117
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 5

    # 3. Pilihan Algoritma
    win.blit(font_bold.render("PILIH ALGORITMA (Klik / Tombol 1-4):", True, COLOR_TEXT_ACCENT), (x, y))
    y += 18

    algo_labels = {
        'BFS': "1. BFS",
        'Dijkstra': "2. Dijkstra",
        'A* Standar': "3. A* Standar",
        'A* Tie-Break': "4. A* Tie-Break"
    }
    for algo_key, rect in buttons['algo'].items():
        draw_button(win, font_small, rect, algo_labels[algo_key], active=(state['algo'] == algo_key))

    y = 189
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 5

    # 4. Mode Edit & Aksi (Tata Letak Rapi Tanpa Teks Terpotong)
    win.blit(font_bold.render("MODE EDIT & AKSI:", True, COLOR_TEXT_ACCENT), (x, y))
    y += 18

    draw_button(win, font_small, buttons['mode']['S'], "[S] Start", active=(state['mode'] == 'S'))
    draw_button(win, font_small, buttons['mode']['G'], "[G] Goal", active=(state['mode'] == 'G'))
    draw_button(win, font_small, buttons['mode']['O'], "[O] Dinding", active=(state['mode'] == 'O'))

    draw_button(win, font_bold, buttons['actions']['visualize'], "▶ Visualisasi Langkah demi Langkah (SPACE)", color_override=(20, 75, 40), border_color_override=(46, 213, 115))
    draw_button(win, font_bold, buttons['actions']['benchmark'], "⚡ Benchmark 30x (B)", color_override=(110, 65, 15), border_color_override=(255, 195, 18))
    draw_button(win, font_bold, buttons['actions']['reset'], "🔄 Reset (C)", color_override=(75, 25, 25), border_color_override=(255, 71, 87))

    y = 296
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 5

    # 5. Riwayat Hasil Visualisasi (History Berdampingan)
    win.blit(font_bold.render("RIWAYAT HASIL VISUALISASI:", True, COLOR_TEXT_ACCENT), (x, y))
    y += 16

    header_hist = f"{'Algoritma':<13} {'Status':<11} {'Waktu':<12} {'Node':<7} {'Jalur':<6}"
    win.blit(font_small.render(header_hist, True, COLOR_TEXT_MUTED), (x, y))
    y += 13
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 4

    algo_order = ['BFS', 'Dijkstra', 'A* Standar', 'A* Tie-Break']
    for algo in algo_order:
        short_name = "A* TB" if algo == 'A* Tie-Break' else ("A* Std" if algo == 'A* Standar' else algo)
        hist = state['visual_history'].get(algo)
        if hist:
            time_str = f"{hist['time_ms']:>7.2f} ms"
            row_line = f"{short_name:<13} {hist['status']:<11} {time_str:<12} {hist['expanded']:<7} {hist['path_len']:<6}"
            row_color = COLOR_TEXT_WARN if algo == state.get('last_algo_run') else COLOR_TEXT_MAIN
        else:
            row_line = f"{short_name:<13} {'-':<11} {'-':<12} {'-':<7} {'-':<6}"
            row_color = COLOR_TEXT_MUTED

        win.blit(font_small.render(row_line, True, row_color), (x, y))
        y += 14

    y += 2
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 5

    # 6. Tabel Benchmark 30x (Headless)
    win.blit(font_bold.render("TABEL BENCHMARK (30x PENGULANGAN):", True, COLOR_TEXT_ACCENT), (x, y))
    y += 16

    header_bm = f"{'Algoritma':<13} {'Status':<11} {'Rata-rata':<12} {'Node':<7} {'Jalur':<6}"
    win.blit(font_small.render(header_bm, True, COLOR_TEXT_MUTED), (x, y))
    y += 13
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 4

    if state['benchmark']:
        for algo in algo_order:
            row_data = state['benchmark'].get(algo)
            if row_data:
                short_name = "A* TB" if algo == 'A* Tie-Break' else ("A* Std" if algo == 'A* Standar' else algo)
                t_str = f"{row_data['avg_ms']:>7.3f} ms"
                line = f"{short_name:<13} {row_data['status']:<11} {t_str:<12} {row_data['expanded']:<7} {row_data['path_len']:<6}"
                row_color = COLOR_TEXT_WARN if algo == 'A* Tie-Break' else COLOR_TEXT_MAIN
                win.blit(font_small.render(line, True, row_color), (x, y))
                y += 14
    else:
        win.blit(font_small.render("Tekan [⚡ Benchmark 30x] untuk membandingkan", True, COLOR_TEXT_MUTED), (x, y))
        y += 14
        win.blit(font_small.render("keempat algoritma secara instan tanpa jeda grafis.", True, COLOR_TEXT_MUTED), (x, y))
        y += 14
        y += 14  # spacer to keep heights consistent
        y += 14

    y += 2
    pygame.draw.line(win, COLOR_PANEL_BORDER, (x, y), (x + PANEL_WIDTH - 32, y), 1)
    y += 5

    # 7. Legenda Warna & Panduan
    win.blit(font_bold.render("LEGENDA WARNA & KONTROL:", True, COLOR_TEXT_ACCENT), (x, y))
    y += 16
    legends = [
        (COLOR_START, "START", COLOR_GOAL, "GOAL"),
        (COLOR_ROAD, "Jalan", COLOR_WALL, "Obstacle"),
        (COLOR_FRONTIER, "Frontier (Antrean)", COLOR_EXPANDED, "Diekspansi"),
        (COLOR_PATH, "Jalur Terpendek", None, None),
    ]
    for c1, l1, c2, l2 in legends:
        pygame.draw.rect(win, c1, (x, y + 2, 10, 10))
        win.blit(font_small.render(l1, True, COLOR_TEXT_MAIN), (x + 16, y))
        if c2:
            pygame.draw.rect(win, c2, (x + 195, y + 2, 10, 10))
            win.blit(font_small.render(l2, True, COLOR_TEXT_MAIN), (x + 211, y))
        y += 13

    y += 3
    win.blit(font_small.render("* Klik/drag kiri: gambar | Klik kanan: hapus", True, COLOR_TEXT_MUTED), (x, y))
    y += 13
    win.blit(font_small.render("* SPACE: Visualisasi | B: Benchmark 30x | C: Reset", True, COLOR_TEXT_MUTED), (x, y))


def render_all(win, grid, rows, cell_size, offset_x, offset_y, font, font_bold, font_small, state, buttons):
    win.fill((12, 13, 16))
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, cell_size, offset_x, offset_y)
    draw_panel(win, font, font_bold, font_small, state, buttons)
    pygame.display.update()


# ================= PROGRAM UTAMA =================
def main():
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tubes PKA A4 - Visualisasi BFS, Dijkstra, A* Std & A* Tie-Break")
    font = pygame.font.SysFont("consolas", 12)
    font_bold = pygame.font.SysFont("consolas", 12, bold=True)
    font_small = pygame.font.SysFont("consolas", 11)
    clock = pygame.time.Clock()

    bx1 = PANEL_X + 16
    bx2 = PANEL_X + 216
    bw = 194
    bh = 20

    buttons = {
        'scenarios': {
            1: pygame.Rect(bx1, 46, bw, bh),
            2: pygame.Rect(bx2, 46, bw, bh),
            3: pygame.Rect(bx1, 69, bw, bh),
            4: pygame.Rect(bx2, 69, bw, bh),
            5: pygame.Rect(bx1, 92, bw, bh),
            6: pygame.Rect(bx2, 92, bw, bh),
        },
        'algo': {
            'BFS': pygame.Rect(bx1, 140, bw, bh),
            'Dijkstra': pygame.Rect(bx2, 140, bw, bh),
            'A* Standar': pygame.Rect(bx1, 163, bw, bh),
            'A* Tie-Break': pygame.Rect(bx2, 163, bw, bh),
        },
        'mode': {
            'S': pygame.Rect(bx1, 212, 126, bh),
            'G': pygame.Rect(bx1 + 133, 212, 126, bh),
            'O': pygame.Rect(bx1 + 266, 212, 128, bh),
        },
        'actions': {
            'visualize': pygame.Rect(bx1, 238, 394, 25),
            'benchmark': pygame.Rect(bx1, 267, 246, 23),
            'reset': pygame.Rect(bx1 + 252, 267, 142, 23),
        }
    }

    rows = 31
    cell_size = 19
    offset_x = GRID_VIEW_MARGIN + (GRID_AREA_SIZE - rows * cell_size) // 2
    offset_y = (WINDOW_HEIGHT - rows * cell_size) // 2

    current_scenario = 1
    state = {
        'algo': 'A* Tie-Break',
        'mode': 'O',
        'status': 'IDLE',
        'rows': rows,
        'scenario': current_scenario,
        'last_algo_run': None,
        'visual_history': {},
        'benchmark': {},
    }

    grid = make_grid(rows, cell_size, offset_x, offset_y)
    start = grid[1][1]
    end = grid[rows - 2][rows - 2]
    start.make_start()
    end.make_goal()

    def load_scenario(sc_num, r_count=None):
        nonlocal rows, cell_size, offset_x, offset_y, grid, start, end, current_scenario
        current_scenario = sc_num
        if r_count:
            rows = r_count
        else:
            if sc_num == 5:
                # Variasi ukuran grid pada skenario 5: toggle 21, 31, 51
                if rows == 31: rows = 21
                elif rows == 21: rows = 51
                else: rows = 31
            else:
                rows = 31

        if rows == 21: cell_size = 28
        elif rows == 31: cell_size = 19
        elif rows == 51: cell_size = 11
        else: cell_size = GRID_AREA_SIZE // rows

        offset_x = GRID_VIEW_MARGIN + (GRID_AREA_SIZE - rows * cell_size) // 2
        offset_y = (WINDOW_HEIGHT - rows * cell_size) // 2

        grid = make_grid(rows, cell_size, offset_x, offset_y)
        walls, s_pos, g_pos = apply_scenario(sc_num, rows)

        for r in range(rows):
            for c in range(rows):
                if (r, c) in walls:
                    grid[r][c].make_barrier()

        start = grid[s_pos[0]][s_pos[1]]
        end = grid[g_pos[0]][g_pos[1]]
        start.make_start()
        end.make_goal()

        state['rows'] = rows
        state['scenario'] = current_scenario
        state['status'] = 'IDLE'
        state['last_algo_run'] = None
        state['visual_history'].clear()
        state['benchmark'].clear()

    def start_visualization():
        if not (start and end):
            return
        clear_search_visuals(grid, start, end)
        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)

        algo_name = state['algo']
        state['status'] = 'MENCARI JALUR...'
        draw_callback = lambda: render_all(win, grid, rows, cell_size, offset_x, offset_y, font, font_bold, font_small, state, buttons)

        speed = 240 if rows >= 51 else 120
        if algo_name == 'BFS':
            found, el_time, exp_cnt, plen = run_bfs(draw_callback, grid, start, end, clock, speed)
        elif algo_name == 'Dijkstra':
            found, el_time, exp_cnt, plen = run_dijkstra(draw_callback, grid, start, end, clock, speed)
        elif algo_name == 'A* Standar':
            found, el_time, exp_cnt, plen = run_astar_standard(draw_callback, grid, start, end, clock, speed)
        elif algo_name == 'A* Tie-Break':
            found, el_time, exp_cnt, plen = run_astar_tiebreak(draw_callback, grid, start, end, clock, speed)

        status_str = "DITEMUKAN" if found else "TIDAK ADA"
        state['last_algo_run'] = algo_name
        state['visual_history'][algo_name] = {
            'status': status_str,
            'time_ms': el_time,
            'expanded': exp_cnt,
            'path_len': plen
        }
        state['status'] = status_str

    def run_benchmark():
        if not (start and end):
            return
        state['status'] = 'BENCHMARKING...'
        render_all(win, grid, rows, cell_size, offset_x, offset_y, font, font_bold, font_small, state, buttons)
        results = run_benchmark_30x(grid, start, end)
        state['benchmark'] = results
        state['status'] = 'BENCHMARK SELESAI'

    load_scenario(1)

    running = True
    while running:
        render_all(win, grid, rows, cell_size, offset_x, offset_y, font, font_bold, font_small, state, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Deteksi Klik Tombol UI Panel Samping
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                # Klik Skenario 1 - 6
                for sc_id, rect in buttons['scenarios'].items():
                    if rect.collidepoint(pos):
                        load_scenario(sc_id)
                        break

                # Klik Pilihan Algoritma
                for algo_name, rect in buttons['algo'].items():
                    if rect.collidepoint(pos):
                        state['algo'] = algo_name
                        break

                # Klik Mode Edit
                for mode_key, rect in buttons['mode'].items():
                    if rect.collidepoint(pos):
                        state['mode'] = mode_key
                        break

                # Klik Tombol Aksi
                if buttons['actions']['visualize'].collidepoint(pos):
                    start_visualization()
                elif buttons['actions']['benchmark'].collidepoint(pos):
                    run_benchmark()
                elif buttons['actions']['reset'].collidepoint(pos):
                    clear_search_visuals(grid, start, end)
                    state['status'] = 'IDLE'
                    state['last_algo_run'] = None
                    state['visual_history'].clear()
                    state['benchmark'].clear()

            # Input Mouse pada Area Grid
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < PANEL_X:
                    clicked = get_clicked_pos(pos, rows, cell_size, offset_x, offset_y)
                    if clicked:
                        r, c = clicked
                        spot = grid[r][c]
                        if state['mode'] == 'S':
                            if not spot.is_barrier() and spot != end:
                                if start:
                                    start.reset()
                                start = spot
                                start.make_start()
                                state['visual_history'].clear()
                                state['benchmark'].clear()
                        elif state['mode'] == 'G':
                            if not spot.is_barrier() and spot != start:
                                if end:
                                    end.reset()
                                end = spot
                                end.make_goal()
                                state['visual_history'].clear()
                                state['benchmark'].clear()
                        elif state['mode'] == 'O':
                            if spot != start and spot != end:
                                spot.make_barrier()
                                state['visual_history'].clear()
                                state['benchmark'].clear()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] < PANEL_X:
                    clicked = get_clicked_pos(pos, rows, cell_size, offset_x, offset_y)
                    if clicked:
                        r, c = clicked
                        spot = grid[r][c]
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None
                        spot.reset()
                        state['visual_history'].clear()
                        state['benchmark'].clear()

            # Dukungan Keyboard Hotkeys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: state['mode'] = 'S'
                elif event.key == pygame.K_g: state['mode'] = 'G'
                elif event.key == pygame.K_o: state['mode'] = 'O'

                elif event.key == pygame.K_1: state['algo'] = 'BFS'
                elif event.key == pygame.K_2: state['algo'] = 'Dijkstra'
                elif event.key == pygame.K_3: state['algo'] = 'A* Standar'
                elif event.key == pygame.K_4: state['algo'] = 'A* Tie-Break'

                elif event.key == pygame.K_c:
                    clear_search_visuals(grid, start, end)
                    state['status'] = 'IDLE'
                    state['last_algo_run'] = None
                    state['visual_history'].clear()
                    state['benchmark'].clear()

                elif event.key == pygame.K_F1: load_scenario(1)
                elif event.key == pygame.K_F2: load_scenario(2)
                elif event.key == pygame.K_F3: load_scenario(3)
                elif event.key == pygame.K_F4: load_scenario(4)
                elif event.key == pygame.K_F5: load_scenario(5)
                elif event.key == pygame.K_F6: load_scenario(6)

                elif event.key == pygame.K_b:
                    run_benchmark()

                elif event.key == pygame.K_SPACE:
                    start_visualization()

    pygame.quit()


if __name__ == "__main__":
    main()
