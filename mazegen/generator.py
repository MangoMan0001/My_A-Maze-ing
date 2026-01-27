#!/usr/bin/env python3
"""迷路生成のコアロジックおよび設定管理を行うモジュール.

設定値の検証 - Pydantic
迷路生成 - 穴掘り法（DFS）
最短経路算出 - 幅優先探索（BFS）
"""

import random
import sys
import ast
from pathlib import Path
from pydantic import BaseModel, Field, model_validator, \
                     field_validator, ValidationError, ConfigDict
from typing import Annotated, Any
from collections import deque

PositiveInt = Annotated[int, Field(ge=0, description="正の整数型")]


class MazeConfig(BaseModel):
    """MazeGeneratorの設定値を保持・検証するデータクラス.

    Pydanticを使用して、型チェックと値の範囲を検証する。

    Attributes:
        width (int): 迷路の幅（0〜42）。デフォルト(20)
        height (int): 迷路の高さ（0〜42）。デフォルト(15)
        entry (tuple): スタート地点の座標 (x, y)。デフォルト(0, 0)
        exit (tuple): ゴール地点の座標 (x, y)。デフォルト(19, 14)
        output_file (Path): 出力ファイルのパス。デフォルト('maze.txt')
        seed (int): 乱数シード値（0〜1000）。デフォルト(42)
        perfect (bool): 完全迷路のフラグ。デフォルト(True)
    """
    model_config = ConfigDict(validate_assignment=True)
    # .[弾くもの]intと数字以外のstr
    width: int = Field(alias='WIDTH',
                       ge=0,
                       le=42,
                       default=20,
                       description="迷路の横幅")
    height: int = Field(alias='HEIGHT',
                        ge=0,
                        le=42,
                        default=15,
                        description="迷路の縦幅")
    # .[弾くもの]tuple以外
    entry: tuple[PositiveInt, PositiveInt] = Field(alias="ENTRY",
                                                   default=(0, 0),
                                                   description="迷路のスタート地点")
    exit: tuple[PositiveInt, PositiveInt] = Field(alias="EXIT",
                                                  default=(19, 14),
                                                  description="迷路のゴール地点")
    # .[弾くもの]数字、リスト、dict、Noneなど
    output_file: Path = Field(alias="OUTPUT_FILE",
                              default=Path("maze.txt"),
                              description="出力ファイル名")
    seed: int = Field(alias="SEED",
                      ge=0,
                      le=1000,
                      default=42,
                      description="迷路の乱数種")
    # .[弾くもの]boolと文字のboll以外
    perfect: bool = Field(alias="PERFECT",
                          default=True,
                          description="PERFECTフラグ")

    # .インスタンス作成前に実行されるためclassmethodが必要
    @field_validator('output_file')  # .何も書かないとafterになる
    @classmethod
    def _validate_file_name(cls, v: Any) -> Any:
        """出力ファイル名の妥当性を検証/修正する.

        - 拡張子 '.txt' がなければ付与
        - 同名のディレクトリが存在しないか確認
        - ファイルへの書き込み権限があるかテスト

        Args:
            v (Any): 入力されたファイルパス。

        Returns:
            Any: 検証・修正済みのPathオブジェクト。

        Raises:
            ValueError: ディレクトリと同名の場合や書き込み権限がない場合。
        """
        if v.suffix != '.txt':
            v = v.with_suffix('.txt')

        if v.exists() and v.is_dir():
            raise ValueError(f"A directory named {v.name} already exists.")

        try:
            if v.exists():
                with open(v, 'a'):
                    pass
            else:
                with open(v, 'x'):
                    pass
                v.unlink()
        except OSError as e:
            raise ValueError(f"File_NameError: {e}")
        return v

    @field_validator('entry', 'exit', mode='before')
    @classmethod
    def _rescue_invalid_values_tuple(cls, v: Any) -> Any:
        """タプルの入力値を安全にパースします.

        設定ファイルから文字列として "(0, 0)" のように渡された場合、
        Pythonのタプルオブジェクトに変換します。

        Args:
            v (Any): 入力値（タプルまたは文字列）。

        Returns:
            Any: 変換後のタプル、または元の値。
        """
        if isinstance(v, tuple):
            return v
        if isinstance(v, str):
            try:
                # 文字列でもそのままその型として値に変換してくれる
                return ast.literal_eval(v)
            except Exception:
                return v
        return v

    @model_validator(mode="after")
    def _after_valid_mazeconfig(self) -> "MazeConfig":
        """複数のフィールドにまたがる整合性を検証します.

        - ENTRY/EXITが迷路の範囲内に収まっているか
        - ENTRYとEXITが同じ座標でないか

        Returns:
            MazeConfig: 検証済みのインスタンス。

        Raises:
            ValueError: 座標が範囲外、または重複している場合。
        """
        w, h = self.width, self.height
        ex, ey = self.entry
        gx, gy = self.exit

        if w <= ex or h <= ey:
            raise ValueError(f"ENTRY {ex, ey} exceeds maze size {w, h}")
        if w <= gx or h <= gy:
            raise ValueError(f"EXIT {gx, gy} exceeds maze size {w, h}")
        if self.entry == self.exit:
            raise ValueError(f"ENTRY {ex, ey} and EXIT {gx, gy} overlap")
        return self

    def report_status(self) -> str:
        """MazeGeneratorの現在の設定を出力する."""
        all_fields = self.model_fields.keys()
        set_fields = self.model_fields_set
        report_lines = ["===Current settings==="]

        for name in all_fields:
            value = getattr(self, name)
            if name in set_fields:
                report_lines.append(f"{name.upper()}: {value}")
            else:
                report_lines.append(f"{name.upper()} (Default): {value}")

        return "\n".join(line for line in report_lines)


class MazeGenerator:
    """迷路の生成と経路探索を行うメインクラス.

    Attributes:
        _conf (MazeConfig): 検証済みの設定オブジェクト。
        _maze (list): 生成された迷路データ（壁情報）。
        _path (list): スタートからゴールへの最短経路（座標リスト）。
        _way (list): 最短経路の方角リスト（N, E, S, W）。
        _grid (list): 描画・探索用に拡張されたグリッドデータ。
        _visited (list): 迷路生成時の訪問済み管理フラグ。
        _report (str): 現在迷路の設定
    """

    def __init__(self, confdict: dict[str, Any] | None = None):
        """MazeGeneratorを初期化します.

        Args:
            confdict (dict, optional): 設定値の辞書。指定がない場合はデフォルト値が使用されます。
        """
        try:
            if confdict is None:
                confdict = {}
            self._conf = MazeConfig(**confdict)

            self._maze: list[list[int]] = []
            self._path: list[tuple[int, int]] = []
            self._way: list[str] = []
            self._grid: list[list[int]] = []
            self._visited: list[list[int]] = []
            self._report: str

            # ショートカットの初期化
            self._width = self._conf.width
            self._height = self._conf.height
            self._entry = self._conf.entry
            self._exit = self._conf.exit
            self._output_file = self._conf.output_file
            self._seed = self._conf.seed
            self._perfect = self._conf.perfect

        except ValidationError as e:
            print("Validation error:")
            for err in e.errors():
                location = err['loc'][0] if err['loc'] else "Model Rules"
                print(f"    - {location}: {err['msg']}")
                print(f"      input:({err['input']})")
            sys.exit(1)

    # --- Properties (Getters & Setters) ---

    @property  # getter
    def conf(self) -> MazeConfig:
        """現在の設定オブジェクトを返します."""
        return self._conf

    @property  # getter
    def maze(self) -> list[list[int]]:
        """迷路の壁データ（2次元配列）を返します."""
        return self._maze

    @property  # getter
    def path(self) -> list[tuple[int, int]]:
        """最短経路の座標リストを返します."""
        return self._path

    @property  # getter
    def way(self) -> list[str]:
        """最短経路の方角リストを返します."""
        return self._way

    @property  # getter
    def grid(self) -> list[list[int]]:
        """描画用の拡張グリッドデータを返します."""
        return self._grid

    @property  # getter
    def report(self) -> str:
        """現在迷路の設定を返します."""
        return self._report

    @property  # getter
    def width(self) -> int:
        """迷路の幅を返します."""
        return self._width

    @width.setter  # setter
    def width(self, value: int) -> None:
        """迷路の幅を更新します."""
        self._conf.width = value
        self._width = value
        print(f"WIDTH has been changed to {value}")

    @property  # getter
    def height(self) -> int:
        """迷路の高さを返します."""
        return self._height

    @height.setter  # setter
    def height(self, value: int) -> None:
        """迷路の高さを更新します."""
        self._conf.height = value
        self._height = value
        print(f"HEIGHT has been changed to {value}")

    @property  # getter
    def entry(self) -> tuple[int, int]:
        """スタート地点の座標を返します."""
        return self._entry

    @entry.setter  # setter
    def entry(self, value: tuple[int, int]) -> None:
        """スタート地点の座標を更新します."""
        self._conf.entry = value
        self._entry = value
        print(f"ENTRY has been changed to {value}")

    @property  # getter
    def exit(self) -> tuple[int, int]:
        """ゴール地点の座標を返します."""
        return self._exit

    @exit.setter  # setter
    def exit(self, value: tuple[int, int]) -> None:
        """ゴール地点の座標を更新します."""
        self._conf.exit = value
        self._exit = value
        print(f"EXIT has been changed to {value}")

    @property  # getter
    def output_file(self) -> Path:
        """出力ファイルのパスを返します."""
        return self._output_file

    @output_file.setter  # setter
    def output_file(self, value: Path) -> None:
        """出力ファイルのパスを更新します."""
        self._conf.output_file = value
        self._output_file = value
        print(f"EXIT has been changed to {value}")

    @property  # getter
    def seed(self) -> int:
        """現在の乱数シード値を返します."""
        return self._seed

    @seed.setter  # setter
    def seed(self, value: int) -> None:
        """乱数シード値を更新します."""
        self._conf.seed = value
        self._seed = value
        print(f"SEED has been changed to {value}")

    @property  # getter
    def perfect(self) -> bool:
        """Perfectフラグの状態を返します."""
        return self._perfect

    @perfect.setter  # setter
    def perfect(self, value: bool) -> None:
        """Perfectフラグを更新します."""
        self._conf.perfect = value
        self._perfect = value
        print(f"PEFECT has been changed to {value}")

    # --- Core Methods ---

    def generate(self) -> None:
        """迷路生成のメインプロセスを実行します.

        1. シード値の設定
        2. 迷路の初期化（'42'ロゴの配置など）
        3. 穴掘り法による迷路構築
        4. 壁崩し（Not Perfectの場合）
        5. 最短経路の探索
        6. ステータスのレポート
        """
        seed = self._seed
        random.seed(seed) if seed > 0 else random.seed(42)

        self._init_maze()
        self._generate_maze(*self._entry)

        if not self._perfect:
            self._break_the_wall()

        self._find_path()
        self._report = self.conf.report_status()

    def _init_maze(self) -> None:
        """迷路配列を初期化し、可能であれば中央に'42'のロゴを配置します.

        すべてのセルを壁（15 = 1111）で埋め、visited配列をリセットします。
        迷路サイズが十分大きい場合、中央に'42'の形に通路を掘ります。
        """
        # 42のビットマップ (1:壁, 0:通路)
        ft = [[1, 0, 0, 0, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 0, 1, 1, 1],
              [0, 0, 1, 0, 1, 0, 0],
              [0, 0, 1, 0, 1, 1, 1]]

        self._maze = [[15 for _ in range(self._width)]
                      for _ in range(self._height)]
        self._visited = [[0 for _ in range(self._width)]
                         for _ in range(self._height)]

        if 8 < self._width and 6 < self._height:
            start_x = (self._width - len(ft[0])) // 2
            start_y = (self._height - len(ft)) // 2
            for y in range(len(ft)):
                for x in range(len(ft[0])):
                    if ft[y][x]:  # ビットマップが１なら
                        # 一度訪れたフラグを立てて、後の迷路生成アルゴリズムから浮かす
                        self._visited[start_y + y][start_x + x] = 1
            self._validate_maze()
            return
        print("MazeGenerator Warning: maze is too small to add '42' in it")
        print("It must be at least (9, 7).")

    def _validate_maze(self) -> None:
        """42内にENTRYやEXITが含まれていないかを検証する."""
        try:
            for y, line in enumerate(self._visited):
                for x, cell in enumerate(line):
                    if (x, y) == self._entry and cell:
                        raise ValueError(f"42 and ENTRY {self._entry} overlap")
                    if (x, y) == self._exit and cell:
                        raise ValueError(f"42 and EXIT {self._entry} overlap")
        except ValueError as e:
            print(f"ValueError: {e}")
            sys.exit(1)

    def _generate_maze(self, x: int, y: int) -> None:
        """再帰的な穴掘り法（DFS）を用いて迷路を生成します.

        Args:
            x (int): 現在のx座標.
            y (int): 現在のy座標.
        """
        # 一度訪れたことがあるなら足を止める
        if self._visited[y][x] == 1:
            return

        # (x軸移動, y軸移動, 自身から見た破壊すべき壁ビット, 移動先から見た破壊すべき壁ビット)
        wasd = [(-1, 0, 8, 2, 'W'), (0, -1, 1, 4, 'S'),
                (1, 0, 2, 8, 'E'), (0, 1, 4, 1, 'N')]

        random.shuffle(wasd)
        self._visited[y][x] = 1

        for d in wasd:
            nx = x + d[0]   # .次に進むx座標 next_x
            ny = y + d[1]   # .次に進むy座標 next_y
            mw = d[2]       # .自分から見た壁ビット my_wall
            yw = d[3]       # .相手から見た壁ビット your_wall

            # マップ外に出ないように
            if not (0 <= nx < self._width and 0 <= ny < self._height):
                continue
            # その先に訪れていなければ壁を破壊して進む
            if self._visited[ny][nx] == 0:
                self._maze[y][x] -= mw
                self._maze[ny][nx] -= yw
                self._generate_maze(nx, ny)

    def _break_the_wall(self) -> None:
        """3つ壁があるマスの壁をランダムに1枚破壊する.

        Perfect迷路（分岐のみでループがない）を崩し、
        複数のルートが存在する迷路にします。
        """
        # (x軸移動, y軸移動, 自身から見た破壊すべき壁ビット, 移動先から見た破壊すべき壁ビット)
        wasd = [(-1, 0, 8, 2, 'W'), (0, -1, 1, 4, 'S'),
                (1, 0, 2, 8, 'E'), (0, 1, 4, 1, 'N')]

        for y, line in enumerate(self._maze):
            for x, cell in enumerate(line):

                # 3つの壁に囲われたcellなら
                if cell in (14, 13, 11, 7):
                    random.shuffle(wasd)

                    # 方角をランダムに選択
                    for d in wasd:
                        nx = x + d[0]   # .破壊先のx座標 next_x
                        ny = y + d[1]   # .破壊先のy座標 next_y
                        mw = d[2]       # .自分から見た壁ビット my_wall
                        yw = d[3]       # .相手から見た壁ビット your_wall

                        # マップ外に出ないように
                        if not (0 <= nx < self._width and
                                0 <= ny < self._height):
                            continue
                        # 入口/出口なら
                        if (x, y) in (self._entry, self._exit):
                            continue
                        # 42だったら
                        if self._maze[ny][nx] == 15:
                            continue
                        # 選ばれた方角に壁があれば破壊
                        if cell & mw:
                            self._maze[y][x] -= mw
                            self._maze[ny][nx] -= yw
                            break

    def _convert_hex_maze_to_grid(self) -> None:
        """16進数(ビット)表現の迷路を、探索用のグリッド形式に展開します.

        壁と通路を明確にするため、1セルを 2x+1 のサイズに拡張します。
        0: 通路, 1: 壁, 5: 42ロゴ
        """
        width = self._width
        height = self._height

        self._grid = [[1 for _ in range(2 * width + 1)]
                      for _ in range(2 * height + 1)]

        for y in range(height):
            gy = 2*y + 1
            for x in range(width):
                gx = 2*x + 1
                info = self._maze[y][x]
                bits = bin(info)[2:].zfill(4)

                self._grid[gy][gx] = 0  # セル

                # cellから見た壁情報をgridに書き込む
                if bits[0] == "0":  # 左
                    self._grid[gy][gx-1] = 0
                if bits[1] == "0":  # 下
                    self._grid[gy+1][gx] = 0
                if bits[2] == "0":  # 右
                    self._grid[gy][gx+1] = 0
                if bits[3] == "0":  # 上
                    self._grid[gy-1][gx] = 0
                if info == 15:
                    self._grid[gy][gx] = 5

    def _find_path(self) -> None:
        """幅優先探索（BFS）を用いてスタートからゴールへの最短経路を探索します."""
        self._convert_hex_maze_to_grid()

        start = (self._entry[0] * 2 + 1, self._entry[1] * 2 + 1)
        goal = (self._exit[0] * 2 + 1, self._exit[1] * 2 + 1)

        sx, sy = start
        gx, gy = goal

        height = len(self._grid)
        width = len(self._grid[0])

        queue = deque([start])
        visited = {start}
        prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        # 進む経路を頭から取り出す
        while queue:
            x, y = queue.popleft()
            # ゴールにたどり着いたら終了
            if (x, y) == goal:
                break

            # 進むべき経路を後ろから予約する
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if self._grid[ny][nx] != 1 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        prev[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        # ゴールからスタートまでの経路座標をprevを手繰り寄せて取得する
        cur: tuple[int, int] | None = goal
        self._path = []
        while cur is not None:
            self._path.append(cur)
            cur = prev[cur]
        # 最後に逆転されることでスタートからゴールまでのPathが完成する
        self._path.reverse()

        self._grid[sy][sx] = 2
        self._grid[gy][gx] = 3
        self._path_to_way()

    def _path_to_way(self) -> None:
        """座標リスト形式の経路を、方角リスト（N, E, S, W）に変換します.

        Raises:
            ValueError: 隣接していないセルへの移動が検出された場合。
        """
        self._way = []

        # グリッド拡張されているため、2つ飛ばしで元のセルの動きを取得
        just_cell_path = self.path[::2]

        # zipは引数が取り出せない時に処理が終了する
        # 最後のマス（EXIT）だった時にそこから向かうルートがないため処理が終了する
        for (x1, y1), (x2, y2) in zip(just_cell_path, just_cell_path[1:]):
            dx = x2 - x1
            dy = y2 - y1

            if dx == 2 and dy == 0:
                self._way.append("E")
            elif dx == -2 and dy == 0:
                self._way.append("W")
            elif dx == 0 and dy == 2:
                self._way.append("S")
            elif dx == 0 and dy == -2:
                self._way.append("N")
            else:
                raise ValueError(f"Invalid move: {(x1, y1)} -> {(x2, y2)}")


if __name__ == "__main__":
    pass
