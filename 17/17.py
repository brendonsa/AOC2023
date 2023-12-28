import numpy as np
from heapq import heappush, heappop

FILENAME = '17.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(np.array(list(map(int, list(line.strip())))))
    return np.vstack(data)


MOVES = {(1, 0), (0, 1), (-1, 0), (0, -1)}


def djikstra(data, min_path=1, max_path=3):
    end = (data.shape[0]-1, data.shape[1]-1)
    start = (0, 0)
    queue = [(0, start, 0, 0)]
    visited = set()
    while queue:
        heat, move, px, py = heappop(queue)
        x, y = move
        if (x, y) == end:
            return heat
        if (x, y, px, py) in visited:
            continue
        visited.add((x, y, px, py))
        for dx, dy in MOVES - {(px, py), (-px, -py)}:
            new_x = x
            new_y = y
            new_heat = heat
            for i in range(1, max_path+1):
                new_x = new_x + dx
                new_y = new_y + dy
                if 0 <= new_x < data.shape[0] and 0 <= new_y < data.shape[1]:
                    new_heat = new_heat + data[new_x, new_y]
                    if i >= min_path:
                        heappush(queue, (new_heat, (new_x, new_y), dx, dy))


data = read_data(FILENAME)
print(djikstra(data, 4, 10))
