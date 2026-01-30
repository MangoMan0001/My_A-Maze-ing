*This project has been created as part of the 42 curriculum by ayhirose rtsubuku.*

# A-Maze-ing

### Description
Pythonベースの迷路生成とゴール探索プログラム

共通目標
- PACMANで使用するMAPジェネレータを作成する
    - 設定ファイルを受け取り、迷路を生成する。
    - 最短経路探索アルゴリズムを実装する
- 迷路のVisualizerを作成する。
- プログラムの再利用化ができるようになる。

チーム目標
- メンバーやAIに依存せず、問題なくプロジェクトが進められる ”基本設計” が組めるようになる
- 今後の課題でも継続して実装する`Makefile`, `README`, `pyproject.toml`などの仕様を理解する。

ディレクトリ構成
```
.
├── Makefile
├── README.md
├── setup.cfg
├── .gitignore
│
├── config.txt                          # 迷路の設定ファイル(下記に書式説明)
├── requirements.txt                    # 依存ライブラリ（mlx, mypy, flake8等）
├── pyproject.toml                      # ビルド設定ファイル (setuptools)
├── mazegen-0.0.1-py3-none-any.whl      # 共有パッケージ (mazegen)
│
├── a_maze_ing.py                       # 全体の統括（エントリーポイント）
├── mazegen/                            # 【再利用可能な迷路生成パッケージ】
│   ├── __init__.py
│   └── generator.py                   # MazeGeneratorクラス
│
└── src/                                # 【迷路生成/探索以外の実装コード】
    ├── __init__.py
    ├── config_parser.py                # 設定ファイルの読み込み
    ├── visualizer_ascii.py             # 迷路のターミナル表示
    └── file_output.py                  # 16進数形式でのファイル書き出し担当
    └── user_input.py                   # ユーザー操作
```

### Instructions

プログラムは**Python 3.10以上**での実行が前提で作成されています。

1. **インストール**
```bash
make install
```
このコマンドを実行すると`.venv`という名前で仮想環境が構築され、`requirement.txt`に記述されたパッケージを`.venv`にインストールされます。

2. **プログラムの実行**
```bash
make run
```
このコマンドを実行すると`config.txt`を読み込み、迷路を生成して表示します。ユーザー操作も受け付ける状態になります。
```bash
./.venv/bin/python3 a_maze_ing.py config.txt
```
また、手動で実行することでファイル名を指定することも可能です。
```bash
sorce .venv/bin/activate
```
課題pdfに準拠する形で実行する場合は、事前に仮想環境を`activate`してください。 \
仮想環境から離脱する場合は`deactivate`を実行してください。

3. **その他の`Makefile`コマンド**
```bash
make lint
make lint-strict
```
静的解析: `flake8` と `mypy`を実行。 \
`-strict`でstrictモードで実行

```bash
make debug
```
デバッグモード: `pdb`を使用して実行。

```bash
make clean
```
クリーンアップ: キャッシュファイルの削除。 \
`fclean`で`.venv`と`maze.txt`も削除。


## Additional sections

### config.txt

```python
WIDTH=20                # Maze width (number of cells)
HEIGHT=15	            # Maze height
ENTRY=0,0	            # Entry coordinates (x,y)
EXIT=19,14	            # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt	# Output filename(.txt)
PERFECT=True	        # Is the maze perfect?
SEED=42			        # Maze seed
```

PERFECTが`False`だと正答のルートが複数ある迷路が生成される

### Algorithm
* **迷路生成:** [穴掘り方] \
理由: 穴掘り方は実装がシンプルで、3*3の広いエリアを生成するリスクがないため。

* **迷路探索:** [幅優先探索] \
理由: 幅優先探索 (BFS) は重みなしグラフにおける最短経路を保証するため。

### Reusable
`mazegen`パッケージは迷路生成ロジックとして分離しています。\
パッケージ管理: `pyproject.toml` \
インストール方法: `pip` \
詳細な使用方法は後述の**Package Usage**を参照

### Project management

**Team member**

ayhirose
- 基礎設計
- `MazeGenerator`の実装
- `file_output`の実装

rtsubuku
- `config_perser`の実装
- `visualizer`の実装
- `MazeGenerator.find_path`の実装
- `user_input`の実装


**Planning**
-  [x]  **Phase 1: 基盤作成**
    - [x] `config.txt`パーサー実装  1/20
    - [x] `MazeGenerator`クラス定義  1/20
- [x] **Phase 2: コアロジック**
    - [x]  `MazeGenerator`の実装 1/22
        - [x] 迷路生成アルゴリズムの実装 1/21
        - [x] PERFECTフラグでの作り分け 1/22
        - [x] 「42」パターンの埋め込み 1/21
    - [x] `MazeGenerator.find_path`の実装 1/24
        - [x] 最短経路探索の実装 1/21
- [x] **Phase 3: アプリケーション**
    - [x] `output_validator.py` をpass 1/24
        - [x] ファイル出力(16進数表記) 1/24
    - [x] `visualizer` の実装 1/24
        - [x] 迷路の可視化 1/21
        - [x] path経路の可視化 1/22
        - [x] ユーザー操作の実装 1/23 24
- [ ] **Phase 4: パッケージ化**
    - [x] flake8, mypyのPass
    - [x] `pyproject.toml`の作成
    - [x] `Makefile`の作成
    - [x] `README`の完成

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
ユーザー操作、visualizerのクラス化、find_path最適化、各々のファイルをテスト的にMazeGeneratorに組み込んだ \
致命的なバグは見られず

1/24 \
目標：output_fileの作成とvalidatorのPass、書式の統一 \
find_pathの最適化とgeneratorのデバッグが進み、output_fileがvalidatorの基準に見立った \
user_inputの最適化を行った

1/25 \
目標: Docstringの最適化、mypy, flake8のPass \
Docstringの大幅修正を行った。 \
書式がいくつかあること、それに準じたテスターがflake8やmypyに存在していることを学んだ

1/26 \
目標：パッケージ化、MakeFileとREADMEの最適化 \
パッケージ化に必要なpyproject.tomlについて書式と仕組みを理解した \
ある程度形になったのでrtsubuku君作テスターを通せれば一旦提出してみようかなと思う

1/27 \
目標：MazeGeneratorにセッターとゲッターを設ける

1/28 \
テスター導入

1/29 \
提出 -> Pass \
完


**Improvement / Eflection point**

【Improvement (良かった点)】

ayhirose
- 役割を迷路生成と迷路探索でキレイに分けれたこと、最初にある程度設計がまとめられたので実装のスケージュールやタスク管理がしやすかった。

rtsubuku

- 分業がしっかりとできて、自分のタスクがはっきりしていたこと

【Election point (反省点)】

ayhirose
- MazeVisuarizerのクラス設計を実装が進みながら構築したため、rtsubukuくんの作成したコードを書きかえる必要が出てしまっていた。初期の設計段階でMazeGeneratorだけでなくて、Visualizerもクラス化の必要性に気づくべきだった。しつこい要件に文句一つ言わずに書いてくれてありがとう！！

rtsubuku

- とにかく動かすことを目標にしてメソッドをベタ書きしてしまったので綺麗に書くことができず、後からクラスでまとめるときに苦労しました。自身のクラスに対する理解の浅さを痛感しました。また、Makefileや環境構築なども全部任せてしまったので、もう少し手伝える部分があったのではないかと反省しています。

**Tools**

- Discord
- GitHub


### Resources

AI (Gemini)
- 設計のテンプレート作成
- エラーログの解析
- Docstring作成

## 📦 Maze Generator Package Usage (パッケージの利用方法)

このプロジェクトは、迷路生成ロジックを再利用可能なPythonライブラリとして提供しています。
以下に、インストール方法と基本的な使い方を説明します。

### 1. インストール (Installation)
生成された `.whl` ファイルを使用してパッケージをインストールします。

```bash
pip install mazegen-0.0.1-py3-none-any.whl
```

### 2. 基本的な使い方 (Basic Usage)
example.
```python
from mazegen import MazeGenerator

# 設定をdict型で用意
conf ={WIDTH=20,
       HEIGHT=15,
       ENTRY=(0, 0),
       EXIT=(19, 14),
       OUTPUT_FILE=maze.txt,
       PERFECT=True,
       SEED=42}

# ジェネレータのインスタンス化
generator = MazeGenerator(conf)

# 迷路構造の生成
generator.generate()

print("迷路が正常に生成されました！")
```

### 3. パラメータの変更/取得 (Custom Parameters)
```python
generator.'setter' = 'value'

# SEEDを変更したい場合
generator.seed = 42

# PERFECTを取得したい場合
flag = generator.perfect

# 現在の設定を取得したい場合
generator.conf.report_status()
conf:str = generator.report()
```
各種パラメータには`setter`と`getter`が用意されています。


### 4. 迷路と解法へのアクセス (Accessing Maze and Path)
```python
# 迷路を取得したい場合 (16進数)
maze = generator.maze

# 迷路を取得したい場合 (2進数)
grid = generator.grid

# 最短経路を取得したい場合 (座標)
path = generator.path

# 迷路を取得したい場合 (方角)
way = generator.way
```
