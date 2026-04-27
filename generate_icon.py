from PIL import Image

# Read the GIF
img = Image.open('takodachi-ina.gif')

# Take the first frame
img.seek(0)

# Convert to RGBA just in case
img = img.convert("RGBA")

# Save as an icon file with multiple sizes for Windows
img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

print("成功將 takodachi-ina.gif 轉換為 icon.ico！")
