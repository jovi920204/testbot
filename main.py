import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# 以下代碼源自 https://developers.google.com/sheets/api/quickstart/python ，經過我們稍作更改
class GoogleAPIClient:
    SECRET_PATH = '.credentials/client_secret.json'
    CREDS_PATH = '.credentials/cred.json'
    
    def __init__(self, serviceName: str, version: str, scopes: list) -> None:
        self.creds = None
        # The file client_secret.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.CREDS_PATH):
            self.creds = Credentials.from_authorized_user_file(self.CREDS_PATH, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.SECRET_PATH, scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.CREDS_PATH, 'w') as token:
                token.write(self.creds.to_json())
        self.googleAPIService = build(serviceName, version, credentials=self.creds)

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

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    message = TextSendMessage("main test")
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    googleSheetAPI = GoogleAPIClient(
        'sheets',
        'v4',
        ['https://www.googleapis.com/auth/spreadsheets'],
        )
    print(googleSheetAPI.googleAPIService)