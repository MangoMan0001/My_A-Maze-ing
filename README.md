*This project has been created as part of the 42 curriculum by ayhirose.*

# A-Maze-ing

### Description
Pythonベースの迷路生成とゴール探索プログラム

共通目標
- PACMANで使用するMAPジェネレータを作成する
- READMEと仲良くなる
- MLXと仲良くなる
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
    ├── visualizer_mlx.py  # GUI描画とユーザー入力監視（MLX）
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
OUTPUT_FILE=maze.txt	# Output filename
PERFECT=True	# Is the maze perfect?
SEED=42			# Maze seed
P_MODE=False	# is the PAC_MAN mode?
```

PERFECTがTrueだと正答のルートが複数ある迷路が生成される

### Algorithm

### Reusable

### Project management

Team member

ayhirose

- 設計
- `visualizer`の実装

rtsubuku
- `config.txt`パーサーの実装


Planning
-  [ ]  **Phase 1: 基盤作成**
    - [x] `config.txt`パーサー実装
    - [x] `MazeGenerator`クラス定義
- [ ] **Phase 2: コアロジック**
    - [ ] 迷路生成アルゴリズムの実装
    - [ ] PERFECTフラグでの作り分け
    - [ ] 「42」パターンの埋め込み
    - [x] 最短経路探索の実装
    - [ ] PACMANのメソッド
- [ ] **Phase 3: アプリケーション**
    - [ ] ファイル出力(16進数表記)
    - [ ] `output_validator.py` をpass
    - [ ] `visualizer` の実装
    - [ ] ユーザー操作の実装
- [ ] **Phase 4: パッケージ化**
    - [ ] `setup.py`の作成



Improvement / Eflection point

Tools


### Resources

AI (Gemini)
- 設計のテンプレート作成
