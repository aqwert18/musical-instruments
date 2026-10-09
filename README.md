# 樂器維護紀錄表

管樂器維修保養紀錄 App。手機、電腦都能用，可加到手機主畫面全螢幕開啟。

- 網址：https://aqwert18.github.io/musical-instruments/
- 登入：Google 帳號（只有授權名單上的帳號能使用）
- 資料：存在登入者自己的 Google Drive「樂器維護紀錄」資料夾（`records.json` 與 `photos/`）

## 檔案

| 路徑 | 說明 |
|---|---|
| `index.html` | 正式版（由 `tools/build.py` 產生，請勿直接修改） |
| `prototype/index.html` | 介面與功能的原始樣板 |
| `tools/build.py` | 由樣板產生正式版：接上 Google 登入與 Google Drive |
| `tools/drive.js.txt`、`tools/save.js.txt` | Google 登入、Drive 讀寫、儲存紀錄的程式 |
| `tools/icons.py` | 產生 App 圖示 |
| `docs/google-setup.md` | Google Cloud 與 OAuth 設定教學 |

## 修改流程

1. 修改 `prototype/index.html`（或 `tools/` 內的程式）
2. 執行 `python tools/build.py`
3. 提交並推送到 `main`，GitHub Pages 會自動更新

## 新增授權帳號

1. 執行 `python tools/hash_email.py 新帳號@gmail.com`，把輸出的雜湊值加進 `prototype/index.html` 的 `ALLOWED_SHA256`，再執行 `python tools/build.py`（網站是公開的，所以帳號只存雜湊值，不存明文 Email）
2. Google Cloud Console → Google Auth Platform → 目標對象 → 測試使用者，加入同一個帳號
