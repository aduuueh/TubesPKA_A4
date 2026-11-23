"""
Algoritma pencarian jalur - Tubes PKA A4.
Semua run_* dipanggil main.py dengan bentuk:
    found, waktu_ms, expanded, plen = run_xxx(draw, grid, start, end, clock, speed)
Node dihitung diekspansi saat keluar dari antrean (termasuk GOAL).
Waktu hanya menghitung komputasi, tanpa draw() dan clock.tick().
"""
import sys
import time
import heapq
from collections import deque

import pygame


def buat_jalur(came_from, start, end):
    jalur = []
    cur = end
    while cur is not None:
        jalur.append(cur)
        cur = came_from[cur]
    jalur.reverse()
    return jalur


#BFS
def bfs_headless(start, end):
    queue = deque([start])
    came_from = {start: None}
    expanded = 0

    while queue:
        cur = queue.popleft()
        expanded += 1
        if cur == end:
            return True, expanded, len(buat_jalur(came_from, start, end)) - 1
        for nb in cur.neighbors:
            if nb not in came_from:
                came_from[nb] = cur
                queue.append(nb)

    return False, expanded, 0


def run_bfs(draw, grid, start, end, clock, speed):
    queue = deque([start])
    came_from = {start: None}
    expanded = 0
    total = 0.0
    t = time.perf_counter()

    while queue:
        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()

        cur = queue.popleft()
        expanded += 1

        if cur == end:
            total += time.perf_counter() - t
            jalur = buat_jalur(came_from, start, end)
            for spot in jalur:
                if spot != start and spot != end:
                    spot.make_path()
            draw()
            return True, total * 1000, expanded, len(jalur) - 1

        for nb in cur.neighbors:
            if nb not in came_from:
                came_from[nb] = cur
                queue.append(nb)
                if nb != end:
                    nb.make_open()

        if cur != start:
            cur.make_closed()

        total += time.perf_counter() - t
        draw()
        clock.tick(speed)
        t = time.perf_counter()

    draw()
    return False, total * 1000, expanded, 0


#Dijkstra
def run_dijkstra(draw_callback, grid, start, end, clock=None, speed=120):
    count = 0
    pq = [(0, count, start)]
    distances = {start: 0}
    came_from = {}
    visited = set()

    expanded_count = 0
    found = False
    compute_time = 0.0

    while pq:
        t0 = time.perf_counter()
        current_dist, _, current = heapq.heappop(pq)

        if current in visited:
            compute_time += time.perf_counter() - t0
            continue

        visited.add(current)
        expanded_count += 1

        if current == end:
            found = True
            compute_time += time.perf_counter() - t0
            break

        for neighbor in current.neighbors:
            if neighbor in visited:
                continue

            new_dist = current_dist + 1
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                came_from[neighbor] = current
                count += 1
                heapq.heappush(pq, (new_dist, count, neighbor))

                if draw_callback and neighbor != end:
                    neighbor.make_open()

        if draw_callback and current != start:
            current.make_closed()

        compute_time += time.perf_counter() - t0

        if draw_callback:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            draw_callback()
            if clock:
                clock.tick(speed)

    path_len = 0
    if found:
        curr = end
        while curr in came_from:
            curr = came_from[curr]
            path_len += 1
            if draw_callback and curr != start:
                curr.make_path()
                draw_callback()
                if clock:
                    clock.tick(speed)

    elapsed_ms = compute_time * 1000
    return found, elapsed_ms, expanded_count, path_len


#A* Standar
def run_astar_standard(draw, grid, start, end, clock, speed):
    raise NotImplementedError


#A* Tie-Break
def run_astar_tiebreak(draw, grid, start, end, clock, speed):
    raise NotImplementedError


# Benchmark
# kembalikan dict per algoritma: {"avg_ms": median, "expanded": n, "path_len": n}
def run_benchmark_30x(grid, start, end):
    raise NotImplementedError