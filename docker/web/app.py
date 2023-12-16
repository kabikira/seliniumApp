from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mysql.connector
import os

# ヘッドレスモードでChromeを起動するためのオプション
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    # Seleniumでブラウザを操作
    print("ブラウザを起動中...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://google.com")

    # MySQLに接続
    print("データベースに接続中...")
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "mysql_pass"),
        database=os.getenv("DB_NAME", "web_logs")
    )
    cursor = conn.cursor()

    # ログを保存
    print("データベースにログを保存中...")
    query = "INSERT INTO logs (url) VALUES (%s)"
    cursor.execute(query, (driver.current_url,))
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
