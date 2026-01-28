import tkinter as tk
from tkinter import Canvas, Button, Label
from PIL import Image, ImageDraw
import requests
import json
import time
import pyperclip
import pyautogui
import win32gui
import win32con
import win32com.client

class GoogleHandwritingIME:
    def __init__(self, root):
        self.root = root
        self.root.title("Google 手寫輸入法 (桌面版)")
        self.root.geometry("400x600")
        self.root.attributes('-topmost', True)
        
        # API 設定
        self.api_url = "https://www.google.com/inputtools/request?ime=handwriting"
        
        # ✅ 新增：自動辨識計時器
        self.auto_recognize_timer = None
        self.auto_recognize_delay = 500  # 延遲 1 秒（毫秒）
        
        # 記錄目標視窗
        self.target_hwnd = None
        
        # 筆跡資料
        self.strokes = []
        self.current_stroke = {'x': [], 'y': [], 't': []}
        self.start_time = time.time() * 500
        
        # 初始化候選字
        self.candidates = []
        
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.05
        
        # WScript.Shell
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
        # UI
        instruction = Label(root, text="手寫中文，停止筆劃 0.5 秒後自動辨識", 
                           font=('Microsoft JhengHei', 10), fg='gray')
        instruction.pack(pady=5)
        
        self.canvas = Canvas(root, bg='white', width=350, height=350,
                            cursor='cross', relief='solid', borderwidth=2)
        self.canvas.pack(pady=10)
        self.canvas.bind('<Button-1>', self.start_stroke)
        self.canvas.bind('<B1-Motion>', self.draw_stroke)
        self.canvas.bind('<ButtonRelease-1>', self.end_stroke)
        
        # 偵測滑鼠進入（記錄目標視窗）
        self.canvas.bind('<Enter>', self.on_mouse_enter)
        self.canvas.bind('<Leave>', self.on_mouse_leave)
        
        # 按鈕
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="✅ 立即辨識", command=self.recognize,
                 width=10, bg='#4285f4', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ 清空", command=self.clear,
                 width=8, bg='#ea4335', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # 結果顯示
        self.result_label = Label(root, text="", font=('Microsoft JhengHei', 12), fg='#4285f4')
        self.result_label.pack(pady=5)
        
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10)
        
        self.candidate_buttons = []
        for i in range(5):
            btn = tk.Button(self.result_frame, text="", width=3, 
                           font=('Microsoft JhengHei', 14),
                           command=lambda idx=i: self.select_candidate(idx))
            btn.pack(side=tk.LEFT, padx=3)
            self.candidate_buttons.append(btn)
        
        # 狀態顯示
        self.status_label = Label(root, text="就緒", font=('Arial', 9), fg='gray')
        self.status_label.pack()
        
        self.target_info = Label(root, text="", font=('Arial', 8), fg='blue')
        self.target_info.pack()
    
    def on_mouse_enter(self, event):
        """當滑鼠進入手寫板時，記錄當前焦點視窗"""
        try:
            self.target_hwnd = win32gui.GetForegroundWindow()
            target_title = win32gui.GetWindowText(self.target_hwnd)
            print(f"🎯 記錄目標視窗: {target_title} (HWND: {self.target_hwnd})")
            self.target_info.config(text=f"📌 目標: {target_title[:20]}")
        except Exception as e:
            print(f"❌ 記錄視窗失敗: {e}")
    
    def on_mouse_leave(self, event):
        """當滑鼠離開時"""
        pass
    
    def start_stroke(self, event):
        """開始新筆劃"""
        # ✅ 清除之前的自動辨識計時器
        if self.auto_recognize_timer:
            self.root.after_cancel(self.auto_recognize_timer)
            self.auto_recognize_timer = None
        
        self.current_stroke = {
            'x': [event.x],
            'y': [event.y],
            't': [int(time.time() * 500 - self.start_time)]
        }
        print("✒️ 開始筆劃")
    
    def draw_stroke(self, event):
        """繪製筆劃"""
        x, y = event.x, event.y
        
        if self.current_stroke['x']:
            self.canvas.create_line(
                self.current_stroke['x'][-1], self.current_stroke['y'][-1],
                x, y, fill='black', width=3, capstyle=tk.ROUND, smooth=True
            )
        
        self.current_stroke['x'].append(x)
        self.current_stroke['y'].append(y)
        self.current_stroke['t'].append(int(time.time() * 500 - self.start_time))
    
    def end_stroke(self, event):
        """結束筆劃"""
        if self.current_stroke['x']:
            self.strokes.append(self.current_stroke)
            self.current_stroke = {'x': [], 'y': [], 't': []}
            
            print(f"✏️ 筆劃完成，{self.auto_recognize_delay}ms 後自動辨識...")
            
            # ✅ 清除之前的計時器
            if self.auto_recognize_timer:
                self.root.after_cancel(self.auto_recognize_timer)
            
            # ✅ 設定新的自動辨識計時器[216][219]
            self.auto_recognize_timer = self.root.after(
                self.auto_recognize_delay, 
                self.recognize
            )
            
            self.status_label.config(text="⏳ 等待中...", fg='orange')
    
    def recognize(self):
        """呼叫 Google API 辨識"""
        print(f"📤 自動辨識觸發（筆劃數: {len(self.strokes)}）")
        
        if not self.strokes:
            self.status_label.config(text="請先手寫", fg='red')
            return
        
        self.status_label.config(text="辨識中...", fg='orange')
        self.root.update()
        
        # ✅ 清除計時器
        if self.auto_recognize_timer:
            self.root.after_cancel(self.auto_recognize_timer)
            self.auto_recognize_timer = None
        
        try:
            payload = {
                "device": "Python Desktop App",
                "options": "enable_pre_space",
                "requests": [{
                    "writing_guide": {
                        "writing_area_width": 350,
                        "writing_area_height": 350
                    },
                    "ink": [[stroke['x'], stroke['y'], stroke['t']] 
                           for stroke in self.strokes],
                    "language": "zh",
                    "max_num_results": 10,
                    "max_completions": 0
                }]
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"📥 API 回應狀態: {response.status_code}")
            
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                status = result[0]
                
                if status == 'SUCCESS' and len(result) > 1 and result[1]:
                    candidates = result[1][0][1]
                    
                    print(f"✓ 候選字: {candidates}")
                    
                    self.candidates = candidates
                    
                    for i, btn in enumerate(self.candidate_buttons):
                        if i < len(candidates):
                            btn.config(text=candidates[i], state='normal')
                        else:
                            btn.config(text="", state='disabled')
                    
                    self.result_label.config(text=f"辨識完成，點擊選字或等待")
                    self.status_label.config(text="✅ 辨識完成", fg='green')
                    
                    # ✅ 新增：自動選擇第一個候選字（可選）
                    # self.select_candidate(0)
                else:
                    self.status_label.config(text="❌ 無法辨識", fg='red')
            else:
                self.status_label.config(text="❌ API 回應格式錯誤", fg='red')
        
        except Exception as e:
            self.status_label.config(text=f"❌ 錯誤: {str(e)}", fg='red')
            print(f"✗ 異常: {e}")
    
    def select_candidate(self, index):
        """選擇候選字並輸入"""
        if not self.candidates or index >= len(self.candidates):
            print(f"❌ 無效的候選字索引: {index}")
            return
        
        text = self.candidates[index]
        print(f"📝 選擇候選字: {text} (索引 {index})")
        
        self.input_text_with_focus_switch(text)
    
    def input_text_with_focus_switch(self, text):
        """自動切換焦點並輸入"""
        try:
            if not self.target_hwnd:
                print("❌ 未記錄目標視窗")
                self.status_label.config(text="❌ 未記錄目標視窗", fg='red')
                return
            
            print(f"📋 準備輸入文字: {text}")
            
            # 保存原始剪貼簿
            try:
                original = pyperclip.paste()
            except:
                original = ""
            
            # 複製到剪貼簿
            pyperclip.copy(text)
            print(f"✓ 文字已複製到剪貼簿: {text}")
            
            # 發送 ALT 鍵
            self.shell.SendKeys('%')
            print(f"✓ 已發送 ALT 鍵")   

            # 切換焦點
            win32gui.SetForegroundWindow(self.target_hwnd)
            print(f"✓ 已切換焦點到目標視窗")
            
            time.sleep(0.1)
            
            # 模擬 Ctrl+V
            pyautogui.hotkey('ctrl', 'v')
            print(f"✓ 已執行 Ctrl+V 貼上")
                        
            # 恢復原始剪貼簿
            try:
                pyperclip.copy(original)
            except:
                pass
            
            # 清空畫布
            self.clear()
            
            self.status_label.config(text="✅ 輸入完成", fg='green')
            print(f"✅ 輸入完成")
        
        except Exception as e:
            print(f"❌ 輸入失敗: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.config(text=f"❌ 輸入失敗: {e}", fg='red')
    
    def clear(self):
        """清空畫布"""
        # ✅ 清除計時器
        if self.auto_recognize_timer:
            self.root.after_cancel(self.auto_recognize_timer)
            self.auto_recognize_timer = None
        
        self.canvas.delete('all')
        self.strokes = []
        self.current_stroke = {'x': [], 'y': [], 't': []}
        self.start_time = time.time() * 500
        self.candidates = []
        
        self.result_label.config(text="")
        for btn in self.candidate_buttons:
            btn.config(text="", state='disabled')
        
        self.status_label.config(text="就緒", fg='gray')
        print("🗑️ 畫布已清空")


if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleHandwritingIME(root)
    root.mainloop()
