import random
import os
from src import output_maze
from mazegen import MazeGenerator


def user_input_choice(generator: MazeGenerator, view):
    view.draw()
    while True:
        user_input = int(input("Input something: "))

        if user_input == 1:
            os.system('clear')
            generator.seed = random.randint(1, 1000)
            print(generator.seed)
            generator.generate()
            view.draw()
            output_maze(generator)

        elif user_input == 2:
            os.system('clear')
            view.set_wall_color(random.randint(30, 39))
            generator.conf.report_status()
            view.draw()

        elif user_input == 3:
            os.system('clear')
            view.toggle_path()
            view.draw()

        elif user_input == 4:
            os.system('clear')
            break

        elif user_input == 5:
            os.system('clear')
            if generator.perfect:
                generator.perfect = False
            else:
                generator.perfect = True
            generator.generate()
            view.draw()
            output_maze(generator)

        else:
            print("matigaetmasuyo number ok???")
