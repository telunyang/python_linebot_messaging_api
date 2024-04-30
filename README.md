# LINE Bot (以 Message API 為例)
參考連結:
- [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
- [LINE Developer Documentation](https://developers.line.biz/en/docs/)
- [Message API](https://developers.line.biz/en/reference/messaging-api/)
- [Building a bot](https://developers.line.biz/en/docs/messaging-api/building-bot/#set-up-bot-on-line-developers-console)
- [Ngrok](https://ngrok.com/)

# (Required) 設定 LINE BOT
## 1. 設定流程
1. 安裝套件: `pip install -r requirements.txt`
2. 登入 [LINE Developers](https://developers.line.biz/console/profile)。
  - 可以用自己的 LINE 帳號登入，沒有的話可以註冊一個。
3. 新增 Provider (Create a new provider)，並輸入 Provider name。
4. 新增該 Provider 下的 Channel，選擇 Create Messaging API channel。
5. 之後依需求選擇、填寫基本資料，最後勾選頁面底下兩個「I have read agree to the ...」，按下 Create。
6. 按下/選擇先前 Create 的 Channel。
7. 到 Basic settings 標籤取得 `Channel secret`。
8. 到 Messaging API 標籤：
  - 取得 `Channel access token` (long-lived)。
  - 將 `Channel secret` 和 `Channel access token` 複製貼上到專案資料夾裡面的 `config.py` 當中
  - ![](https://i.imgur.com/jiSR4k1.png)
  - 設定 Webhook URL，並驗證 (verify) 是否請求成功 (success)。
    - **註: 若需要測試環境，可以選擇 ngrok 工具**
  - 開啟 webhook (Use webhook)。
  - 按下 Auto-reply messages 的 Edit 連結：
    - 聊天 關閉
    - 加入好友的歡迎訊息 關閉
    - Webhook **打開**
    - 自動回應訊息 關閉
    - (回 LINE Developers 首頁，刷新畫面，檢視設定結果)

## 2. 執行 LINE BOT 主程式
```bash
# 記得先安裝 sdk
$ pip install line-bot-sdk
```
```bash
# 未來依需求調整內容
$ python app.py
```

# 模擬 SSL 環境設定: ngrok
由於 LINE 的 webhook 需要使用 SSL 才能通過請求，若是在測試階段，本機沒有 SSL，此時我們需要一個暫時的 URI 來填入 Webhook URL。 

## 1. 登入 ngrok 儀表板
- 進入 [ngrok 首頁](https://ngrok.com/)。
- 註冊一個帳號，或是使用 GitHub 或 Google 帳號來登入。
- 進入儀表板頁面：
![儀表板畫面](https://i.imgur.com/tWTxsyK.png)
- 在儀表板上方，依作業系統來選擇下載 zip 檔，裡面是 ngrok 執行檔，並解壓縮到指定資料夾路徑：
![Windows下載畫面](https://i.imgur.com/DtkrHbq.png)
- 開啟/進入 Terminal，到解壓縮後的資料夾或專案目錄中，執行 ngrok 程式。
- (Optional) 若在 MacOS 或 Linux 環境 ngrok 沒有執行權限：
  - 額外開啟 Terminal，到指定資料夾或專案目錄中，以 ngrok 執行檔為主。
    - `chmod +x ngrok` 或 `chmod +x ./ngrok`
- 接下來執行以下指令，它會加入 auth token 到 ngrok.yml 當中 (可直接複製儀表板中的內容貼上):
  - `ngrok config add-authtoken 24e3*********************************************`

## 2. 執行 ngrok
專案使用的 port 號為 5005，可依需求調整:
```bash
# Windows
ngrok http http://localhost:8080
```
```bash
# MacOS 或 Linux
# 註: 可能需要提供 ngrok 可執行權限: chmod +x ngrok
./ngrok http http://localhost:8080
```

## 3. ngrok 啟動成功的畫面
![](https://i.imgur.com/V13yTIG.png)
**注意: 要複製 _Forwarding_ 那一列後面的網址，例如
`https://xxxx-xx-xxx-xxx-xx.ngrok-free.app`，之後 Webhook 設定會用到。**

## 4. 回到 LINE Developers
- 進入先前建立的 Channel。
- 在 Webhook settings 下面的 Webhook URL 當中，編輯/填寫 `https://xxxx-xx-xxx-xxx-xx.ngrok-free.app/callback`，記得後面要加上 **/callback**，這邊會跟主程式相呼應。
- 按下 Update 來儲存設定。
- 開啟 Use webhook。
![](https://i.imgur.com/D3gyZyU.png)


# 啟動服務

## 1. 執行主程式
回到專案資料夾後，準備執行主程式，建立文字生成服務:
```python
$ python app.py
```
若執行無誤，則會出現以下結果:
![](https://i.imgur.com/r0fY8M4.png)

## 2. 測試 Webhook
回到剛才 Message API 的 Webhook 設定，按下 Verify，如果沒有錯誤，則會出現以下結果:
![](https://i.imgur.com/H33XwAL.png)

**註: 記得加入自己建立的 LINE BOT 喔!!**

---

# (Optional) Rich Menu
為了在 LINE BOT 當中可以使用指定回話情緒的選單，需要加入 RichMenu、上傳 RichMenu 圖片，並指定預設的 RichMenu。以下會提供幾個程式，可依需求自行修改內容。

**註: 記得先將 config.py 的內容設定好。** 

## 1. 加入 Rich Menu
```python
$ python 1_addRichMenu.py
```
正常執行的結果，會輸出:
```python
'{"richMenuId":"RichMenu ID 的值"}'
```
**注意: 之後請將 richMenuId 的值，複製到 2_uploadRichMenuImage.py 和 3_setRichMenu.py 有關 richMenuId 變數當中**

## 2. 上傳 Rich Menu 圖片
將上傳專案資料夾當中的 richmenu.jpg，作為 Rich Menu 的背景圖片。
```python
$ python 2_uploadRichMenuImage.py
```
正常執行的結果，會輸出:
```
'{}'
```

## 3. 指定預設 Rich Menu
```python
$ python 3_setRichMenu.py
```
正常執行的結果，會輸出:
```
'{}'
```

# 最後提醒
如果主機沒有 SSL 檔案可以用，臨時需要展示，則建議使用 ngrok，此時啟動服務的程式 **app.py**，在最底下的主程式區塊當中，就可以使用:
```python
if __name__ == "__main__":
    app.run(
        debug=True,    # 啟用除錯模式
        host="0.0.0.0", # 設定 0.0.0.0 會對外開放
        port=5005       # 啟用 port 號
    )
```
如果主機當中，已經設置好 SSL 環境，則可以使用:
```python
if __name__ == "__main__":
    app.run(
        debug=True,    # 啟用除錯模式
        host="0.0.0.0", # 設定 0.0.0.0 會對外開放
        port=5005,      # 啟用 port 號
        ssl_context=(
            '/root/certs/fullchain4.pem', 
            '/root/certs/privkey4.pem') 
            # 建立 SSL 證證 for LINE Bot Webhook
    )
```
注意: 使用 ssl_context 設定前，一定要先確認是否同時有 **fullchain.pem** 與 **privkey.pem** 這兩個檔案。

