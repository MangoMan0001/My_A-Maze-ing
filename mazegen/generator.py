#!/usr/bin/env python3
import random


class MazeGenerator:
    """
    conf
    creaat maze
    """

    def __init__(self, conf: dict = {}):
        """
        initiialize
        """

        self._maze = []
        self._path = []
        self._visited = []
        self._width = conf.get('WIDTH', 20)  # .number of cell
        self._height = conf.get('HEIGHT', 15)
        self._entry = conf.get('ENTRY', (0, 0))
        self._goal = conf.get('GOAL', (19, 14))
        self._seed = conf.get('SEED', 42)

    @property  # getter
    def maze(self) -> list:
        return self._maze

    def generate(self):
        seed = self._seed
        random.seed(seed) if seed > 0 else random.seed(42)
        self._seed = seed
        self._init_maze()
        self._generate_maze(*self._entry)
        self._find_path()

    def _init_maze(self) -> None:
        """
        _init_maze の Docstring
        """
        ft = [[1, 0, 0, 0, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 0, 1, 1, 1],
              [0, 0, 1, 0, 1, 0, 0],
              [0, 0, 1, 0, 1, 1, 1]]
        self._maze = [[15 for _ in range(self._width)]
                      for _ in range(self._height)]
        self._visited = [[0 for _ in range(self._width)]
                         for _ in range(self._height)]
        start_x = (self._width - len(ft[0])) // 2
        start_y = (self._height - len(ft)) // 2
        for y in range(len(ft)):
            for x in range(len(ft[0])):
                if ft[y][x]:
                    self._visited[start_y + y][start_x + x] = 1

    def _generate_maze(self, x: int, y: int) -> None:
        """
        _generate_maze の Docstring
        """
        if self._visited[y][x] == 1:
            return
        # (x軸移動, y軸移動, 自身から見た破壊すべき壁ビット, 移動先から見た破壊すべき壁ビット)
        wasd = [(-1, 0, 8, 2, "W"), (0, -1, 1, 4, "S"), (1, 0, 2, 8, "E"), (0, 1, 4, 1, "N")]
        random.shuffle(wasd)
        self._visited[y][x] = 1
        for d in wasd:
            nx = x + d[0]  # .次に進むx座標 next_x
            ny = y + d[1]  # .次に進むy座標 next_y
            mw = d[2]  # .自分から見た壁ビット my_wall
            yw = d[3]  # .相手から見た壁ビット your_wall
            if not (0 <= nx < self._width and 0 <= ny < self._height):
                continue
            if self._visited[ny][nx] == 0:
                self._maze[y][x] -= mw
                self._maze[ny][nx] -= yw
                self._generate_maze(nx, ny)
        return

    def _find_path(self) -> None:
        """
        _find_path の Docstring
        """


if __name__ == "__main__":
    pass
