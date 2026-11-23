import random

def create_maze(rows, seed, remove_walls_prob=0.0):
    rnd = random.Random(seed)
    walls = set()
    for r in range(rows):
        for c in range(rows):
            walls.add((r, c))

    start = (1, 1)
    walls.discard(start)
    stack = [start]
    visited = {start}

    while stack:
        cr, cc = stack[-1]
        neighbors = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = cr + dr, cc + dc
            if 1 <= nr < rows - 1 and 1 <= nc < rows - 1 and (nr, nc) not in visited:
                neighbors.append((nr, nc, cr + dr // 2, cc + dc // 2))

        if neighbors:
            nr, nc, wr, wc = rnd.choice(neighbors)
            visited.add((nr, nc))
            walls.discard((nr, nc))
            walls.discard((wr, wc))
            stack.append((nr, nc))
        else:
            stack.pop()

    walls.discard((1, 1))
    walls.discard((rows - 2, rows - 2))

    if remove_walls_prob > 0:
        for r in range(1, rows - 1):
            for c in range(1, rows - 1):
                if (r, c) in walls and rnd.random() < remove_walls_prob:
                    walls.discard((r, c))

    return walls


def apply_scenario(scenario_num, rows):
    walls = set()
    start_pos = (1, 1)
    goal_pos = (rows - 2, rows - 2)

    for r in range(rows):
        for c in range(rows):
            if r == 0 or r == rows - 1 or c == 0 or c == rows - 1:
                walls.add((r, c))

    if scenario_num == 1:
        pass

    elif scenario_num == 2:
        rnd = random.Random(2026)
        for r in range(1, rows - 1):
            for c in range(1, rows - 1):
                if (r, c) not in (start_pos, goal_pos) and rnd.random() < 0.20:
                    walls.add((r, c))
        for i in range(1, rows - 1):
            walls.discard((1, i))
            walls.discard((i, rows - 2))

    elif scenario_num == 3:
        walls = create_maze(rows, seed=42, remove_walls_prob=0.30)
        for r in range(rows):
            walls.add((r, 0)); walls.add((r, rows - 1))
            walls.add((0, r)); walls.add((rows - 1, r))

    elif scenario_num == 4:
        walls = create_maze(rows, seed=101, remove_walls_prob=0.0)
        for r in range(rows):
            walls.add((r, 0)); walls.add((r, rows - 1))
            walls.add((0, r)); walls.add((rows - 1, r))

    elif scenario_num == 5:
        walls = create_maze(rows, seed=2026, remove_walls_prob=0.15)
        for r in range(rows):
            walls.add((r, 0)); walls.add((r, rows - 1))
            walls.add((0, r)); walls.add((rows - 1, r))

    elif scenario_num == 6:
        gr, gc = goal_pos
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            walls.add((gr + dr, gc + dc))

    return walls, start_pos, goal_pos
