*This project has been created as part of the 42 curriculum by ayhirose rtsubuku.*

# A-Maze-ing

### Description
Pythonベースの迷路生成とゴール探索プログラム

共通目標
- PACMANで使用するMAPジェネレータを作成する
- 迷路探索アルゴリズムを実装する
- READMEと仲良くなる
- プログラムの再利用化ができるようになる。

個人目標
- メンバーやAIに依存せず、問題なくプロジェクトが進められる ”基本設計” が組めるようになる

ディレクトリ構成
```
.
├── Makefile
├── README.md
├── .gitignore
├── a_maze_ing.py          # 全体の統括（エントリーポイント）
├── config.txt
├── requirements.txt       # 依存ライブラリ（mlx, mypy, flake8等
├── mazegen/               # 【再利用可能なパッケージ】
│   ├── __init__.py
│   └── generator.py       # MazeGeneratorクラス（ロジック担当）
└── src/                   # 【補助コード】
    ├── __init__.py
    ├── config_parser.py   # 設定ファイルの読み込み担当
    ├── visualizer_ascii.py # ターミナル表示担当
    └── file_output.py     # 16進数形式でのファイル書き出し担当
```

### Instructions



## Additional sections

### config.txt

```python
WIDTH=20	# Maze width (number of cells)
HEIGHT=15	# Maze height
ENTRY=0,0	# Entry coordinates (x,y)
EXIT=19,14	# Exit coordinates (x,y)
OUTPUT_FILE=maze.txt	# Output filename(.txt)
PERFECT=True	# Is the maze perfect?
SEED=42			# Maze seed
```

PERFECTがTrueだと正答のルートが複数ある迷路が生成される

### Algorithm

### Reusable

### Project management

Team member

ayhirose

- 基礎設計
- `MazeGenerator`の実装

rtsubuku
- `config_perser`の実装
- `visualizer`の実装
- `MazeGenerator.find_path`の実装


Planning
-  [ ]  **Phase 1: 基盤作成**
    - [x] `config.txt`パーサー実装  1/20
    - [x] `MazeGenerator`クラス定義  1/20
- [ ] **Phase 2: コアロジック**
    - [ ]  `MazeGenerator`の実装
        - [x] 迷路生成アルゴリズムの実装 1/21
        - [x] PERFECTフラグでの作り分け 1/22
        - [x] 「42」パターンの埋め込み 1/21
        - [ ] PACMANのメソッド
    - [ ] `MazeGenerator.find_path`の実装
        - [x] 最短経路探索の実装 1/21
- [ ] **Phase 3: アプリケーション**
    - [ ] `output_validator.py` をpass
        - [ ] ファイル出力(16進数表記)
    - [ ] `visualizer` の実装
        - [x] 迷路の可視化 1/21
        - [x] path経路の可視化 1/22
        - [ ] ユーザー操作の実装
- [ ] **Phase 4: パッケージ化**
    - [ ] `setup.py`の作成

1/16 \
初日 \
課題理解と土台作り、実装機能の洗い出し

1/17 \
READMEのプレバージョン完成 \
PACMAN、mazegeneratorの解読

1/18 \
ヴィジュアライザー導入開始

1/19 \
ヴィジュアライザー作成

1/20 21 \
MazeGeneratorクラスの迷路出力が可能になった。 \
Visualizer,16進数のマップデータをASCIIでターミナルに出力できるようになった。 \
PERFECTフラグの実装とGOALを壁にしない仕組みが足りない。 \
config_perserで抜き取ったデータ型はMazeGeneratorクラスで扱ってるデータ型に変換が必要だとわかった。 \
STARTやGOALの位置、MAPSIZEのバリデーションはMazeGeneratorでやるべきかconfig_perserでやるべきか要検討。

1/22 \
目標：PERFECTフラグの実装とEXITを壁にしない仕組みの導入。config_perserでデータ型の変換と検証の導入。 \
config.txtのバリデーションをMazeGeneratorで前処理する形で実装 \
42にENTRYやEXITの座標が重複している場合の例外処理実装 \
PERFECTフラグ機能切り替え実装 \
Visualizerもクラス設計を事前にしておくべきだったと反省 \
そろそろパッケージ化に取り組み始めたい \
あと、課題要件との照らし合わせも改めて

1/23 \
目標：PACMANメソッド実装、visualizer、findpath最適化と組み込み、ユーザー操作実装 \


Improvement / Eflection point

Tools


### Resources

AI (Gemini)
- 設計のテンプレート作成
