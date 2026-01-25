#!/usr/bin/env python3
"""迷路をASCIIとしてコンソールに表示するモジュール."""


from mazegen import MazeGenerator


class MazeView:
    """迷路の描画（表示）を担当するクラス.

    MazeGeneratorから迷路データを受け取り、コンソール上に
    色付きのASCII文字としてレンダリングします。

    Attributes:
        _gen (MazeGenerator): 迷路生成ロジックを持つインスタンス.
        _show_path (bool): 正解ルートを表示するかどうかのフラグ.
        _wall (str): 壁を表示するための文字列（ANSIエスケープシーケンス含む）.
        _start (str): スタート地点の表示文字.
        _goal (str): ゴール地点の表示文字.
        _path (str): 通路（床）の表示文字.
        _walk_path (str): 正解ルート（足跡）の表示文字.
        _forty_two (str): '42'の文字部分を表す特別な表示文字.
    """

    def __init__(self, generate: MazeGenerator):
        """MazeViewを初期化します.

        Args:
            generate (MazeGenerator): 描画対象となるMazeGeneratorインスタンス.
        """
        self._gen = generate
        self._show_path = False
        self._wall = "\x1b[0m██\x1b[0m"
        self._start = "\x1b[43m  \x1b[0m"
        self._goal = "\x1b[43m  \x1b[0m"
        self._path = "  "
        self._walk_path = "・"
        self._forty_two = "\x1b[43m  \x1b[0m"

    def set_wall_color(self, color: int) -> None:
        """壁の色を変更します.

        ANSIエスケープシーケンスを使用して、壁の表示色を更新します。

        Args:
            color (int): 設定したい色のANSIカラーコード（例: 31=赤, 32=緑）.
        """
        self._wall = f"\x1b[{color}m██\x1b[0m"

    def toggle_path(self) -> None:
        """正解ルートの表示/非表示を切り替えます."""
        self._show_path = not self._show_path

    def draw(self) -> None:
        """現在の迷路の状態をコンソールに出力します.

        _gen（MazeGenerator）が持つグリッドデータを読み込み、
        設定された文字（壁、床、スタート、ゴールなど）に変換して表示します。
        _show_pathフラグがTrueの場合は、正解ルートも重ねて描画します。
        """
        grid = self._gen._grid
        path = self._gen._path

        # グリッドをコピーして、描画用の一時データを作成
        temp = [row[:] for row in grid]

        if self._show_path and path:
            for x, y in path:
                if temp[y][x] == 0:
                    temp[y][x] = 4  # 足跡としてマーク
        for row in temp:
            line = ""
            for cell in row:
                if cell == 1:
                    line += self._wall
                elif cell == 0:
                    line += self._path
                elif cell == 2:
                    line += self._start
                elif cell == 3:
                    line += self._goal
                elif cell == 4:
                    line += self._walk_path
                elif cell == 5:
                    line += self._forty_two
            print(line)
        print()


if __name__ == "__main__":
    pass
