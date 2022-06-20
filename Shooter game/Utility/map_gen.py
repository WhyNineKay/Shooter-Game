from Utility import globs
from Utility import entities

map_array = [
    [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
]


def create_walls() -> None:
    for i, row in enumerate(map_array):
        for j, col in enumerate(row):
            if col == 1:
                globs.walls.append(entities.Wall(j * 100, i * 100, 100, 100))

