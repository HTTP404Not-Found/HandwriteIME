# Google 手寫輸入法 (桌面版)

這是一個使用 Python 與 Tkinter 製作的桌面版「手寫輸入法」，  
透過呼叫 **Google Input Tools Handwriting API** 進行中文手寫辨識，  
並可自動將辨識結果貼到目前使用者正在輸入的視窗中。

## 功能特色

- 支援滑鼠在畫布上手寫中文字
- 停止書寫約 0.5 秒後自動呼叫 Google API 辨識
- 顯示多個候選字，點選即可輸入
- 自動記錄目標視窗，將文字貼回先前正在輸入的視窗
- 提供「立即辨識」與「清空」按鈕
- 視窗永遠置頂，方便搭配其他應用程式使用

## 執行環境與相依套件

目前程式為 **Windows + Python** 環境設計，使用到以下套件：

- Python 3.x
- Tkinter（標準庫，自帶）
- `requests`
- `Pillow`（PIL）
- `pyperclip`
- `pyautogui`
- `pywin32`（`pywin32` / `pypiwin32`）
- `pywin32` 相關：`win32gui`, `win32con`, `win32com.client`

### 安裝步驟

1. 先安裝 Python 3（若尚未安裝）

2. 建議建立虛擬環境（非必須）：

   ```bash
   python -m venv venv
   venv\Scripts\activate
