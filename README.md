# HandwriteIME

一個使用 Python 與 Tkinter 製作的桌面版「手寫輸入法」，透過呼叫 **Google Input Tools Handwriting API** 進行中文手寫辨識，並可自動將辨識結果貼到目前使用者正在輸入的視窗中。

## 功能特色

- ✍️ 支援滑鼠在畫布上手寫中文字
- ⚡ 停止書寫約 0.5 秒後自動呼叫 Google API 辨識
- 📝 顯示多個候選字，點選即可輸入
- 🎯 自動記錄目標視窗，將文字貼回先前正在輸入的視窗
- 🔄 提供「立即辨識」與「清空」按鈕
- 📌 視窗永遠置頂，方便搭配其他應用程式使用

## 執行環境與相依套件

本程式為 **Windows + Python** 環境設計，使用到以下套件：

### 系統需求

- Python 3.x
- Windows 作業系統
- 網路連線（呼叫 Google API）

### 相依套件

- `Tkinter`（標準庫，自帶）
- `requests`
- `Pillow`（PIL）
- `pyperclip`
- `pyautogui`
- `pywin32`
- `win32gui`, `win32con`, `win32com.client`（pywin32 相關）

## 安裝步驟

### 1. 安裝 Python 3

若尚未安裝，請從 [python.org](https://www.python.org/) 下載並安裝 Python 3.x 版本。

### 2. 建立虛擬環境（推薦）

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安裝相依套件

```bash
pip install requests pillow pyperclip pyautogui pywin32
```

### 4. 驗證 Tkinter

確認可以導入 Tkinter（通常 Windows 版 Python 會內建）：

```bash
python -c "import tkinter; print('tkinter ok')"
```

若出現錯誤，請重新安裝 Python 時勾選 tcl/tk 選項。

## 使用方法

### 啟動程式

```bash
git clone https://github.com/<你的帳號>/HandwriteIME.git
cd HandwriteIME
python main.py
```

（若檔名不是 `main.py`，請改成實際檔名，例如 `handwrite_ime.py`）

### 使用步驟

1. **準備目標視窗**  
   把滑鼠移到你要輸入文字的視窗（例如記事本、Word、瀏覽器輸入框），讓它取得焦點。

2. **記錄目標視窗**  
   將滑鼠移到本程式的手寫畫布上，此時程式會自動記錄目前的「目標視窗」。

3. **手寫中文**  
   在白色畫布上用滑鼠左鍵按住書寫中文字。

4. **自動辨識**  
   放開滑鼠後約 0.5 秒，程式會自動呼叫 Google Handwriting API 進行辨識。

5. **選擇候選字**  
   下方會出現最多 5 個候選字，點選其中一個，即會自動切回剛才的目標視窗並貼上文字。

6. **重新書寫**  
   若要重新書寫，可按「🗑️ 清空」按鈕清除畫布。

## 程式結構說明

### 主要類別：`GoogleHandwritingIME`

| 屬性/方法 | 功能說明 |
|----------|--------|
| `canvas` | 手寫畫布，負責接收滑鼠事件（開始、移動、結束） |
| `strokes` | 紀錄所有筆劃的座標與時間戳，傳給 Google API 使用 |
| `recognize()` | 組成 payload，呼叫 Google Handwriting API 進行辨識 |
| `select_candidate(index)` | 處理候選字按鈕點擊事件 |
| `input_text_with_focus_switch(text)` | 將焦點切回目標視窗，並透過剪貼簿與 `Ctrl+V` 貼上文字 |
| `auto_recognize_timer` | 透過 `root.after()` 在結束筆劃後延遲觸發自動辨識 |

### 核心功能流程

```
使用者手寫
    ↓
canvas.draw_stroke() 紀錄筆劃
    ↓
canvas.end_stroke() 設定自動辨識計時器
    ↓
auto_recognize_timer 觸發（0.5 秒延遲）
    ↓
recognize() 呼叫 Google API
    ↓
解析候選字並顯示按鈕
    ↓
使用者點擊候選字
    ↓
input_text_with_focus_switch() 輸入文字到目標視窗
```

## 注意事項

⚠️ **重要提示**

- **需要網路連線**：程式必須連線到 Google 的手寫輸入 API 才能使用。
- **Windows 平台優先**：本程式主要在 Windows 平台開發與測試，其他作業系統（macOS、Linux）可能無法使用 `pywin32` 與 `win32gui` 等功能。
- **目標視窗記錄失敗**：若未成功取得目標視窗，程式會顯示「未記錄目標視窗」的警告訊息。
- **API 變動風險**：Google 的非公開 API 可能未來有變動風險，若 API 介面或網址更改，程式可能需同步調整。
- **剪貼簿操作**：程式會暫時使用剪貼簿貼上文字，輸入完成後會恢復原始內容。

## 授權條款

MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 貢獻

如果你有任何建議或發現 Bug，歡迎提交 Issue 或 Pull Request！

## 常見問題 (FAQ)

**Q: 程式無法辨識我的筆跡**  
A: 請確保：
   - 筆劃連貫清晰
   - 停止後等待 0.5 秒讓程式自動辨識
   - 網路連線正常
   - Google API 未被限制

**Q: 文字無法貼到目標視窗**  
A: 請檢查：
   - 滑鼠是否有進入畫布（讓程式記錄目標視窗）
   - 目標視窗是否支援 `Ctrl+V` 貼上
   - 嘗試手動點擊「立即辨識」而非依賴自動辨識

**Q: 支援 macOS 或 Linux 嗎？**  
A: 目前不支援。程式依賴 `pywin32` 等 Windows 特定套件。未來可能考慮跨平台版本。

---

**Made with ❤️ for Chinese Input**
