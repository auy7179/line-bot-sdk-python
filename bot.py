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

app = Flask(__name__)

line_bot_api = LineBotApi('2aCqScEbnWGwCosBsOB0tOW/lfOL0JvNfefZEFP37YGZzoCuahuLAV5gG64UBX1u/Ep2AZTkNtySLct/kZZ5qoNVcTLjpssO/M6TIa+8jeXVMv6Ob7cSMn9vZIKeXCXpVzBf1v47996SsJHzDOvqsgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8374e28538d448f73ae8c1d0420bb0e9')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
