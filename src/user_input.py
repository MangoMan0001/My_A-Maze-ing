import random
import os
from src import output_maze, MazeView
from mazegen import MazeGenerator

choice_txt = """=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze random colors
4. PERFECT flag switch
5. Quit"""


def user_input_choice(generator: MazeGenerator, view: MazeView):
    view.draw()
    print(choice_txt)
    while True:
        try:
            user_input = int(input("Choice? (1-5):"))
        except BaseException:
            print("Please select from 1-5")
            continue

        if user_input == 1:
            os.system('clear')
            generator.seed = random.randint(1, 1000)
            generator.generate()
            view.draw()
            output_maze(generator)
            print(choice_txt)
            continue

        elif user_input == 2:
            os.system('clear')
            view.set_wall_color(random.randint(30, 39))
            generator.conf.report_status()
            view.draw()
            print(choice_txt)
            continue

        elif user_input == 3:
            os.system('clear')
            view.toggle_path()
            generator.conf.report_status()
            view.draw()
            print(choice_txt)
            continue

        elif user_input == 4:
            # os.system('clear')
            if generator.perfect:
                generator.perfect = False
            else:
                generator.perfect = True
            generator.generate()
            view.draw()
            output_maze(generator)
            print(choice_txt)
            continue

        elif user_input == 5:
            os.system('clear')
            break

        else:
            print("Please select from 1-5")
