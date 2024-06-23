## Sliniumを使用してGoogleの検索結果数をMySQLに保存するアプリ
## 実行手順
プロジェクトのルートディレクトリに移動
```sh
cd seliniumApp
```

Dockerコンテナをビルドして起動
```sh
docker-compose up --build
```
## 結果の確認
下記コマンドでコンテナIDを確認して
```
docker ps
```
MySQLに接続して、ログが正しく保存されているか確認します。
```
docker exec -it <db_container_id> mysql -u root -p
```
```sql
USE web_logs;
SELECT * FROM logs;
```
