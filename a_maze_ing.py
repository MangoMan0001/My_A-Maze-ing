#!usr/bin/env python3
import sys
from src import config_parser, visualize_ascii
from mazegen import MazeGenerator


def a_maze_ing() -> None:
    """
    迷路を生成し、最短経路と共にテキストファイルで出力する。
    """

    conf = config_parser(sys.argv)
    conf = {'WIDTH': 30,
            "HEIGHT": 30,
            "ENTRY": (0, 0),
            "EXIT": (20, 20),
            "OUTPUT_FILE": 'maze.txt',
            "PERFECT": True,
            "SEED": 42,
            "P_MODE": False}
    print(conf)
    generator = MazeGenerator(conf)
    generator.generate()
    visualize_ascii(generator.maze)


if __name__ == "__main__":
    a_maze_ing()
