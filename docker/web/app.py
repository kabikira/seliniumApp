from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# ヘッドレスモードでChromeを起動するためのオプション
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 検索するキーワード
search_query = "Python"

try:
    # Seleniumでブラウザを操作
    print("ブラウザを起動中...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.google.com/search?q={search_query}")

    # 検索結果のヒット数を取得
    print("検索結果を取得中...")
    try:
        results_stats = driver.find_element(By.ID, "result-stats").text
    except NoSuchElementException:
        results_stats = "検索結果なし"
    print(f"検索結果: {results_stats}")

    # MySQLに接続
    print("データベースに接続中...")
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "mysql_pass"),
        database=os.getenv("DB_NAME", "web_logs"),
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    # ログを保存
    print("データベースにログを保存中...")
    query = "INSERT INTO logs (url, result) VALUES (%s, %s)"
    cursor.execute(query, (driver.current_url, results_stats))
    conn.commit()
    print("ログが保存されました。")

except mysql.connector.Error as e:
    print(f"データベースエラー: {e}")
except Exception as e:
    print(f"一般的なエラー: {e}")
finally:
    # 接続を閉じる
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'conn' in locals() and conn is not None:
        conn.close()
    if driver is not None:
        driver.quit()
        print("ブラウザを閉じました。")
