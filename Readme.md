# 系統需求

- Python 3.12

# 執行方式

```bash
pip install -r requirements.txt
streamlit run frontend.py --server.port 8080
```

# 部署流程

1. 將 Streamlit 程式碼上傳到 GitHub 公開倉庫。
2. 在根目錄準備一個 requirements.txt 檔案，列出所有需要的 Python 套件。
3. 登入 Streamlit Community Cloud 並連結 GitHub 帳號。
4. 選擇對應的倉庫與主檔案，點擊 Deploy 即可。

# 帳號

- 帳號：[EMAIL_ADDRESS]
- 密碼：[PASSWORD]

# 流程

1. 填寫表單
2. 點擊儲存
3. 點擊匯出
4. 點擊列印

# 匯出格式

- 匯出格式：PDF
- 匯出路徑：/home/eng/Andy/hitachi_SR_System/output/

# 匯入格式

- 匯入格式：Excel
- 匯入路徑：/home/eng/Andy/hitachi_SR_System/input/

# 系統架構

- 前端：Streamlit
- 後端：Streamlit
- 資料庫：SQLite

# 系統功能

- 填寫表單
- 儲存表單
- 匯出表單
- 列印表單

# 備註

- 系統目前僅支援單一使用者，若要支援多使用者，需要加入使用者管理功能。
- 系統目前僅支援單一表單，若要支援多表單，需要加入表單管理功能。
- 系統目前僅支援單一流程，若要支援多流程，需要加入流程管理功能。
