#!/usr/bin/env python3
from error_case import error_case


def load_maze(filename: str) -> list:
    """
    filenameをopenし、中身を1行ずつ二次元リストにして返す
    16進数か、のバリデーションもここで行う
    座標と経路のバリデーションや書式検証はここじゃない方がよき？？
    """

    maze = []
    try:
        file = open(filename, 'r')
        for line in file:
            if line.strip() == "":
                break
            maze.append([int(c, 16) for c in line.strip()])
    except Exception as e:
        error_case(e)


def visualize_ascii(maze: list) -> None:
    """
    ターミナルにvisualizeする
    """

    


if __name__ == "__main__":
    load_maze("test_output.txt")
