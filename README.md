# Takodachi GPU Monitor 🐙

一個可愛的 Windows 系統列小工具！這隻 Takodachi 會一直待在你的系統列中，並透過動畫速度即時反映你的 NVIDIA GPU 使用率。當你的 GPU 滿載時，Tako 就會瘋狂扭動！

## 功能特色
- **即時動畫速度**：GPU 使用率越高，Tako 動得越快。
- **浮動狀態顯示**：把滑鼠游標停在 Tako 圖示上，即可顯示當前精確的 GPU 使用率（例如：`Tako GPU Monitor - 85%`）。
- **極低資源消耗**：使用 `PyQt5` 開發，在背景安靜且高效地執行。
- **無縫隱藏背景**：打包為獨立的 `.exe` 檔，執行時沒有煩人的終端機黑框。

## 需求環境
- Windows 系統
- NVIDIA 顯示卡
- Python 3 (如需自行編譯)

## 如何使用

可以直接下載打包好的 `tako_tray.exe` 執行檔，雙擊即可運行。
執行後，你可以打開一款 3D 遊戲，或是執行任何需要 GPU 運算的程式，並觀察右下角的 Tako 速度變化！

如果你想自行安裝與修改：
1. 確保你安裝了 Python。
2. 安裝必要的套件：
   ```bash
   pip install -r requirements.txt
   ```
3. 直接執行腳本：
   ```bash
   python tako_tray.py
   ```

## 如何打包成 .exe
如果你修改了程式碼，想重新打包成獨立的執行檔，請在終端機輸入：
```bash
pyinstaller -y --onefile --windowed --noconsole --icon=icon.ico --add-data "takodachi-ina.gif;." --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module matplotlib --exclude-module torch tako_tray.py
```
打包完成後的執行檔會產生在 `dist/` 資料夾內。
