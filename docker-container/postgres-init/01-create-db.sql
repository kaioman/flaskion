-- uwgenデータベース作成
CREATE DATABASE uwgen_pg12;

-- ユーザー作成
CREATE USER uwgen WITH PASSWORD 'uwgen';
GRANT ALL PRIVILEGES ON DATABASE uwgen_pg12 TO uwgen;
