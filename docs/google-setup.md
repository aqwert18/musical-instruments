# Google 登入與 Google Drive 權限設定教學

目標：讓「樂器維護紀錄表」能用 Google 帳號登入，並把每位使用者的紀錄與照片存進**他自己的** Google Drive。

完成後你只需要交給我一樣東西：**OAuth 用戶端 ID**（長得像 `1234567890-xxxx.apps.googleusercontent.com`）。
用戶端 ID 不是密碼，可以放在網頁程式裡。**不需要**用戶端密鑰（Client Secret），也不需要 API 金鑰。

---

## 步驟 1：建立 Google Cloud 專案

1. 用管理者的 Gmail 登入 <https://console.cloud.google.com/>
2. 第一次使用時，同意服務條款。
3. 點畫面上方的專案選單 →「新增專案」
   - 專案名稱：`musical-instruments`
   - 機構：無機構
4. 按「建立」，等幾秒後切換到這個專案（上方選單要顯示 `musical-instruments`）。

## 步驟 2：啟用 Google Drive API

1. 左側選單 →「API 和服務」→「程式庫」
2. 搜尋 `Google Drive API` → 點進去 → 按「啟用」

## 步驟 3：設定 OAuth 同意畫面（Google Auth Platform）

左側選單 →「API 和服務」→「OAuth 同意畫面」。新版介面會帶你到「Google Auth Platform」，按「開始」。

1. **應用程式資訊**
   - 應用程式名稱：`樂器維護紀錄表`
   - 使用者支援電子郵件：選你的 Gmail
2. **目標對象**：選「外部」
3. **聯絡資訊**：填你的 Gmail
4. 勾選同意政策 →「建立」

接著在左側的 Google Auth Platform 選單繼續：

5. **目標對象（Audience）** → 「測試使用者」→「新增使用者」，加入：
   - 每一個要使用本 App 的 Google 帳號

   > 發布狀態維持「**測試中**」。在這個狀態下，**只有測試使用者名單上的帳號能通過 Google 登入**。這就是由 Google 把關的授權名單，網頁程式裡也會再檢查一次。以後要加人，就回到這裡新增（上限 100 人）。

6. **資料存取（Data Access）** →「新增或移除範圍」，勾選以下 4 個後更新、儲存：
   - `openid`
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
   - `.../auth/drive.file`

   > `drive.file`：App 只能看到**它自己建立**的檔案，看不到使用者 Drive 裡的其他東西。這是權限最小的範圍，屬於非敏感範圍，不需要送 Google 審核。

## 步驟 4：建立 OAuth 用戶端 ID

1. Google Auth Platform →「用戶端（Clients）」→「建立用戶端」
2. 應用程式類型：**網頁應用程式**
3. 名稱：`樂器維護紀錄表 Web`
4. **已授權的 JavaScript 來源**，新增兩筆：
   - `https://aqwert18.github.io`（正式網址，GitHub Pages）
   - `http://localhost:5500`（我在電腦上開發測試用）
5. 「已授權的重新導向 URI」**留空**
6. 按「建立」→ 複製畫面上的**用戶端 ID**，貼給我

> 來源只能寫網域，不能有路徑或結尾的 `/`。修改設定後，可能要等 5 分鐘到幾小時才會生效。

## 步驟 5：開啟 GitHub Pages（等程式寫好再做）

1. 到 <https://github.com/aqwert18/musical-instruments> →「Settings」→「Pages」
2. Source 選「Deploy from a branch」，Branch 選 `main`、資料夾選 `/ (root)` → Save
3. 網址會是 `https://aqwert18.github.io/musical-instruments/`
4. 手機用 Chrome 或 Safari 開這個網址 →「加到主畫面」，就能像 App 一樣全螢幕開啟。

---

## 資料會怎麼存（正式版規劃）

每位使用者登入後，App 會在**他自己的** Google Drive 建立：

```
我的雲端硬碟/
└── 樂器維護紀錄/
    ├── records.json          ← 所有維修紀錄
    └── photos/
        ├── 2026-10-09_長笛_1.jpg
        └── ...
```

- 兩個帳號各存各的，彼此看不到。
- 使用者可以在 Drive 直接看到這個資料夾和照片，也可以自行備份。
- 照片上傳前會先壓縮（長邊約 1600px），節省空間與流量。

## 常見狀況

| 畫面訊息 | 原因 / 處理 |
|---|---|
| 「Google 尚未驗證這個應用程式」 | 測試中的 App 都會出現。點「繼續」即可，只有測試使用者看得到這個畫面。 |
| `Error 403: access_denied` | 這個帳號不在測試使用者名單，回到步驟 3-5 加入。 |
| `Error 400: origin_mismatch` | 網址沒有列在步驟 4 的 JavaScript 來源，或還沒生效。 |
| 每隔約 1 小時要重新授權 | Google 存取權杖的正常效期。正式版會在背景自動更新，必要時跳出一次確認。 |
