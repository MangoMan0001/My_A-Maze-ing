#!/usr/bin/env python3

HORIZON = "━━━"
VERTICAL = "┃"

CORNER1 = "┏"
CORNER2 = "┓"
CORNER3 = "┗"
CORNER4 = "┛"

WEDGE1 = "┣"
WEDGE2 = "┳"
WEDGE3 = "┫"
WEDGE4 = "┻"
WEDGE5 = "╋"

INIT_H = "   "
INIT_V = " "

PATH = "\x1b[44m   \x1b[0m"
WALL = "\x1b[47m   \x1b[0m"
START = "\x1b[42m  \x1b[0m"
GOAL = "\x1b[41m  \x1b[0m"
ROOT = "\x1b[43m  \x1b[0m"


def _gen_map(maze: list) -> list:
    """
    ASCII出力用マップへ変換する
    """

    result = [[INIT_V for _ in range(len(maze[0]) * 2 + 1)]
              for _ in range(len(maze) * 2 + 1)]
    for y in range(0, len(result), 2):
        for x in range(len(result[y])):
            result[y][x] = INIT_H
    result[0][0] = CORNER1
    result[0][-1] = CORNER2
    result[-1][0] = CORNER3
    result[-1][-1] = CORNER4
    for y, line in enumerate(maze):
        for x, cell in enumerate(line):
            vx = x * 2 + 1
            vy = y * 2 + 1
            result[vy][vx] = PATH
            if cell == 15:
                result[vy][vx] = WALL
            if cell & 1:
                result[vy - 1][vx] = HORIZON
            if cell & 2:
                result[vy][vx + 1] = VERTICAL
            if cell & 4:
                result[vy + 1][vx] = HORIZON
            if cell & 8:
                result[vy][vx - 1] = VERTICAL

    for y, line in enumerate(result):
        for x, cell in enumerate(line):
            if cell in (INIT_H, INIT_V):
                bit = 0
                if 0 < y and result[y - 1][x] == VERTICAL:  # .上に壁があるか
                    bit += 1
                if x < len(line) - 1 and result[y][x + 1] == HORIZON:  # .右に壁があるか
                    bit += 2
                if y < len(result) - 1 and result[y + 1][x] == VERTICAL:  # .下に壁があるか
                    bit += 4
                if 0 < x and result[y][x - 1] == HORIZON:  # .左に壁があるか
                    bit += 8

                if bit == 7:
                    result[y][x] = WEDGE1  # "┣"
                elif bit == 14:
                    result[y][x] = WEDGE2  # "┳"
                elif bit == 13:
                    result[y][x] = WEDGE3  # "┫"
                elif bit == 11:
                    result[y][x] = WEDGE4  # "┻"
                elif bit == 15:
                    result[y][x] = WEDGE5  # "╋"

                if bit == 10:
                    result[y][x] = "━"
                # if bit == 5:
                #     result[y][x] = "┃"

                if bit == 6:
                    result[y][x] = CORNER1  # "┏"
                if bit == 12:
                    result[y][x] = CORNER2  # "┓"
                if bit == 3:
                    result[y][x] = CORNER3  # "┗"
                if bit == 9:
                    result[y][x] = CORNER4  # "┛"
    return result


def visualize_ascii(maze: list) -> None:
    """
    ターミナルにvisualizeする
    受け取ったlistは二次元配列で、各要素の値を参照してasciiに変換する
    """

    maze = _gen_map(maze)
    for line in maze:
        for cell in line:
            print(cell, end="")
        print()


def load_maze(filename: str) -> list:
    """
    filenameをopenし、中身を1行ずつ二次元リストにして返す
    16進数か、のバリデーションもここで行う
    座標と経路のバリデーションや書式検証はここじゃない方がよき？？
    """

    maze = []
    file = open(filename, 'r')
    for line in file:
        if line.strip() == "":
            break
        maze.append([int(c, 16) for c in line.strip()])
    return maze


if __name__ == "__main__":
    maze = load_maze("test.txt")
    for line in maze:
        for cell in line:
            if cell < 10:
                print(" ", end="")
            print(cell, end=",")
        print()
#     maze = [[13, 6, 12, 6, 13, 5, 5, 4, 4, 5, 5, 6, 12, 5, 4, 5, 6, 12, 5, 6],
# [14, 10, 10, 9, 5, 5, 6, 11, 10, 12, 6, 10, 11, 12, 3, 14, 9, 3, 14, 10],
# [10, 9, 3, 12, 5, 6, 10, 12, 3, 10, 10, 9, 5, 3, 12, 1, 6, 12, 3, 10],
# [9, 4, 6, 9, 6, 10, 9, 3, 12, 3, 9, 7, 12, 4, 3, 14, 9, 2, 12, 3],
# [12, 3, 9, 6, 10, 9, 5, 5, 2, 12, 5, 5, 3, 9, 6, 8, 5, 3, 10, 14],
# [10, 12, 5, 3, 10, 14, 15, 12, 3, 10, 15, 15, 15, 14, 10, 10, 12, 5, 3, 10],
# [10, 9, 5, 6, 10, 10, 15, 9, 5, 1, 5, 7, 15, 10, 10, 11, 9, 6, 13, 2],
# [8, 5, 6, 10, 10, 10, 15, 15, 15, 14, 15, 15, 15, 10, 9, 4, 6, 9, 6, 10],
# [10, 14, 10, 10, 9, 2, 12, 6, 15, 10, 15, 13, 5, 0, 7, 10, 9, 7, 10, 10],
# [10, 10, 10, 10, 12, 3, 11, 10, 15, 10, 15, 15, 15, 10, 12, 3, 12, 5, 3, 10],
# [9, 2, 10, 11, 9, 5, 6, 8, 5, 2, 13, 5, 4, 2, 9, 5, 3, 12, 6, 10],
# [12, 3, 9, 4, 5, 7, 10, 9, 6, 9, 5, 5, 3, 9, 6, 12, 5, 3, 10, 10],
# [10, 12, 7, 9, 6, 12, 3, 12, 3, 12, 5, 5, 5, 7, 10, 9, 6, 12, 3, 10],
# [10, 9, 5, 6, 9, 3, 13, 2, 12, 1, 5, 6, 12, 5, 3, 12, 3, 10, 12, 2]]
    visualize_ascii(maze)
