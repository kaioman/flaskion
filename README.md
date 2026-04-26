# Flaskion - 統合型AI バックエンド APIサーバー

**Flaskion** は、**Gemini**、**ComfyUI** など複数のAIバックエンドに接続できるように設計された軽量かつ拡張可能なFlaskベースのAPIサーバーです。知的相互作用のための統一インターフェースを提供します。

## 目次

- [概要](#概要)
- [主な機能](#主な機能)
- [前提条件](#前提条件)
- [インストール](#インストール)
- [クイックスタート](#クイックスタート)
- [プロジェクト構成](#プロジェクト構成)
- [APIエンドポイント](#apiエンドポイント)
- [VSCodeによるDocker内のFlaskリモートデバッグ](#vscodeによるdocker内のflaskリモートデバッグ)
- [Alembicを使用したデータベースマイグレーション](#alembicを使用したデータベースマイグレーション)
- [テスト](#テスト)
- [トラブルシューティング](#トラブルシューティング)
- [コントリビューション](#コントリビューション)
- [ライセンス](#ライセンス)

## 概要

Flaskionは、複数のAIサービス統合の複雑さを抽象化する一元化されたAPIゲートウェイとして機能します。以下を提供します：

- **統一REST API** - テキスト生成、画像生成、画像分析用
- **マルチバックエンド対応** - Gemini、ComfyUI など
- **データベース永続化** - PostgreSQLとSQLAlchemy
- **認証とセキュリティ** - JWT と暗号化認証情報
- **拡張可能なアーキテクチャ** - 新しいサービスと機能を追加可能
- **Docker-first デプロイメント** - 開発環境と本番環境のプロファイル

## 主な機能

- ✅ 複数のAIバックエンド統合（Gemini、ComfyUI）
- ✅ テキストと画像操作用の統一REST API
- ✅ Alembic マイグレーション対応のPostgreSQLデータベース
- ✅ VSCode + debugpy によるリモートデバッグサポート
- ✅ ローカル開発用 Docker Compose
- ✅ Fernet暗号化による認証情報管理
- ✅ 包括的なロギングとエラーハンドリング
- ✅ Marshmallowスキーマによるリクエスト/レスポンス検証
- ✅ RESTful サービスアーキテクチャ

## 前提条件

開始する前に、以下をインストールしていることを確認してください：

- **Python** 3.11 以上
- **Docker** 20.10+ および **Docker Compose** 1.29+
- **PostgreSQL** 12+ （またはDocker版を使用）
- **Git** バージョン管理用

## インストール

### 1. リポジトリをクローン

```bash
git clone https://github.com/kaioman/flaskion.git
cd flaskion
```

### 2. 仮想環境のセットアップ

#### Windows の場合

```bash
python -m venv env
env\Scripts\activate
```

#### macOS/Linux の場合

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Python依存関係のインストール

```bash
pip install -r requirements.txt
pip install debugpy  # 開発/デバッグ用
```

### 4. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成します：

```bash
# データベース
DATABASE_URL=postgresql://user:password@localhost:5432/flaskion_db

# AIバックエンド
GEMINI_API_KEY=your_gemini_api_key
COMFYUI_URL=http://localhost:8188

# Flask
FLASK_APP=server.py
FLASK_ENV=development  # または production
SECRET_KEY=your_secret_key
FERNET_KEY=your_fernet_key  # gen_fernet_key.py を使用

# デバッグ（開発環境のみ）
DEBUGPY=false
DEBUG_PORT=5150
```

### 5. 暗号化キーの生成（必要な場合）

認証情報の暗号化用：

```bash
python gen_fernet_key.py
python gen_secret_key.py
```

## クイックスタート

### オプション A: Docker Compose （推奨）

```bash
# コンテナをビルドしスタート
docker-compose up -d

# データベースを初期化（初回のみ）
docker exec -it flaskion bash
source env/bin/activate
alembic upgrade head
exit

# Flask API は http://localhost:5100 で利用可能
```

### オプション B: ローカル開発

```bash
# PostgreSQL がローカルで実行していることを確認
# .env の DATABASE_URL をローカルインスタンスに指定

# 仮想環境を有効化
env\Scripts\activate  # Windows
# または
source env/bin/activate  # macOS/Linux

# マイグレーションを実行
alembic upgrade head

# Flask開発サーバーを起動
python server.py
# または
flask run --host=0.0.0.0 --port=5100

# API は http://localhost:5100 で利用可能
```

## プロジェクト構成

```bash
flaskion/
├── app/
│   ├── __init__.py              ← Flask アプリケーションファクトリ
│   ├── main.py                  ← メインアプリケーションセットアップ
│   ├── api/
│   │   └── v1/                  ← API v1 エンドポイント
│   │       ├── auth.py          ← 認証エンドポイント
│   │       ├── text_gen.py      ← テキスト生成エンドポイント
│   │       ├── image_gen.py     ← 画像生成エンドポイント
│   │       ├── image_edit.py    ← 画像編集エンドポイント
│   │       └── image_analyze.py ← 画像分析エンドポイント
│   ├── services/
│   │   ├── auth_service.py      ← 認証ビジネスロジック
│   │   ├── text_gen_service.py  ← テキスト生成ロジック
│   │   ├── image_gen_service.py ← 画像生成ロジック
│   │   ├── image_edit_service.py← 画像編集ロジック
│   │   └── image_analyze_service.py ← 画像分析ロジック
│   ├── models/
│   │   ├── user.py              ← SQLAlchemy ユーザーモデル
│   │   ├── request_log.py       ← リクエストログモデル
│   │   └── ...                  ← その他のデータベースモデル
│   ├── schemas/
│   │   ├── auth.py              ← 認証リクエスト/レスポンススキーマ
│   │   ├── text_gen.py          ← テキスト生成スキーマ
│   │   ├── image.py             ← 画像操作スキーマ
│   │   └── ...                  ← その他の検証スキーマ
│   ├── core/
│   │   ├── security.py          ← パスワードハッシング、JWTトークン
│   │   ├── config.py            ← 設定管理
│   │   ├── constants.py         ← アプリケーション定数
│   │   └── exceptions.py        ← カスタム例外
│   ├── db/
│   │   ├── session.py           ← SQLAlchemy セッション管理
│   │   └── base.py              ← ベースモデル設定
│   ├── routes/
│   │   ├── auth.py              ← 認証ルートブループリント
│   │   ├── text_gen.py          ← テキスト生成ルート
│   │   ├── image.py             ← 画像操作ルート
│   │   └── ...                  ← その他のルートブループリント
│   ├── static/                  ← 静的ファイル（CSS、JS、画像）
│   ├── templates/               ← HTMLテンプレート（テンプレート使用時）
│   ├── test_api_*.py            ← APIエンドポイント用テストファイル
│   └── configs/
│       ├── logger.json          ← ロギング設定
│       └── comfyui/             ← ComfyUI設定
├── alembic/
│   ├── env.py                   ← Alembic環境設定
│   ├── script.py.mako           ← マイグレーションスクリプトテンプレート
│   ├── versions/                ← データベースマイグレーションスクリプト
│   └── README                   ← Alembicドキュメント
├── docker-container/
│   ├── Dockerfile               ← コンテナイメージ定義
│   ├── docker-compose.yml       ← 本番環境構成
│   ├── docker-compose.override.yml ← 開発環境構成
│   ├── exec-py311_flask.sh      ← Flask実行スクリプト
│   └── exec-pg12_uwgen.sh       ← PostgreSQL実行スクリプト
├── credentials/
│   └── gen-lang-client-*.json   ← Google Cloud認証情報
├── server.py                    ← アプリケーションエントリーポイント
├── requirements.txt             ← Python依存関係
├── alembic.ini                  ← Alembic設定
├── gen_fernet_key.py            ← Fernetキー生成ユーティリティ
├── gen_secret_key.py            ← シークレットキー生成ユーティリティ
└── README.md                    ← このファイル（日本語）
```

## APIエンドポイント

### テキスト生成

- `POST /api/v1/text/generate` - AIバックエンドを使用してテキストを生成
- `GET /api/v1/text/models` - 利用可能なテキスト生成モデルをリスト

### 画像生成

- `POST /api/v1/image/generate` - テキストから画像を生成
- `POST /api/v1/image/generate-comfyui` - ComfyUIを使用して生成
- `GET /api/v1/image/models` - 利用可能な画像生成モデルをリスト

### 画像編集

- `POST /api/v1/image/edit` - 既存の画像を編集
- `POST /api/v1/image/upscale` - 画像解像度をアップスケール

### 画像分析

- `POST /api/v1/image/analyze` - 画像内容を分析
- `POST /api/v1/image/describe` - 画像の説明を生成

### 認証

- `POST /api/v1/auth/signup` - 新規ユーザーを登録
- `POST /api/v1/auth/signin` - ユーザーをログイン
- `POST /api/v1/auth/logout` - ユーザーをログアウト
- `POST /api/v1/auth/refresh` - JWTトークンをリフレッシュ

## VSCodeによるDocker内のFlaskリモートデバッグ

このプロジェクトは、**VSCode** と **debugpy** を使用してDocker内で実行されているFlaskアプリケーションのリモートデバッグをサポートしています。
デバッガーは **開発環境のみ** で有効です。

### 1. コンテナに `debugpy` をインストール

リモートコンテナに入り、仮想環境を有効化します：

```bash
docker exec -it <container_name> bash
source env/bin/activate
pip install debugpy
```

これにより、コンテナ内のFlaskプロセスがdebugpyで起動できます。

### 2. ホストに `debugpy` をインストール（開発環境のみ）

ソースコードが `debugpy` をインポートするため、ホスト環境にもパッケージが必要です。

ホストの仮想環境を有効化してインストール：

```bash
env\Scripts\activate  # Windows
# または
source env/bin/activate  # macOS/Linux

pip install debugpy
```

### 3. デバッガーポートを公開

`docker-compose.override.yml`（開発環境のみ）:

```yaml
services:
  flaskion:
    ports:
      - "5100:5100" # Flask
      - "5150:5150" # デバッグ用
    environment:
      - DEBUGPY=true
      - DEBUG_PORT=5150 # デバッガーポート
      - PYDEVD_DISABLE_FILE_VALIDATION=1
    entrypoint: [
      "/var/docker-flask/flaskion/env/bin/python", 
      "-Xfrozen_modules=off", 
      "-m", "flask",
    ]
    command: [
      "run",
      "--host=0.0.0.0",
      "--port=5100"
    ]
```

### 4. `server.py` で `debugpy` を有効化

エントリーポイント（`server.py`）の上部に以下を追加：

```python
# debugpy
import os

# デバッグモード確認
if os.getenv("DEBUGPY", "false").lower() == "true":
    # 重複リッスンを防止
    if not os.getenv("DEBUGPY_STARTED"):
        os.environ["DEBUGPY_STARTED"] = "true"
        import debugpy
        
        # デバッグポートを取得
        debug_port = int(os.getenv("DEBUG_PORT", "5150"))
        print(f"🚀[debugpy] ポート {debug_port} でリスナーを開く準備中")
        # デバッグポートでリッスン
        debugpy.listen(("0.0.0.0", debug_port))
        print(f"✅[debugpy] クライアント接続完了。実行を継続します。")
```

### 5. VSCode で `launch.json` を設定

最後に、VSCodeをDocker内で実行されているFlaskプロセスに接続するように設定します。
`.vscode/launch.json` に以下を追加：

```jsonc
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "debugpy",
            "request": "attach",
            "name": "Attach to Flask (Docker)",
            "connect": {
                "host": "localhost",
                "port": 5150
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/flaskion",
                    "remoteRoot": "/var/docker-flask/flaskion"
                }
            ]
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Launch Chrome for localhost",
            "url": "http://localhost:5100",
            "webRoot": "${workspaceFolder}"
        }
    ],
    "compounds": [
        {
            "name": "Debug Flask + Chrome",
            "configurations": [
                "Attach to Flask (Docker)",
                "Launch Chrome for localhost"
            ]
        }
    ]
}
```

この設定により、VSCodeデバッガーをDocker内のFlaskアプリケーションに接続し、
同時にフロントエンドデバッグ用にChromeを起動できます。

### 6. VSCodeをFlaskプロセスに接続

debugpyが有効で、ポートが公開されている状態でコンテナが実行中の場合：

1. VSCodeで **Run and Debug** パネルを開く（`Ctrl+Shift+D`）
2. ドロップダウンから **Attach to Flask (Docker)** を選択（またはバックエンドとフロントエンド両方をデバッグする場合は **Debug Flask + Chrome**）
3. **Start Debugging** （F5）を押す
4. VSCodeがポート `5150` 経由でDocker内のFlaskプロセスに接続
5. Pythonソースファイルにブレークポイントを設定。Flaskアプリケーションがそれらの行を実行すると、VSCodeが実行を一時停止し、変数、スタックトレース等を検査できます
6. デバッグを停止するには、VSCode内でセッションを停止するだけです。Flaskアプリケーションはコンテナ内で実行され続けます

> 💡 **ヒント**：バックエンドとフロントエンド両方をデバッグしたい場合は、複合構成 **Debug Flask + Chrome** を選択してください。これによりFlaskプロセスに接続し、同時に `http://localhost:5100` を指すChromeを起動します。

## Alembicを使用したデータベースマイグレーション

Flaskionは **Alembic** を使用して、データベーススキーママイグレーションを一貫性のある再現可能な方法で管理します。
このセクションでは、Docker ベースの開発環境内でAlembicをインストール、初期化、実行する方法を説明します。

### 1. Alembicをインストール（コンテナ内）

Flaskionコンテナに入り、仮想環境にAlembicをインストール：

```bash
docker exec -it <container_name> bash
source env/bin/activate
pip install alembic
```

requirements ファイルを使用している場合は、それも更新します：

```bash
pip freeze > requirements.txt
```

### 2. Alembicを初期化

コンテナ内でAlembicを初期化：

```bash
alembic init alembic
```

これにより以下を含む `alembic/` ディレクトリが作成されます：

- `env.py` — Alembic環境設定
- `script.py.mako` — マイグレーションスクリプトテンプレート
- `versions/` — マイグレーションファイルが保存される場所

### 3. Alembicを設定（`alembic.ini` と `env.py`）

`alembic.ini` を更新してデータベースURLを指定します。
Flaskionが環境変数からDB URLをロードする場合は、以下を設定：

```ini
sqlalchemy.url = ${DATABASE_URL}
```

その後、`alembic/env.py` を修正してアプリケーションからSQLAlchemy `Base` をロード：

```python
from app.db import Base  # インポートパスを調整してください
target_metadata = Base.metadata
```

これにより、Alembicはモデルに基づいてマイグレーションを自動生成できます。

### 4. マイグレーションを作成

モデル変更に基づいてマイグレーションを生成：

```bash
alembic revision --autogenerate -m "変更内容を説明"
```

Alembicは `alembic/versions/` の下に新しいファイルを作成します。
生成されたマイグレーションスクリプトの正確性を確認してください。

### 5. マイグレーションを適用

コンテナ内でマイグレーションを実行：

```bash
alembic upgrade head
```

ダウングレードの場合：

```bash
alembic downgrade -1
```

### 6. Docker ComposeでAlembicを実行

コンテナ起動時にAlembicが自動的に実行されるようにしたい場合（オプション）、
`docker-compose.override.yml` にコマンドを追加：

```yaml
command: >
  bash -c "
    alembic upgrade head &&
    flask run --host=0.0.0.0 --port=5100
  "
```

これにより、開発環境でデータベーススキーマが常に最新の状態を保ちます。

## テスト

含まれるテストファイルを実行してAPIエンドポイントを検証：

```bash
# テキスト生成APIテスト
python -m pytest app/test_api_text_gen.py -v

# 画像生成APIテスト
python -m pytest app/test_api_image_gen.py -v

# ComfyUIによる画像生成APIテスト
python -m pytest app/test_api_image_gen_comfyui.py -v

# 画像編集APIテスト
python -m pytest app/test_api_image_edit.py -v

# 画像分析APIテスト
python -m pytest app/test_api_image_analyze.py -v
```

## トラブルシューティング

### 問題: DockerでFlask アプリが起動しない

**解決策:**

- `docker-compose.override.yml` が正しいパスを持っていることを確認
- 環境変数が適切に設定されていることを確認
- PostgreSQLコンテナが実行中か確認: `docker ps`

### 問題: データベース接続エラー

**解決策:**

- `.env` の DATABASE_URL が正しいことを確認
- PostgreSQLコンテナログを確認: `docker logs postgres`
- データベースが存在し、マイグレーションが実行されていることを確認

### 問題: debugpy接続が失敗

**解決策:**

- docker-compose でポート 5150 が公開されていることを確認
- 環境変数で DEBUGPY=true が設定されていることを確認
- VSCode launch.json の pathMappings が正しいことを確認

### 問題: モジュール欠落エラー

**解決策:**

```bash
pip install -r requirements.txt
```

### 問題: Fernetまたはシークレットキーエラー

**解決策:**

```bash
python gen_fernet_key.py
python gen_secret_key.py
# 生成されたキーで .env を更新
```

## コントリビューション

コントリビューションを歓迎します。以下のガイドラインに従ってください：

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。

## サポート

問題、質問、提案については、GitHubでissueを開くか、メンテナーに連絡してください。

---

**最終更新**: 2026-04-26
