import torch
import time
import sys

print("=== Tako GPU 壓力測試程式 ===")
print("正在使用 PyTorch 將你的 RTX 3060 操到 100%...")
print("請觀察右下角的 Tako 圖示速度與數值！")
print("按下 Ctrl+C 即可結束測試。")

if not torch.cuda.is_available():
    print("找不到 CUDA 顯示卡，請確認驅動程式。")
    sys.exit(1)

device = torch.device("cuda:0")

# Create large random matrices
size = 8192
a = torch.rand(size, size, device=device)
b = torch.rand(size, size, device=device)

try:
    while True:
        # Perform heavy matrix multiplication continuously to max out GPU utilization
        c = torch.matmul(a, b)
        torch.cuda.synchronize()
except KeyboardInterrupt:
    print("\n測試結束！Tako 應該要冷靜下來了。")
