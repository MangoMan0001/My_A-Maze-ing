from mazegen import MazeGenerator, generator
import random
from src import visualizer_ascii, draw_ascii_maze


def user_input_choice(generator: MazeGenerator, maze) -> None:
    """
    ユーザーのインプットによって出力を変える
    """

    while (True):
        user_input = int(input("Input something:"))
        if user_input == 1:
            generator.setseed(random.randint(1, 1000))
            generator.generate()
            visualizer_ascii(generator.maze)
            continue
        elif user_input == 2:
            wall_color = random.randint(30, 39)
            draw_ascii_maze(maze, wall_color)
            continue
        elif user_input == 3:
            generator.find_path()
            continue
        elif user_input == 4:
            break
        print("matigaetmasuyo number ok???")
        continue
