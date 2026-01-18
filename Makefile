# ==========================================
#  A-Maze-ing Project Makefile
# ==========================================

# 実行するPythonコマンド
PYTHON_EXEC ?= python3

# バージョンチェック用スクリプト (ワンライナー)
# 3.10未満ならエラー(1)を返す
CHECK_VERSION = $(PYTHON_EXEC) -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"

# プロジェクト名とメインスクリプト
NAME        = a_maze_ing
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt

# 仮想環境の設定
VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip
PY_VERSION  = python3

# 依存パッケージ
REQUIREMENTS = requirements.txt

# ==========================================
#  Rules
# ==========================================

.PHONY: all install run debug clean lint lint-strict build re

all: install

# ------------------------------------------
#  Environment Setup
# ------------------------------------------
install: ## 仮想環境を作成し、依存関係をインストールする
	@echo "🔍 Checking Python version..."
	@if ! $(CHECK_VERSION); then \
		echo "Error: Python 3.10 or higher is required."; \
		echo "   Your $(PYTHON_EXEC) is version:"; \
		$(PYTHON_EXEC) --version; \
		echo "   Try setting PYTHON_EXEC (e.g., 'make install PYTHON_EXEC=python3.11')"; \
		exit 1; \
	fi
	@echo "Python version is OK."
	@echo "Creating virtual environment..."
	$(PY_VERSION) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	# もしMLXのwheelファイルを手動で入れる場合は以下をアンコメントしてください
	# $(PIP) install ./mlx-2.2-py3-ubuntu-any.whl --force-reinstall
	@echo "Setup complete! Run 'make run' to start."

# ------------------------------------------
#  Execution
# ------------------------------------------
run: ## メインプログラムを実行
	@echo "🚀 Running $(NAME)..."
	@if [ ! -d "$(VENV)" ]; then echo "❌ Venv not found. Run 'make install' first."; exit 1; fi
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

debug: ## pdbデバッガを使って実行
	@echo "🐞 Debugging $(NAME)..."
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

# ------------------------------------------
#  Quality Control
# ------------------------------------------
lint: ## Flake8とMypyによる静的解析を実行
	@echo "🔍 Running Linter (Standard)..."
	@if [ ! -d "$(VENV)" ]; then echo "❌ Venv not found. Run 'make install' first."; exit 1; fi
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: ## より厳しいMypyチェックを実行
	@echo "🧐 Running Linter (Strict)..."
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

# ------------------------------------------
#  Packaging
# ------------------------------------------
build: ## mazegenパッケージをビルドして .whl を作成
	@echo "📦 Building mazegen package..."
	$(PIP) install build
	$(PYTHON) -m build
	@echo "✅ Build complete. Check 'dist/' directory."

# ------------------------------------------
#  Cleanup
# ------------------------------------------
clean: ## 一時ファイルやキャッシュを削除
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf **/__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	@echo "✨ Clean complete."

re: clean all
