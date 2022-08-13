from pickle import FALSE
from main import GoogleAPIClient
from pprint import pprint
import pandas as pd

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('utQsTR9kVxafKMfgGXc1mYihJhoAvN2dve6Pm3b8lzHfeSpd880FssyHiF3rQxBCGKxHHq95hGY2P14BLjRDLtSNFg17Z3B+4gK4JpT9iRyw0xSOdzyiP0zqwjYmCRVTFOcR8YX9VYQo1Vy9ZBLpUwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('ad605b660f9bdd1f4706ab637b9da3e4')

line_bot_api.push_message('U3005f96c26253c99979ffabaf06cc57c', TextSendMessage(text='你可以開始了'))


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

class GoogleSheets(GoogleAPIClient):
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets'],
        )
    def getWorksheet(self, spreadsheetId: str, range: str):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=spreadsheetId,
            range=range,
        )
        response = request.execute()
        return response


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    inputText = TextSendMessage(text=event.message.text)
    room = ''
    bed = ''
    floor = ''
    newText = inputText.split('-')
    room = newText[0]
    if (len(room) == 3):
        floor = room[0:1]
        room = '10'+room
    elif (len(room) == 4):
        floor = room[0:2]
        room = '1'+room
    bed = newText[1]
    myWorksheet = GoogleSheets()
    try:
        floorSituation = myWorksheet.getWorksheet(
            spreadsheetId='1-Z71G5IrXe3oUCXqHVSao_lqksUy7u6Hi07YdoTKHZA',
            range = floor+'F'
        )['values']
        df = pd.DataFrame(floorSituation)
        df = df[df[0]==room]
        df = df[df[1]==bed]
        ret = df.iloc[0,2]
        message = "房號："+room+'-'+bed+'\n'
        if ret == 'TRUE':
            message += "床位已空，可以入住"
        elif ret == 'FALSE':
            message += "尚未退宿，請再等等"
    except:
        message = "房號："+room+'-'+bed+'\n'
        message += "查無此房"
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


