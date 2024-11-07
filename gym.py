import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

msg_list = ['gym','人數','健嗎','gym ','Gym ','Gym']
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


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #echo
    msg = event.message.text
    if (msg in msg_list):
        re = f"目前健身房人數: {crawl_gym ()} 人"
        message = TextSendMessage(text = re)
        line_bot_api.reply_message(event.reply_token,message)
    return
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
