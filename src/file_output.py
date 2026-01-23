#!/usr/bin/env python3
from mazegen import MazeGenerator


def output_maze(generator: MazeGenerator) -> None:
    """
    迷路をtxtファイル形式で出力する。
    条件は以下の通り

        ・各セル一つに付き16進数で記述
        ・各桁はどの壁が閉じているのかを符号化する
            0:北 1:東 2:南 3:西
            ex. 3 -> 0011 -> 南壁と西壁が開いている
                10 -> 1010 -> 東西の壁がふさがっている
        ・セルは1行に付き1行で保存される
        ・迷路の後、空行に続いて以下の三要素が各行に分けて出力される。
            1.入口座標
            2.出口座標
            3.最短経路(N, E, S, W)
        ・すべての行は改行コードで終了する
    """

    lines = []
    maze = generator.maze
    path = generator.path
    entry = generator.entry
    exit = generator.exit
    output_file = generator.output_file

    for row in maze:
        row = "".join(f"{cell:X}" for cell in row)
        lines.append(row)
    lines.append("")
    lines.append(f"{entry}")
    lines.append(f"{exit}")
    lines.append(f"{path}")
    output = "\n".join(lines)

    with open(output_file, 'w') as f:
        f.write(output)


if __name__ == "__main__":
    pass
