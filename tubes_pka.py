
import pygame
import sys
import time
import heapq
from collections import deque

# ==========================================
# 1. INISIALISASI
# ==========================================

pygame.init()

WIDTH = 1200
HEIGHT = 760

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer - BFS, Dijkstra, A*")

clock = pygame.time.Clock()

# ==========================================
# 2. WARNA
# ==========================================

BACKGROUND = (12, 20, 35)
PANEL = (22, 34, 55)
CELL_COLOR = (17, 27, 42)
GRID_COLOR = (55, 70, 90)

WHITE = (240, 245, 255)
GREEN = (0, 210, 100)
RED = (230, 65, 75)
GRAY = (100, 110, 125)
BLUE = (20, 75, 170)
CYAN = (35, 155, 235)
YELLOW = (255, 220, 0)

# ==========================================
# 3. FONT
# ==========================================

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 28, bold=True)

# ==========================================
# 4. PENGATURAN GRID
# ==========================================

ROWS = 20
COLS = 20
CELL_SIZE = 25

GRID_X = 290
GRID_Y = 120

grid = [
    [0 for _ in range(COLS)]
    for _ in range(ROWS)
]

start = None
goal = None

mode = "START"
algorithm = "BFS"
status = "Menunggu"

# ==========================================
# 5. DATA PENCARIAN
# ==========================================

bfs_queue = deque()
bfs_visited = set()
bfs_parent = {}

dijkstra_queue = []
dijkstra_distance = {}
dijkstra_parent = {}
dijkstra_visited = set()

astar_queue = []
astar_g_score = {}
astar_parent = {}
astar_visited = set()

priority_counter = 0

final_path = []
frontier_nodes = set()
expanded_nodes = set()

search_running = False
search_finished = False

expanded_count = 0
path_length = 0
search_time = 0

search_start_time = 0
last_step_time = 0

STEP_DELAY = 35

# ==========================================
# 6. FUNGSI TEKS
# ==========================================

def draw_text(text, x, y, selected_font=font, color=WHITE):

    image = selected_font.render(text, True, color)
    screen.blit(image, (x, y))


# ==========================================
# 7. FUNGSI PANEL
# ==========================================

def draw_panel(x, y, width, height):

    pygame.draw.rect(
        screen,
        PANEL,
        (x, y, width, height),
        border_radius=12
    )


# ==========================================
# 8. POSISI MOUSE
# ==========================================

def get_cell_position(mouse_x, mouse_y):

    col = (mouse_x - GRID_X) // CELL_SIZE
    row = (mouse_y - GRID_Y) // CELL_SIZE

    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col

    return None


# ==========================================
# 9. RESET HASIL PENCARIAN
# ==========================================

def clear_search():

    global bfs_queue, bfs_visited, bfs_parent

    global dijkstra_queue, dijkstra_distance
    global dijkstra_parent, dijkstra_visited

    global astar_queue, astar_g_score
    global astar_parent, astar_visited

    global priority_counter

    global final_path, frontier_nodes, expanded_nodes
    global search_running, search_finished
    global expanded_count, path_length, search_time

    bfs_queue = deque()
    bfs_visited = set()
    bfs_parent = {}

    dijkstra_queue = []
    dijkstra_distance = {}
    dijkstra_parent = {}
    dijkstra_visited = set()

    astar_queue = []
    astar_g_score = {}
    astar_parent = {}
    astar_visited = set()

    priority_counter = 0

    final_path = []
    frontier_nodes = set()
    expanded_nodes = set()

    search_running = False
    search_finished = False

    expanded_count = 0
    path_length = 0
    search_time = 0


# ==========================================
# 10. RESET GRID
# ==========================================

def reset_grid():

    global grid, start, goal, status

    grid = [
        [0 for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    start = None
    goal = None

    clear_search()

    status = "Grid berhasil direset"


# ==========================================
# 11. EDIT GRID
# ==========================================

def edit_cell(row, col, edit_mode):

    global start, goal, status

    position = (row, col)

    if edit_mode == "START":

        if grid[row][col] == 0 and position != goal:
            start = position
            status = "START berhasil dipasang"

    elif edit_mode == "GOAL":

        if grid[row][col] == 0 and position != start:
            goal = position
            status = "GOAL berhasil dipasang"

    elif edit_mode == "OBSTACLE":

        if position != start and position != goal:
            grid[row][col] = 1
            status = "Obstacle ditambahkan"

    elif edit_mode == "ERASE":

        grid[row][col] = 0

        if position == start:
            start = None

        if position == goal:
            goal = None

        status = "Sel berhasil dihapus"

    clear_search()


# ==========================================
# 12. HEURISTIK MANHATTAN
# ==========================================

def manhattan(position, target):

    return (
        abs(position[0] - target[0])
        + abs(position[1] - target[1])
    )


# ==========================================
# 13. MENYELESAIKAN PENCARIAN
# ==========================================

def finish_search(found, parent_map):

    global search_running, search_finished
    global final_path, path_length
    global status, search_time

    search_running = False
    search_finished = True

    if found:

        current = goal
        final_path = []

        while current is not None:
            final_path.append(current)
            current = parent_map[current]

        final_path.reverse()

        path_length = len(final_path) - 1

        status = "Jalur ditemukan!"

    else:

        final_path = []
        path_length = 0

        status = "Jalur tidak ditemukan"

    # Waktu termasuk animasi
    search_time = (
        time.perf_counter() - search_start_time
    ) * 1000


# ==========================================
# 14. MEMULAI BFS
# ==========================================

def start_bfs():

    global search_running, search_finished
    global status, last_step_time

    clear_search()

    if start is None or goal is None:
        status = "Pasang START dan GOAL dahulu"
        return

    bfs_queue.append(start)
    bfs_visited.add(start)
    bfs_parent[start] = None

    search_running = True
    search_finished = False

    last_step_time = pygame.time.get_ticks()

    status = "BFS sedang mencari..."


# ==========================================
# 15. PROSES BFS
# ==========================================

def bfs_step():

    global expanded_count, frontier_nodes

    if not bfs_queue:
        finish_search(False, bfs_parent)
        return

    current = bfs_queue.popleft()

    expanded_nodes.add(current)
    expanded_count += 1

    if current == goal:
        finish_search(True, bfs_parent)
        return

    row, col = current

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if not (0 <= new_row < ROWS):
            continue

        if not (0 <= new_col < COLS):
            continue

        neighbor = (new_row, new_col)

        if grid[new_row][new_col] == 1:
            continue

        if neighbor in bfs_visited:
            continue

        bfs_visited.add(neighbor)
        bfs_parent[neighbor] = current
        bfs_queue.append(neighbor)

    frontier_nodes = set(bfs_queue)


# ==========================================
# 16. MEMULAI DIJKSTRA
# ==========================================

def start_dijkstra():

    global search_running, search_finished
    global status, last_step_time
    global priority_counter

    clear_search()

    if start is None or goal is None:
        status = "Pasang START dan GOAL dahulu"
        return

    dijkstra_distance[start] = 0
    dijkstra_parent[start] = None

    priority_counter = 0

    heapq.heappush(
        dijkstra_queue,
        (0, priority_counter, start)
    )

    search_running = True
    search_finished = False

    last_step_time = pygame.time.get_ticks()

    status = "Dijkstra sedang mencari..."


# ==========================================
# 17. PROSES DIJKSTRA
# ==========================================

def dijkstra_step():

    global expanded_count
    global priority_counter
    global frontier_nodes

    if not dijkstra_queue:
        finish_search(False, dijkstra_parent)
        return

    distance, counter, current = heapq.heappop(
        dijkstra_queue
    )

    if distance != dijkstra_distance.get(current):
        return

    if current in dijkstra_visited:
        return

    dijkstra_visited.add(current)
    expanded_nodes.add(current)

    expanded_count += 1

    if current == goal:
        finish_search(True, dijkstra_parent)
        return

    row, col = current

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if not (0 <= new_row < ROWS):
            continue

        if not (0 <= new_col < COLS):
            continue

        neighbor = (new_row, new_col)

        if grid[new_row][new_col] == 1:
            continue

        if neighbor in dijkstra_visited:
            continue

        new_distance = distance + 1

        if new_distance < dijkstra_distance.get(
            neighbor, float("inf")
        ):

            dijkstra_distance[neighbor] = new_distance
            dijkstra_parent[neighbor] = current

            priority_counter += 1

            heapq.heappush(
                dijkstra_queue,
                (
                    new_distance,
                    priority_counter,
                    neighbor
                )
            )

    frontier_nodes = {
        item[2] for item in dijkstra_queue
        if item[2] not in dijkstra_visited
    }


# ==========================================
# 18. MEMULAI A*
# ==========================================

def start_astar():

    global search_running, search_finished
    global status, last_step_time
    global priority_counter

    clear_search()

    if start is None or goal is None:
        status = "Pasang START dan GOAL dahulu"
        return

    astar_g_score[start] = 0
    astar_parent[start] = None

    priority_counter = 0

    # f(n) = g(n) + h(n)
    start_f = manhattan(start, goal)

    heapq.heappush(
        astar_queue,
        (start_f, priority_counter, start)
    )

    search_running = True
    search_finished = False

    last_step_time = pygame.time.get_ticks()

    status = "A* sedang mencari..."


# ==========================================
# 19. PROSES A*
# ==========================================

def astar_step():

    global expanded_count
    global priority_counter
    global frontier_nodes

    if not astar_queue:
        finish_search(False, astar_parent)
        return

    # Mengambil node dengan nilai f terkecil
    f_score, counter, current = heapq.heappop(
        astar_queue
    )

    if current in astar_visited:
        return

    astar_visited.add(current)
    expanded_nodes.add(current)

    expanded_count += 1

    # Jika tujuan ditemukan
    if current == goal:
        finish_search(True, astar_parent)
        return

    row, col = current

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if not (0 <= new_row < ROWS):
            continue

        if not (0 <= new_col < COLS):
            continue

        neighbor = (new_row, new_col)

        # Menghindari obstacle
        if grid[new_row][new_col] == 1:
            continue

        if neighbor in astar_visited:
            continue

        # Jarak aktual dari START
        tentative_g = astar_g_score[current] + 1

        if tentative_g < astar_g_score.get(
            neighbor, float("inf")
        ):

            astar_g_score[neighbor] = tentative_g

            astar_parent[neighbor] = current

            # Perkiraan jarak ke GOAL
            h_score = manhattan(neighbor, goal)

            # Total nilai prioritas
            f_score = tentative_g + h_score

            priority_counter += 1

            heapq.heappush(
                astar_queue,
                (
                    f_score,
                    priority_counter,
                    neighbor
                )
            )

    frontier_nodes = {
        item[2] for item in astar_queue
        if item[2] not in astar_visited
    }


# ==========================================
# 20. UPDATE ANIMASI
# ==========================================

def update_search():

    global last_step_time

    if not search_running:
        return

    current_time = pygame.time.get_ticks()

    if current_time - last_step_time < STEP_DELAY:
        return

    if algorithm == "BFS":
        bfs_step()

    elif algorithm == "Dijkstra":
        dijkstra_step()

    elif algorithm == "A*":
        astar_step()

    last_step_time = current_time


# ==========================================
# 21. MENGGAMBAR GRID
# ==========================================

def draw_grid():

    for row in range(ROWS):

        for col in range(COLS):

            x = GRID_X + col * CELL_SIZE
            y = GRID_Y + row * CELL_SIZE

            position = (row, col)

            color = CELL_COLOR

            if grid[row][col] == 1:
                color = GRAY

            if position in frontier_nodes:
                color = CYAN

            if position in expanded_nodes:
                color = BLUE

            if position in final_path:
                color = YELLOW

            if position == start:
                color = GREEN

            if position == goal:
                color = RED

            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

            if position == start:
                draw_text(
                    "S", x + 7, y + 2,
                    small_font, WHITE
                )

            if position == goal:
                draw_text(
                    "G", x + 7, y + 2,
                    small_font, WHITE
                )


# ==========================================
# 22. TAMPILAN UTAMA
# ==========================================

def draw_window():

    screen.fill(BACKGROUND)

    draw_text(
        "PATHFINDING VISUALIZER",
        30, 25, title_font, GREEN
    )

    # Panel kiri
    draw_panel(20, 80, 245, 640)

    draw_text("KONTROL GRID", 40, 105)
    draw_text("Ukuran: 20 x 20", 40, 150, small_font)

    draw_text("MODE EDIT", 40, 210)

    draw_text(
        "[1] START", 40, 250, small_font,
        GREEN if mode == "START" else WHITE
    )

    draw_text(
        "[2] GOAL", 40, 285, small_font,
        RED if mode == "GOAL" else WHITE
    )

    draw_text(
        "[3] OBSTACLE", 40, 320, small_font,
        GRAY if mode == "OBSTACLE" else WHITE
    )

    draw_text(
        "[4] ERASE", 40, 355, small_font,
        YELLOW if mode == "ERASE" else WHITE
    )

    draw_text("ALGORITMA", 40, 420)

    draw_text(
        "[5] BFS", 40, 460, small_font,
        GREEN if algorithm == "BFS" else WHITE
    )

    draw_text(
        "[6] DIJKSTRA", 40, 495, small_font,
        GREEN if algorithm == "Dijkstra" else WHITE
    )

    draw_text(
        "[7] A*", 40, 530, small_font,
        GREEN if algorithm == "A*" else WHITE
    )

    draw_text("SPACE : JALANKAN", 40, 600, small_font)
    draw_text("R : RESET", 40, 635, small_font)

    # Panel tengah
    draw_panel(280, 80, 525, 590)

    draw_text("AREA LABIRIN", 300, 90)

    draw_grid()

    # Panel hasil
    draw_panel(820, 80, 360, 300)

    draw_text("HASIL PENCARIAN", 845, 105)

    draw_text(
        "Algoritma: " + algorithm,
        845, 155, small_font
    )

    draw_text(
        "Status: " + status,
        845, 195, small_font
    )

    draw_text(
        "Node diperiksa: " + str(expanded_count),
        845, 235, small_font
    )

    draw_text(
        "Panjang jalur: " + str(path_length),
        845, 275, small_font
    )

    draw_text(
        f"Waktu: {search_time:.2f} ms",
        845, 315, small_font
    )

    # Panel legenda
    draw_panel(820, 395, 360, 275)

    draw_text("LEGENDA WARNA", 845, 420)

    draw_text("Hijau : START", 845, 475, small_font, GREEN)
    draw_text("Merah : GOAL", 845, 515, small_font, RED)
    draw_text("Abu-abu : OBSTACLE", 845, 555, small_font, GRAY)
    draw_text("Biru tua : DIPERIKSA", 845, 595, small_font, BLUE)
    draw_text("Biru muda : FRONTIER", 845, 625, small_font, CYAN)
    draw_text("Kuning : JALUR AKHIR", 845, 650, small_font, YELLOW)

    pygame.display.update()


# ==========================================
# 23. LOOP UTAMA
# ==========================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1 and not search_running:
                mode = "START"

            elif event.key == pygame.K_2 and not search_running:
                mode = "GOAL"

            elif event.key == pygame.K_3 and not search_running:
                mode = "OBSTACLE"

            elif event.key == pygame.K_4 and not search_running:
                mode = "ERASE"

            elif event.key == pygame.K_5 and not search_running:
                algorithm = "BFS"
                clear_search()
                status = "BFS dipilih"

            elif event.key == pygame.K_6 and not search_running:
                algorithm = "Dijkstra"
                clear_search()
                status = "Dijkstra dipilih"

            elif event.key == pygame.K_7 and not search_running:
                algorithm = "A*"
                clear_search()
                status = "A* dipilih"

            elif event.key == pygame.K_SPACE and not search_running:

                if start is None or goal is None:
                    status = "Pasang START dan GOAL dahulu"

                else:

                    search_start_time = time.perf_counter()

                    if algorithm == "BFS":
                        start_bfs()

                    elif algorithm == "Dijkstra":
                        start_dijkstra()

                    elif algorithm == "A*":
                        start_astar()

            elif event.key == pygame.K_r and not search_running:
                reset_grid()

        # Klik mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            if not search_running:

                position = get_cell_position(*event.pos)

                if position is not None:

                    row, col = position

                    if event.button == 1:
                        edit_cell(row, col, mode)

                    elif event.button == 3:
                        edit_cell(row, col, "ERASE")

        # Drag obstacle
        if event.type == pygame.MOUSEMOTION:

            if not search_running:

                if pygame.mouse.get_pressed()[0] and mode == "OBSTACLE":

                    position = get_cell_position(*event.pos)

                    if position is not None:

                        row, col = position

                        edit_cell(row, col, "OBSTACLE")

    update_search()

    draw_window()

    clock.tick(60)


# ==========================================
# 24. KELUAR
# ==========================================

pygame.quit()
sys.exit()