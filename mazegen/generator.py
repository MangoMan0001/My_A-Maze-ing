#!/usr/bin/env python3
import random
import sys
import ast
from pathlib import Path
from pydantic import BaseModel, Field, model_validator, \
                     field_validator, ValidationError
from typing import Annotated, Any
from collections import deque

PositiveInt = Annotated[int, Field(ge=0,
                                   description="正の整数型")]


class MazeConfig(BaseModel):
    """
    MazeGeneratorクラス初期値検証クラス
    """
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
    def _validate_file_nama(cls, v: Any) -> Any:
        """
        以下の追加検証/修正を行う
            ・'.txt'がなければ追加する
            ・同名のディレクトリが存在するか
            ・open()が可能か
        """

        if v.suffix != '.tst':
            v.with_suffix('.txt')

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
        if isinstance(v, tuple):
            return v
        if isinstance(v, str):
            try:
                return ast.literal_eval(v)
            except Exception:
                return v
        return v

    @model_validator(mode="after")
    def _after_valid_mazeconfig(self) -> "MazeConfig":
        """
        以下の項目を追加検証する

            ・entryがwidthとheightを超えていないか
            ・entryとgoalが重なってないか
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

    def report_status(self) -> None:
        """
        MazeGeneratorの現在の設定を出力する
        """

        print("===Current settings===")

        all_fields = self.model_fields.keys()
        set_fields = self.model_fields_set

        for name in all_fields:
            value = getattr(self, name)
            if name in set_fields:
                print(f"{name.upper()}: {value}")
            else:
                print(f"{name.upper()} (Default): {value}")


class MazeGenerator:
    """
    conf
    creaat maze
    """

    def __init__(self, confdict: dict = {}):
        """
        initiialize
        """

        try:
            if not confdict:
                confdict = {}
            self._conf = MazeConfig(**confdict)

            self._maze = []
            self._path = []
            self._way = []
            self._grid = []
            self._visited = []

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

    @property  # getter
    def conf(self) -> MazeConfig:
        return self._conf

    @property  # getter
    def maze(self) -> list:
        return self._maze

    @property  # getter
    def path(self) -> list:
        return self._path

    @property  # getter
    def way(self) -> list:
        return self._way

    @property  # getter
    def grid(self) -> list:
        return self._grid

    @property  # getter
    def width(self) -> int:
        return self._width

    @property  # getter
    def height(self) -> int:
        return self._height

    @property  # getter
    def entry(self) -> tuple:
        return self._entry

    @property  # getter
    def exit(self) -> tuple:
        return self._exit

    @property  # getter
    def output_file(self) -> Path:
        return self._output_file

    @property  # getter
    def seed(self) -> int:
        return self._seed

    @property  # getter
    def perfect(self) -> bool:
        return self._perfect

    @seed.setter  # setter
    def seed(self, value) -> None:
        if value < 0:
            raise ValueError("SEED cannot be changed to a negative value.")
        self._seed = value
        self._conf.seed = value
        print(f"SEED has been changed to {value}")

    @perfect.setter  # setter
    def perfect(self, value) -> None:
        self._perfect = value
        self._conf.perfect = value
        print(f"PEFECT has been changed to {value}")

    def generate(self):
        seed = self._seed
        random.seed(seed) if seed > 0 else random.seed(42)
        self._init_maze()
        self._generate_maze(*self._entry)
        if not self._perfect:
            self._break_the_wall()
        self._find_path()
        self.conf.report_status()

    def _init_maze(self) -> None:
        """
        _init_maze の Docstring
        """
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
                    if ft[y][x]:
                        self._visited[start_y + y][start_x + x] = 1
            self._validate_maze()
            return
        print("MazeGenerator Warning: maze is too small to add '42' in it")

    def _validate_maze(self) -> None:
        """
        42内にENTRYやEXITが含まれていないかを検証する
        """
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
        """
        _generate_maze の Docstring
        """
        if self._visited[y][x] == 1:
            return
        # (x軸移動, y軸移動, 自身から見た破壊すべき壁ビット, 移動先から見た破壊すべき壁ビット)
        wasd = [(-1, 0, 8, 2, 'W'), (0, -1, 1, 4, 'S'),
                (1, 0, 2, 8, 'E'), (0, 1, 4, 1, 'N')]
        random.shuffle(wasd)
        self._visited[y][x] = 1
        for d in wasd:
            nx = x + d[0]  # .次に進むx座標 next_x
            ny = y + d[1]  # .次に進むy座標 next_y
            mw = d[2]  # .自分から見た壁ビット my_wall
            yw = d[3]  # .相手から見た壁ビット your_wall
            if not (0 <= nx < self._width and 0 <= ny < self._height):
                continue
            if self._visited[ny][nx] == 0:
                self._maze[y][x] -= mw
                self._maze[ny][nx] -= yw
                self._generate_maze(nx, ny)

    def _break_the_wall(self) -> None:
        """
        3つ壁があるマスの壁をランダムに1枚破壊する
        """
        # (x軸移動, y軸移動, 自身から見た破壊すべき壁ビット, 移動先から見た破壊すべき壁ビット)
        wasd = [(-1, 0, 8, 2, 'W'), (0, -1, 1, 4, 'S'),
                (1, 0, 2, 8, 'E'), (0, 1, 4, 1, 'N')]
        for y, line in enumerate(self._maze):
            for x, cell in enumerate(line):
                if cell in (14, 13, 11, 7):
                    random.shuffle(wasd)
                    for d in wasd:
                        nx = x + d[0]  # .破壊先のx座標 next_x
                        ny = y + d[1]  # .破壊先のy座標 next_y
                        mw = d[2]  # .自分から見た壁ビット my_wall
                        yw = d[3]  # .相手から見た壁ビット your_wall
                        if not (0 <= nx < self._width and
                                0 <= ny < self._height):
                            continue
                        if self._maze[ny][nx] == 15:
                            continue
                        if (x, y) in (self._entry, self._exit):
                            continue
                        if cell & mw:
                            cell -= mw
                            self._maze[ny][nx] -= yw
                            break

    def _convert_hex_maze_to_grid(self) -> None:
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

    def _find_path(self):
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

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if self._grid[ny][nx] != 1 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        prev[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        cur = goal
        self._path = []
        while cur is not None:
            self._path.append(cur)
            cur = prev[cur]
        self._path.reverse()

        self._grid[sy][sx] = 2
        self._grid[gy][gx] = 3
        self._path_to_way()

    def _path_to_way(self):
        self._way = []
        for (x1, y1), (x2, y2) in zip(self._path, self._path[1:]):
            dx = x2 - x1
            dy = y2 - y1

            if dx == 1 and dy == 0:
                self._way.append("E")
            elif dx == -1 and dy == 0:
                self._way.append("W")
            elif dx == 0 and dy == 1:
                self._way.append("S")
            elif dx == 0 and dy == -1:
                self._way.append("N")
            else:
                raise ValueError(f"Invalid move: {(x1, y1)} -> {(x2, y2)}")
        print(self._way)


if __name__ == "__main__":
    pass
