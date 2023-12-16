FROM python:3.9

WORKDIR /app

# Chromeとその依存関係をインストール
RUN apt-get update \
    && apt-get install -y wget gnupg2 software-properties-common \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# ChromeDriverのインストール（指定されたバージョン）
RUN apt-get install -yqq unzip \
    && wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.71/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver

# Pythonの依存関係をインストール
COPY web/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY web/ .

# アプリケーションの実行
CMD ["python", "./app.py"]
