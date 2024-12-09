from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import os

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = '1o15J+IQMhDcANiGr9vDkljZyut4U5ojuQlxy7Q9+lEoqjldcznC+vmjwNRGeg9zZTClEXp5cT3cgddIRE9pn7IYAgo20nl+dF8wccIOPWgWaZDPihkYiNkQ943RcyLh7oL7m3Qg3HexRltlVO5T4gdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = 'd4a805d159bb917a475bedc7d54916d2'

configuration = Configuration(access_token= YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_wrld():
    return "Hello,World"

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)
