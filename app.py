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

import json
import os


app = Flask(__name__)

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

from pprint import pprint

def loadJson(filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    data_file = os.path.join(basedir, filename)
    with open(data_file,"r") as f:
        result = json.load(f)
    return result

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
    text = event.message.text
    inputLIST = [text]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    
    # read in json files
    uniName = loadJson("school_name_dict.json") #DICT
    deptName = loadJson("dept_name_dict.json")
 
    #setup
    university = resultDICT['university'] #str
    department = resultDICT['department'] #str 
    
    # no university match
    if 'university' in resultDICT:
        university = resultDICT['university']
    else:
        response = "IOH中沒有你查找的學校喔"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = response))
        return
    
    #no department match 
    if 'department' in resultDICT:
        department = resultDICT['department']
    else:
        response = "IOH中沒有你查找的系喔"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = response))
        return
    
    # both uni and dept match
    inquiryDICT = {"university": "", "department": ""} 
    if 'university' in resultDICT:
        inquiryDICT['university'] = resultDICT['university'] 
        if 'department' in resultDICT: 
            inquiryDICT['department'] = resultDICT['department']
            #search
            query_machine = se.HippoChamber()
            df_vec = query_machine.vectorize(query_machine)
            queryLIST = list(inquiryDICT.values())
            for i in len(queryLIST):
                sim_sorted = query_machine.get_similar_articles(query = queryLIST[i])
                key_list = [k for k, v in sim_sorted if v > 0.0]
                if num != -1:
                    keys = set(key_list) & keys
                else:
                    keys = set(key_list)
                num = len(keys)
                if num <= 5:
                    result = list(keys)
                    for r in result:
                        content = query_machine.doc[r].replace("/", "")
                        print(content)
                        print()
                        print()
                    end = True
                if num == 0:
                    print("很抱歉查詢失敗")
                    end = True                
               
    #user didn't mention uni
    if resultDICT['university'] == "":
        response = "請告訴 hippo chamber，你要查找的大學喔"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = response))
        return
    
    #user didn't mention dept
    if resultDICT['department'] == "":
        response = "請告訴 hippo chamber，你要查找的學系喔"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = response))
        return
    

    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text=content))
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)