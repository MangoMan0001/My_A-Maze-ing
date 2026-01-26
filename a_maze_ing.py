#!usr/bin/env python3
"""迷路生成プログラム実行モジュール."""

import sys
try:
    from src import config_parser, output_maze, MazeView, user_input_choice
    from mazegen import MazeGenerator
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)


def a_maze_ing() -> None:
    """迷路を生成し、最短経路と共にテキストファイルで出力する."""
    conf = config_parser(sys.argv)
    generator = MazeGenerator(conf)
    generator.generate()

    view = MazeView(generator)
    output_maze(generator)
    user_input_choice(generator, view)


if __name__ == "__main__":
    try:
        a_maze_ing()
    except Exception as e:
        print(f"Error: {e}")
