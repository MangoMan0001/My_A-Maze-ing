#!/usr/bin/env python3
from mazegen import MazeGenerator


class MazeView:
    def __init__(self, generate: MazeGenerator):
        self._gen = generate
        self._show_path = False

        self._wall = "\x1b[0m██\x1b[0m"
        self._start = "\x1b[43m  \x1b[0m"
        self._goal = "\x1b[43m  \x1b[0m"
        self._path = "  "
        self._walk_path = "・"
        self._forty_two = "\x1b[43m  \x1b[0m"

    def set_wall_color(self, color) -> None:
        self._wall = f"\x1b[{color}m██\x1b[0m"

    def toggle_path(self):
        self._show_path = not self._show_path

    def draw(self):
        grid = self._gen._grid
        path = self._gen._path

        temp = [row[:] for row in grid]

        if self._show_path and path:
            for x, y in path:
                if temp[y][x] == 0:
                    temp[y][x] = 4  # 足跡
        for row in temp:
            line = ""
            for cell in row:
                if cell == 1:
                    line += self._wall
                elif cell == 0:
                    line += self._path
                elif cell == 2:
                    line += self._start
                elif cell == 3:
                    line += self._goal
                elif cell == 4:
                    line += self._walk_path
                elif cell == 5:
                    line += self._forty_two
            print(line)
        print()


if __name__ == "__main__":
    pass
