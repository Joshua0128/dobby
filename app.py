# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify

from line_sdk import Linebot

from IOHbot import runLoki

LINE_ACCESS_TOKEN   = "w477YzEf5ubS1SGrLu88dQvzRdR4HUgbjGvbFPxZ3xVVW0s/1ItqB5z2NaOXk2H8kaQybBx+ICHH8jIkWdCYBTBudh4/+1KzAuQRd6c9DOf/jO0/loUC2rgmAolT5UMx+y07nVc+veZLyWY/aZHpggdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "a126d182d8794e0cde2b203d4496a0ef"

app = Flask(__name__)

@app.route("/callback", methods=["GET", "POST"])
def webhook():
    #GET
    if request.method == "GET":
        return jsonify({"status": True, "msg": "Line Webhook Success."})
    
    #POST
    elif request.method == "POST":
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        
        # Line
        linebot = Linebot(LINE_ACCESS_TOKEN, LINE_CHANNEL_SECRET)        
        
        #dataLIST =[{status, type, message, userID, replyToken, timestamp}]     
        dataLIST = linebot.parse(body, signature)
        for dataDICT in dataLIST:
            if dataDICT["status"]:
                if dataDICT["type"] == "message":
                    if dataDICT["message"] == 'Hi':
                        linebot.respText(dataDICT["replyToken"], "請你告訴我你想找的系")
                        return
                    if dataDICT["message"] == '謝謝':
                        linebot.respText(dataDICT["replyToken"], "期待下次再幫你忙喔！")
                    else:
             


    




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
