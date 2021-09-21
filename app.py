# -*- coding: utf-8 -*-

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('w477YzEf5ubS1SGrLu88dQvzRdR4HUgbjGvbFPxZ3xVVW0s/1ItqB5z2NaOXk2H8kaQybBx+ICHH8jIkWdCYBTBudh4/+1KzAuQRd6c9DOf/jO0/loUC2rgmAolT5UMx+y07nVc+veZLyWY/aZHpggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a126d182d8794e0cde2b203d4496a0ef')

line_bot_api.push_message('U27fc746a9ee5264743e7a594c165c2b0', TextSendMessage(text='hello my friend'))

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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8888))
    bot_info = line_bot_api.get_bot_info()
    print(bot_info.display_name)
    print(bot_info.user_id)
    print(bot_info.basic_id)
    print(bot_info.premium_id)
    print(bot_info.picture_url)
    print(bot_info.chat_mode)
    print(bot_info.mark_as_read_mode)
    app.run(host='0.0.0.0', port=port)
