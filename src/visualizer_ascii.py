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
        #     print(bits, end=",")
        # print()

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

    # for c_line in converted_maze:
    #     print(f"{c_line},")

    H = 2*height + 1
    W = 2*width + 1

    for x in range(W):
        converted_maze[0][x] = 1
        converted_maze[H-1][x] = 1
    for y in range(H):
        converted_maze[y][0] = 1
        converted_maze[y][W-1] = 1

    draw_ascii_maze(converted_maze)
    return (converted_maze)


def draw_ascii_maze(converted_maze, wall_color=0):
    WALL = f"\x1b[{wall_color}m██\x1b[0m"
    START = "\x1b[42m  \x1b[0m"
    GOAL = "\x1b[41m  \x1b[0m"
    PATH = "  "
    WALK_PATH = "足"

    for row in converted_maze:
        line = ""
        for cell in row:
            if cell == 1:
                line += WALL
            elif cell == 0:
                line += PATH
            elif cell == 2:
                line += START
            elif cell == 3:
                line += GOAL
            elif cell == 4:
                line += WALK_PATH
        print(line)

# if __name__ == "__main__":
#     pass
