#!/usr/bin/env python3
import random
import sys
import ast
from pydantic import BaseModel, Field, model_validator, \
                     ValidationError, field_validator
from typing import Annotated, Any
from src import visualize_ascii
from collections import deque


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
            if not confdict:
                confdict = {}
            self.conf = _MazeConfig(**confdict)
            self._maze = []
            self._path = []
            self._visited = []
            self._width = self.conf.width
            self._height = self.conf.height
            self._entry = self.conf.entry
            self._exit = self.conf.exit
            self._seed = self.conf.seed
            self._perfect = self.conf.perfect
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
        self.conf.report_status()
        if not self._perfect:
            self._break_the_wall()

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
        visualize_ascii(self._maze)
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

    def _find_path(self) -> None:
        """
        _find_path の Docstring
        """
        # converted_maze = visualize_ascii(self.maze)
        # height = len(converted_maze)
        # width = len(converted_maze[0])

        # for y in range(height):
        #     for x in range(width):
        #         if converted_maze[y][x] == 2:
        #             self._entry = (x, y)
        #         elif converted_maze[y][x] == 3:
        #             self._goal = (x, y)

        # print("Goal:", self._exit)

        # queue = deque()
        # queue.append(self._entry)
        # visited = set()
        # visited.add(self._entry)

        # counter = 0
        # prev = {}
        # prev[self._entry] = None
        # while queue:
        #     x, y = queue.popleft()
        #     if (x, y) == self._exit:
        #         print(counter, "now:", x, y, "Here is the goal!!")
        #         break
        #     else:
        #         print(counter, "now:", x, y)

        #     for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        #         nx = x + dx
        #         ny = y + dy
        #         if 0 <= nx < width and 0 <= ny < height:
        #             if converted_maze[ny][nx] != 1 and (nx, ny) not in visited:
        #                 visited.add((nx, ny))
        #                 queue.append((nx, ny))
        #                 prev[(nx, ny)] = (x, y)
        #     counter += 1

        # path = []
        # cur = self._exit

        # while cur is not None:
        #     path.append(cur)
        #     cur = prev[cur]

        # path.reverse()
        # print(path)
        # print("shortest way", len(path))

        # for (x, y) in path:
        #     if converted_maze[y][x] == 0:
        #         converted_maze[y][x] = 4

        # draw_ascii_maze(converted_maze)


if __name__ == "__main__":
    pass
