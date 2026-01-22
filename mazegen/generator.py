#!/usr/bin/env python3
import random
import sys
import ast
from pydantic import BaseModel, Field, model_validator, \
                     ValidationError, field_validator
from typing import Annotated, Any

PositiveInt = Annotated[int, Field(ge=0,
                                   description="正の整数型")]


class _MazeConfig(BaseModel):
    """
    MazeGeneratorクラス初期値検証クラス
    """
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
    entry: tuple[PositiveInt, PositiveInt] = Field(alias="ENTRY",
                                                   default=(0, 0),
                                                   description="迷路のスタート地点")
    exit: tuple[PositiveInt, PositiveInt] = Field(alias="EXIT",
                                                  default=(19, 14),
                                                  description="迷路のゴール地点")
    seed: int = Field(alias="SEED",
                      ge=0,
                      le=1000,
                      default=42,
                      description="迷路の乱数種")
    perfect: bool = Field(alias="PERFECT",
                          default=True,
                          description="PERFECTフラグ")

    @field_validator('entry', 'exit', mode='before')
    @classmethod
    def _rescue_invalid_values_tuple(cls, v: Any, info) -> Any:
        if isinstance(v, tuple):
            return v
        if isinstance(v, str):
            try:
                return ast.literal_eval(v)
            except Exception:
                return v
        return v

    @model_validator(mode="after")
    def _after_valid_mazeconfig(self) -> "_MazeConfig":
        """
        以下の項目を追加検証する

            ・entryがwidthとheightを超えていないか
            ・entryとgoalが重なってないか
        """
        w, h = self.width, self.height
        ex, ey = self.entry
        gx, gy = self.exit

        if w < ex or h < ey:
            raise ValueError(f"ENTRY {ex, ey} exceeds maze size {w, h}")
        if w < gx or h < gy:
            raise ValueError(f"ENTRY {gx, gy} exceeds maze size {w, h}")
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
            if name not in set_fields:
                print(f"{name.upper()} (Default): {value}")
            else:
                print(f"{name.upper()}: {value}")


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
            conf = _MazeConfig(**confdict)
            conf.report_status()
            self._maze = []
            self._path = []
            self._visited = []
            self._width = conf.width
            self._height = conf.height
            self._entry = conf.entry
            self._exit = conf.exit
            self._seed = conf.seed
            self._perfect = conf.perfect
        except ValidationError as e:
            print("Validation error:")
            for err in e.errors():
                location = err['loc'][0] if err['loc'] else "Model Rules"
                print(f"    - {location}: {err['msg']}")
                print(f"      input:({err['input']})")
            sys.exit(1)

    @property  # getter
    def maze(self) -> list:
        return self._maze

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value) -> None:
        if value < 0:
            raise ValueError("seed cannot be changed to a negative value.")
        print(f"Seed has been changed to {value}")

    def generate(self):
        seed = self._seed
        random.seed(seed) if seed > 0 else random.seed(42)
        self._init_maze()
        self._generate_maze(*self._entry)
        self._find_path()

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
        start_x = (self._width - len(ft[0])) // 2
        start_y = (self._height - len(ft)) // 2
        for y in range(len(ft)):
            for x in range(len(ft[0])):
                if ft[y][x]:
                    self._visited[start_y + y][start_x + x] = 1

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
        return

    def _find_path(self) -> None:
        """
        _find_path の Docstring
        """


if __name__ == "__main__":
    pass
