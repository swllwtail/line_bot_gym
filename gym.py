import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

def crawl_gym ():

    # 設定要爬取的網址
    url = 'https://rent.pe.ntu.edu.tw'  # 替換成你想要爬取的網址

    # 發送 GET 請求
    response = requests.get(url)

    # 確認請求是否成功
    if response.status_code == 200:
        # 解析 HTML 內容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 獲取網頁標題
        #title = soup.title.string
        #print(f"網頁標題: {title}")

        # 獲取所有段落內容
        paragraphs = soup.find_all('span')
        for idx, paragraph in enumerate(paragraphs):
            if idx == 8:
                population = paragraph.get_text()
                return population
                #print(f"健身房現在人數: {paragraph.get_text()}")
            else:
                #print(f"無法訪問網址，狀態碼: {response.status_code}")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    message = TextSendMessage(text = event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

