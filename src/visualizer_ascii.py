#!/usr/bin/env python3
from mazegen import MazeGenerator


class MazeView:
    def __init__(self, generate: MazeGenerator):
        self.gen = generate
        self.wall_color = 0
        self.show_path = False

        self.wall = f"\x1b[{self.wall_color}m██\x1b[0m"
        self.start = "\x1b[43m  \x1b[0m"
        self.goal = "\x1b[43m  \x1b[0m"
        self.path = "  "
        self.walk_path = "・"
        self.forty_two = "\x1b[43m  \x1b[0m"

    def set_wall_color(self, color):
        self.wall_color = color
        self.wall = f"\x1b[{self.wall_color}m██\x1b[0m"

    def toggle_path(self):
        self.show_path = not self.show_path

    def draw(self):
        grid = self.gen._grid
        path = self.gen._path

        temp = [row[:] for row in grid]

        if self.show_path and path:
            for x, y in path:
                if temp[y][x] == 0:
                    temp[y][x] = 4  # 足跡
        for row in temp:
            line = ""
            for cell in row:
                if cell == 1:
                    line += self.wall
                elif cell == 0:
                    line += self.path
                elif cell == 2:
                    line += self.start
                elif cell == 3:
                    line += self.goal
                elif cell == 4:
                    line += self.walk_path
                elif cell == 5:
                    line += self.forty_two
            print(line)


if __name__ == "__main__":
    pass
