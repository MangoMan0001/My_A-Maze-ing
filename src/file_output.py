#!/usr/bin/env python3
"""迷路データをファイルに出力するためのモジュール."""

from mazegen import MazeGenerator


def output_maze(generator: MazeGenerator) -> None:
    """迷路データを規定のフォーマットでテキストファイルに出力します.

    迷路の各セルを16進数（0-F）で表現し、以下の形式で保存します。
    各ビットは「どの壁が閉じているか」を表します。
    （0:北, 1:東, 2:南, 3:西 のビットに対応）

    例:
        3 (0011) -> 北(1)と東(2)が閉じている（＝南と西が開いている）
        A (1010) -> 東(2)と西(8)が閉じている（= 北と西が開いている）

    ファイルフォーマット:
        1. 迷路のマップデータ（各行が16進数の文字列）
        2. 空行
        3. 入口座標 (x,y)
        4. 出口座標 (x,y)
        5. 最短経路 (N, E, S, W の文字列)

    Args:
        generator (MazeGenerator): 出力対象の迷路データを持つインスタンス.
            `maze`, `way`, `entry`, `exit`, `output_file` の属性が参照されます。
    """
    lines = []
    maze = generator.maze
    # リスト内の文字をつなげて一つの文字列とする
    way = "".join(c for c in generator.way)
    ex, ey = generator.entry
    gx, gy = generator.exit
    output_file = generator.output_file

    # 各cellを16進数文字列に
    for row in maze:
        str_row = "".join(f"{cell:X}" for cell in row)
        lines.append(str_row)

    # ファイルフォーマットの2~5
    lines.append("")
    lines.append(f"{ex},{ey}")
    lines.append(f"{gx},{gy}")
    lines.append(way)
    output = "\n".join(lines)

    # ファイルに書き出し
    with open(output_file, 'w') as f:
        f.write(output)


if __name__ == "__main__":
    pass
