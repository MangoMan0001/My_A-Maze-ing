#!usr/bin/env python3
import sys
from src import config_parser, visualize_ascii, output_maze
from mazegen import MazeGenerator


def a_maze_ing() -> None:
    """
    迷路を生成し、最短経路と共にテキストファイルで出力する。
    """

    conf = config_parser(sys.argv)
    generator = MazeGenerator(conf)
    generator.generate()
    visualize_ascii(generator.maze)
    output_maze(generator)


if __name__ == "__main__":
    a_maze_ing()
