# Makefile
# SSGビルドタスク管理

# 変数定義
PYTHON := python3
BUILD_SCRIPT := generate.py
OUTPUT_DIR := public
PORT := 8000

.PHONY: all build serve dev clean help

# デフォルトターゲット
all: build

# サイト構築（build.pyの実行）
build:
	$(PYTHON) $(BUILD_SCRIPT)

# ローカルサーバー起動（publicディレクトリをルートとして配信）
serve:
	@echo "Starting server at http://localhost:$(PORT)"
	@cd $(OUTPUT_DIR) && $(PYTHON) -m http.server $(PORT)

# ローカル開発モードでビルド＋サーバー起動
dev:
	@echo "Building in LOCAL_DEV mode..."
	@LOCAL_DEV=true $(PYTHON) $(BUILD_SCRIPT) && \
	echo "Starting server at http://localhost:$(PORT)" && \
	cd $(OUTPUT_DIR) && $(PYTHON) -m http.server $(PORT)

# 生成物の削除
clean:
	rm -rf $(OUTPUT_DIR)

# ヘルプ表示
help:
	@echo "Usage:"
	@echo "  make build   - Generate the static site"
	@echo "  make serve   - Serve the site locally at port $(PORT)"
	@echo "  make dev     - Build in dev mode and serve"
	@echo "  make clean   - Remove the $(OUTPUT_DIR) directory"
