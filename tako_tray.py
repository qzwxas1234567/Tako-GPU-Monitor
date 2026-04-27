import sys
import os
import pynvml
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QTimer
from PIL import Image, ImageSequence

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pynvml
gpu_handle = None
try:
    pynvml.nvmlInit()
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
except Exception as e:
    print(f"Error initializing NVML: {e}")

def get_gpu_load():
    if gpu_handle:
        try:
            util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
            return util.gpu / 100.0
        except Exception:
            pass
    return 0.0

class TakoTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TakoTray, self).__init__(parent)
        
        # Load GIF frames
        self.frames = []
        gif_path = resource_path('takodachi-ina.gif')
        original_duration = 100 # default
        try:
            gif = Image.open(gif_path)
            original_duration = gif.info.get('duration', 100) or 100
            for frame in ImageSequence.Iterator(gif):
                # Convert PIL image to QPixmap
                frame = frame.copy().convert("RGBA")
                data = frame.tobytes("raw", "RGBA")
                qim = QImage(data, frame.width, frame.height, QImage.Format_RGBA8888)
                self.frames.append(QIcon(QPixmap.fromImage(qim)))
        except Exception as e:
            print(f"Error loading GIF: {e}")
            sys.exit(1)

        if not self.frames:
            sys.exit(1)

        self.current_frame = 0
        self.setIcon(self.frames[0])
        self.setToolTip("Tako GPU Monitor")

        # Setup Menu
        menu = QMenu()
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_action)
        self.setContextMenu(menu)
        
        # Speed config (in ms)
        # Windows system tray update rate is capped, so 30ms is already very fast.
        self.max_delay = original_duration     # GPU 0% (original speed: 30ms)
        self.min_delay = max(10, int(original_duration / 4))  # GPU 100% (min 10ms to avoid OS ignore)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_icon)
        self.timer.start(self.max_delay)

    def update_icon(self):
        load = get_gpu_load()
        delay = int(self.max_delay - (load * (self.max_delay - self.min_delay)))
        
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setIcon(self.frames[self.current_frame])
        
        # Show GPU load in tooltip
        self.setToolTip(f"Tako GPU Monitor - {int(load * 100)}%")
        
        # Update timer interval dynamically
        if self.timer.interval() != delay:
            self.timer.setInterval(delay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    tray = TakoTray()
    tray.show()
    
    sys.exit(app.exec_())

