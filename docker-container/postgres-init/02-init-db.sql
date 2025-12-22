-- スキーマ作成
CREATE SCHEMA IF NOT EXISTS uwgen AUTHORIZATION uwgen;

-- pgcrypto拡張機能有効化
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- デフォルトスキーマ設定 
ALTER DATABASE uwgen_pg12 SET search_path TO uwgen, public;
