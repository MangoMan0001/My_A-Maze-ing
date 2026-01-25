#!/user/bin/env python3
"""ユーザー入力を処理し、アプリケーションのメインループを制御するモジュール."""

import random
import os
from src import output_maze, MazeView
from mazegen import MazeGenerator

# メニューテキスト
choice_txt = """=== A-Maze-ing ===
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze random colors
4. PERFECT flag switch
5. Quit"""


def user_input_choice(generator: MazeGenerator, view: MazeView) -> None:
    """ユーザーからの入力を受け付け、迷路の再生成や設定変更を行います.

    この関数は無限ループで実行され、'5'が選択されるまで終了しません。

    Args:
        generator (MazeGenerator): 操作対象の迷路生成インスタンス.
        view (MazeView): 操作対象の迷路描画インスタンス.
    """
    view.draw()
    print(generator.report)
    print()
    print(choice_txt)
    while True:
        try:
            # input()は文字列を返すのでintに変換
            user_input = int(input("Choice? (1-5):"))
        except BaseException:
            # 数字以外が入力された場合にキャッチ
            print("Please select from 1-5")
            continue

        # SEEDを変えて迷路の再生成
        if user_input == 1:
            os.system('clear')
            generator.seed = random.randint(1, 1000)
            generator.generate()
            view.draw()
            print(generator.report)
            print()
            output_maze(generator)
            print(choice_txt)
            continue

        # 経路の表示/非表示
        elif user_input == 2:
            os.system('clear')
            view.toggle_path()
            view.draw()
            print(generator.report)
            print()
            print(choice_txt)
            continue

        # カラーコードの再選択
        elif user_input == 3:
            os.system('clear')
            # .ランダムなANSIカラーコードを設定
            view.set_wall_color(random.randint(30, 39))
            view.draw()
            print(generator.report)
            print()
            print(choice_txt)
            continue

        # PERFECTフラグの有効/無効
        elif user_input == 4:
            os.system('clear')
            generator.perfect = not generator.perfect
            generator.generate()
            view.draw()
            print(generator.report)
            print()
            output_maze(generator)
            print(choice_txt)
            continue

        # プログラム終了
        elif user_input == 5:
            os.system('clear')
            break

        else:
            print("Please select from 1-5")
