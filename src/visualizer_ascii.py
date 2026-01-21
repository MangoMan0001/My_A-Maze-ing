#!/usr/bin/env python3


def visualize_ascii(maze: list) -> None:
    width = len(maze[0])
    height = len(maze)

    converted_maze = []
    for rows in range(2 * height + 1):
        row = []
        for cols in range(2 * width + 1):
            row.append(1)
        converted_maze.append(row)

    print()

    for line in maze:
        for info in line:
            bits = bin(info)[2:].zfill(4)
            print(bits, end=",")
        print()

    x, y = 0, 0          # 左上セルだけ
    for y in range(height):
        cy = 2*y + 1
        for x in range(width):
            cx = 2*x + 1
            info = maze[y][x]
            bits = bin(info)[2:].zfill(4)

            converted_maze[cy][cx] = 0

            if bits[0] == "0":  # 左
                converted_maze[cy][cx-1] = 0
            if bits[1] == "0":  # 下
                converted_maze[cy+1][cx] = 0
            if bits[2] == "0":  # 右
                converted_maze[cy][cx+1] = 0
            if bits[3] == "0":  # 上
                converted_maze[cy-1][cx] = 0

    for c_line in converted_maze:
        print(f"{c_line},")

    H = 2*height + 1
    W = 2*width + 1

    for x in range(W):
        converted_maze[0][x] = 1
        converted_maze[H-1][x] = 1
    for y in range(H):
        converted_maze[y][0] = 1
        converted_maze[y][W-1] = 1

    draw_ascii_maze(converted_maze)


def draw_ascii_maze(converted_maze):
    WALL = "██"
    START = "S"
    GOAL = "G"
    PATH = "  "
    WALK_PAHT = "."

    for row in converted_maze:
        line = ""
        for cell in row:
            if cell == 1:
                line += WALL
            elif cell == 0:
                line += PATH
            elif cell == "S":
                line += START
            elif cell == "G":
                line += GOAL

        print(line)


if __name__ == "__main__":
    pass
