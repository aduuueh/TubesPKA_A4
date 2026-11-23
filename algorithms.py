"""
algorithms.py
Modul implementasi algoritma pencarian jalur:
- Breadth-First Search (BFS)
- Dijkstra Algorithm (Uniform Cost Search)
- A* Search Standar (Tanpa Tie-Breaking)
- A* Search dengan Tie-Breaking (Metode Usulan Optimasi)
- Benchmark Headless (30x pengulangan tanpa rendering)
"""

import sys
import time
from collections import deque
import heapq
import pygame


def manhattan(p1, p2):
    """Fungsi heuristik Manhattan: |x1 - x2| + |y1 - y2|"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def reconstruct_path(came_from, current, draw_fn, start, end):
    """Menelusuri balik jalur terpendek dari GOAL ke START"""
    path_len = 0
    curr = current
    while curr in came_from:
        path_len += 1
        curr = came_from[curr]
        if curr != start and curr != end:
            curr.make_path()
        if draw_fn:
            draw_fn()
    if start:
        start.make_start()
    if end:
        end.make_goal()
    return path_len


def run_bfs(draw_fn, grid, start, end, clock, speed=120):
    """Visualisasi BFS menggunakan antrean FIFO (collections.deque)"""
    t0 = time.perf_counter()
    q = deque([start])
    frontier_set = {start}
    visited = set()
    came_from = {}
    expanded_cnt = 0
    found = False

    start.make_open()

    while q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = q.popleft()
        frontier_set.discard(current)

        if current in visited:
            continue
        visited.add(current)
        expanded_cnt += 1

        # Pengujian GOAL saat node dikeluarkan dari frontier
        if current == end:
            found = True
            break

        for neighbor in current.neighbors:
            if neighbor not in visited and neighbor not in frontier_set:
                came_from[neighbor] = current
                frontier_set.add(neighbor)
                q.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()

        if draw_fn:
            draw_fn()
            clock.tick(speed)

        if current != start and current != end:
            current.make_closed()

    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0

    path_len = 0
    if found:
        path_len = reconstruct_path(came_from, end, draw_fn, start, end)

    return found, elapsed_ms, expanded_cnt, path_len


def run_dijkstra(draw_fn, grid, start, end, clock, speed=120):
    """Visualisasi Dijkstra menggunakan Priority Queue (heapq)"""
    t0 = time.perf_counter()
    pq = []
    counter = 0
    heapq.heappush(pq, (0, counter, start))
    cost_so_far = {start: 0}
    visited = set()
    came_from = {}
    expanded_cnt = 0
    found = False

    start.make_open()

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        cost, _, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        expanded_cnt += 1

        if current == end:
            found = True
            break

        for neighbor in current.neighbors:
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                counter += 1
                heapq.heappush(pq, (new_cost, counter, neighbor))
                if neighbor != end and neighbor not in visited:
                    neighbor.make_open()

        if draw_fn:
            draw_fn()
            clock.tick(speed)

        if current != start and current != end:
            current.make_closed()

    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0

    path_len = 0
    if found:
        path_len = reconstruct_path(came_from, end, draw_fn, start, end)

    return found, elapsed_ms, expanded_cnt, path_len


def run_astar_standard(draw_fn, grid, start, end, clock, speed=120):
    """Visualisasi A* Standar: Tanpa tie-breaking, pemecah kesamaan f bersifat FIFO"""
    t0 = time.perf_counter()
    pq = []
    counter = 0
    f_start = manhattan(start.get_pos(), end.get_pos())
    heapq.heappush(pq, (f_start, counter, start))
    g_score = {start: 0}
    visited = set()
    came_from = {}
    expanded_cnt = 0
    found = False

    start.make_open()

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        _, _, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        expanded_cnt += 1

        if current == end:
            found = True
            break

        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + manhattan(neighbor.get_pos(), end.get_pos())
                counter += 1
                heapq.heappush(pq, (f_score, counter, neighbor))
                if neighbor != end and neighbor not in visited:
                    neighbor.make_open()

        if draw_fn:
            draw_fn()
            clock.tick(speed)

        if current != start and current != end:
            current.make_closed()

    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0

    path_len = 0
    if found:
        path_len = reconstruct_path(came_from, end, draw_fn, start, end)

    return found, elapsed_ms, expanded_cnt, path_len


def run_astar_tiebreak(draw_fn, grid, start, end, clock, speed=120):
    """Visualisasi A* Tie-Breaking (Metode Usulan): Memilih node dengan h terkecil (g terbesar) jika f sama"""
    t0 = time.perf_counter()
    pq = []
    counter = 0
    f_start = manhattan(start.get_pos(), end.get_pos())
    heapq.heappush(pq, (f_start, 0, counter, start))
    g_score = {start: 0}
    visited = set()
    came_from = {}
    expanded_cnt = 0
    found = False

    start.make_open()

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        _, _, _, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        expanded_cnt += 1

        if current == end:
            found = True
            break

        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + manhattan(neighbor.get_pos(), end.get_pos())
                counter += 1
                # Kunci Tie-Breaking: jika f sama, utamakan yang nilai g lebih besar (-tentative_g lebih kecil)
                heapq.heappush(pq, (f_score, -tentative_g, counter, neighbor))
                if neighbor != end and neighbor not in visited:
                    neighbor.make_open()

        if draw_fn:
            draw_fn()
            clock.tick(speed)

        if current != start and current != end:
            current.make_closed()

    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0

    path_len = 0
    if found:
        path_len = reconstruct_path(came_from, end, draw_fn, start, end)

    return found, elapsed_ms, expanded_cnt, path_len


# ================= BENCHMARK HEADLESS (30x TANPA RENDER) =================
def solve_headless(algo_name, start, end):
    """Eksekusi satu kali tanpa rendering atau jeda frame"""
    found = False
    expanded = 0
    came_from = {}

    if algo_name == 'BFS':
        q = deque([start])
        frontier_set = {start}
        visited = set()
        while q:
            cur = q.popleft()
            frontier_set.discard(cur)
            if cur in visited:
                continue
            visited.add(cur)
            expanded += 1
            if cur == end:
                found = True
                break
            for nxt in cur.neighbors:
                if nxt not in visited and nxt not in frontier_set:
                    came_from[nxt] = cur
                    frontier_set.add(nxt)
                    q.append(nxt)

    elif algo_name == 'Dijkstra':
        pq = []
        cnt = 0
        heapq.heappush(pq, (0, cnt, start))
        cost_so_far = {start: 0}
        visited = set()
        while pq:
            cost, _, cur = heapq.heappop(pq)
            if cur in visited:
                continue
            visited.add(cur)
            expanded += 1
            if cur == end:
                found = True
                break
            for nxt in cur.neighbors:
                nc = cost + 1
                if nxt not in cost_so_far or nc < cost_so_far[nxt]:
                    cost_so_far[nxt] = nc
                    came_from[nxt] = cur
                    cnt += 1
                    heapq.heappush(pq, (nc, cnt, nxt))

    elif algo_name == 'A* Standar':
        pq = []
        cnt = 0
        f_start = manhattan(start.get_pos(), end.get_pos())
        heapq.heappush(pq, (f_start, cnt, start))
        g_score = {start: 0}
        visited = set()
        while pq:
            _, _, cur = heapq.heappop(pq)
            if cur in visited:
                continue
            visited.add(cur)
            expanded += 1
            if cur == end:
                found = True
                break
            for nxt in cur.neighbors:
                tg = g_score[cur] + 1
                if nxt not in g_score or tg < g_score[nxt]:
                    g_score[nxt] = tg
                    came_from[nxt] = cur
                    cnt += 1
                    f = tg + manhattan(nxt.get_pos(), end.get_pos())
                    heapq.heappush(pq, (f, cnt, nxt))

    elif algo_name == 'A* Tie-Break':
        pq = []
        cnt = 0
        f_start = manhattan(start.get_pos(), end.get_pos())
        heapq.heappush(pq, (f_start, 0, cnt, start))
        g_score = {start: 0}
        visited = set()
        while pq:
            _, _, _, cur = heapq.heappop(pq)
            if cur in visited:
                continue
            visited.add(cur)
            expanded += 1
            if cur == end:
                found = True
                break
            for nxt in cur.neighbors:
                tg = g_score[cur] + 1
                if nxt not in g_score or tg < g_score[nxt]:
                    g_score[nxt] = tg
                    came_from[nxt] = cur
                    cnt += 1
                    f = tg + manhattan(nxt.get_pos(), end.get_pos())
                    heapq.heappush(pq, (f, -tg, cnt, nxt))

    path_len = 0
    if found:
        curr = end
        while curr in came_from:
            path_len += 1
            curr = came_from[curr]

    return found, expanded, path_len


def run_benchmark_30x(grid, start, end):
    """Menjalankan 4 algoritma masing-masing 30x dan mencatat rata-rata"""
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    results = {}
    for algo in ['BFS', 'Dijkstra', 'A* Standar', 'A* Tie-Break']:
        times = []
        found, exp_cnt, plen = False, 0, 0
        for _ in range(30):
            t0 = time.perf_counter()
            found, exp_cnt, plen = solve_headless(algo, start, end)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000.0)

        avg_time = sum(times) / len(times)
        results[algo] = {
            'avg_ms': avg_time,
            'expanded': exp_cnt,
            'path_len': plen,
            'status': "Ditemukan" if found else "Tidak Ada"
        }
    return results
