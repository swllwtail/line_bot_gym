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

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_json()
    reply_token = body['events'][0]['replyToken']
    user_message = body['events'][0]['message']['text']

    if user_message.lower() == "健身房人數":
        reply_message(reply_token, f"目前健身房人數: {crawl_gym()} 人")

    return 'OK'

def reply_message(reply_token, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=data)

if __name__ == "__main__":
    app.run(port=5000)
