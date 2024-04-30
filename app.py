# flask 模組
from flask import Flask, request, abort, send_from_directory

# 網路請求工具
import requests

# line bot sdk python 模組
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
    TextMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    VideoMessageContent,
    AudioMessageContent
)

# 實體化 flask 物件
app = Flask(__name__)

# 自訂組態檔 (放置 LINE Bot 重要設定。未來可以改用 .env 檔案，請參考: https://pypi.org/project/python-dotenv/)
from config import Config
config = Config()
configuration = Configuration(access_token=config['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['YOUR_CHANNEL_SECRET'])

# 貼上 ngrok 提供的網址
# 參考連結: https://i.imgur.com/V13yTIG.png
prefix_url = "https://87ff-66-234-246-87.ngrok-free.app"





'''
路由設定
'''
# 給 LINE Developers 管理平台用的 webhook (確認服務是否存活)
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

# 上傳檔案路徑
@app.route('/files/<path>')
def get_tmp_path(path):
    return send_from_directory('files', path)

# 處理 text 訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    with ApiClient(configuration) as api_client:
        # 取得使用 api 的物件
        api_instance  = MessagingApi(api_client)

        # 取得 replyToken
        replyToken = event.reply_token

        # 取得訊息的內容
        replyText = event.message.text

        # 回覆一到多個文字內容 (最多 5 個)
        list_reply = [
            TextMessage(text=replyText)
        ]

        # 將文字透過 LINE Bot 回覆給使用者
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=replyToken,
                messages=list_reply
            )
        )

# 處理 image 訊息
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    with ApiClient(configuration) as api_client:
        # 取得使用 api 的物件
        api_instance  = MessagingApi(api_client)

        # 取得 replyToken
        replyToken = event.reply_token
        
        # 取得訊息 ID
        messageId = event.message.id

        # 請求標頭
        my_headers = {
            'Authorization': f'Bearer {config["YOUR_CHANNEL_ACCESS_TOKEN"]}',
        }

        url = f"https://api-data.line.me/v2/bot/message/{messageId}/content"

        # 執行請求 (新增 RichMenu)
        response = requests.get(url = url, headers = my_headers)

        # 儲存圖片 (response.content 是二進位制資料)
        with open(f"files/{messageId}.jpg", "wb") as file:
            file.write(response.content)

        replyText = f"已收到圖片：{messageId}.jpg"

        # 回覆一到多個文字內容 (最多 5 個)
        list_reply = [
            TextMessage(text=replyText),
            ImageMessage(original_content_url=f"{prefix_url}/files/{messageId}.jpg", preview_image_url=f"{prefix_url}/files/{messageId}.jpg")
        ]

        # 將文字透過 LINE Bot 回覆給使用者
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=replyToken,
                messages=list_reply
            )
        )

# 處理 video 訊息
@handler.add(MessageEvent, message=VideoMessageContent)
def handle_video_message(event):
    with ApiClient(configuration) as api_client:
        # 取得使用 api 的物件
        api_instance  = MessagingApi(api_client)

        # 取得 replyToken
        replyToken = event.reply_token
        
        # 取得訊息 ID
        messageId = event.message.id

        # 請求標頭
        my_headers = {
            'Authorization': f'Bearer {config["YOUR_CHANNEL_ACCESS_TOKEN"]}',
        }

        url = f"https://api-data.line.me/v2/bot/message/{messageId}/content"

        # 執行請求 (新增 RichMenu)
        response = requests.get(url = url, headers = my_headers)

        # 儲存影片 (response.content 是二進位制資料)
        with open(f"files/{messageId}.mp4", "wb") as file:
            file.write(response.content)

        replyText = f"已收到影片：{messageId}.mp4"

        # 回覆一到多個文字內容 (最多 5 個)
        list_reply = [
            TextMessage(text=replyText),
            VideoMessage(original_content_url=f"{prefix_url}/files/{messageId}.mp4", preview_image_url=f"{prefix_url}/files/{messageId}.mp4")
        ]

        # 將文字透過 LINE Bot 回覆給使用者
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=replyToken,
                messages=list_reply
            )
        )

# 處理 audio 訊息
@handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event):
    with ApiClient(configuration) as api_client:
        # 取得使用 api 的物件
        api_instance  = MessagingApi(api_client)

        # 取得 replyToken
        replyToken = event.reply_token
        
        # 取得訊息 ID
        messageId = event.message.id

        # 請求標頭
        my_headers = {
            'Authorization': f'Bearer {config["YOUR_CHANNEL_ACCESS_TOKEN"]}',
        }

        url = f"https://api-data.line.me/v2/bot/message/{messageId}/content"

        # 執行請求 (新增 RichMenu)
        response = requests.get(url = url, headers = my_headers)

        # 儲存影片 (response.content 是二進位制資料)
        with open(f"files/{messageId}.m4a", "wb") as file:
            file.write(response.content)

        replyText = f"已收到音檔：{messageId}.m4a"

        # 回覆一到多個文字內容 (最多 5 個)
        list_reply = [
            TextMessage(text=replyText),
            AudioMessage(original_content_url=f"{prefix_url}/files/{messageId}.m4a", duration=1000)
        ]

        # 將文字透過 LINE Bot 回覆給使用者
        api_instance.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=replyToken,
                messages=list_reply
            )
        )



'''
主程式
'''
if __name__ == "__main__":
    # 建立 flask web service (使用 ngrok 的情形下)
    app.run(
        debug=True,     # 進入除錯模式
        host="0.0.0.0", # 設定 0.0.0.0 對外開放，讓 Webhook 機制確認 Web API 是否存活
        port=8080       # 啟用 port 號
    )

    # 有自己的 SSL certs 檔案，再開啟下方設定，修正 ssl_context 的值。
    # app.run(
    #     debug=True,     # 進入除錯模式
    #     host="0.0.0.0", # 設定 0.0.0.0 會對外開放
    #     port=5005,      # 啟用 port 號
    #     # ssl_context=('/certs/fullchain4.pem', '/certs/privkey4.pem') # 建立 SSL 證證 for LINE Bot Webhook
    # )