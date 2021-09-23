#!/usr/bin/env python3
# -*- coding:utf-8 -*-

LINE_ACCESS_TOKEN   = "tYSPdyTRv4Y2SOM8pNrlx5B8wckzD/XnICBhr9YCOtqgc38cbSY79IZZG6tXLA9sweiQPr3j8WX9zYLvFBwxUw2um2G/BDVViOAGSETqYAIPLFiTVoGE9qHj37YRSHOLbRgvM+vnC+wRfiatoPhmwAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "862e704472f1a37fe1e7f006b9563fac"

from flask import Flask, request, abort


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from IOHbot import runLoki

from latent_search_engine import se

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

from pprint import pprint


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    msg = request.get_json()
    # pprint(msg)
    text = msg['events'][0]['message']['text']


    app.logger.info("Request body: " + body)
    # inputLIST = [text]
    # filterLIST = []
    # resultDICT = runLoki(inputLIST, filterLIST)
    # print("Result => {}".format(resultDICT))

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    # read in message
    text=event.message.text
    print(text)
    inputLIST = [text]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    txt = "Result => {}".format(resultDICT)
    print(txt)
    
    # search 
    #query_machine = se.HippoChamber()
    #df_vec = query_machine.vectorize(query_machine)
    #sim_sorted = query_machine.get_similar_articles(query = "醫生")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt))
    


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)