import easyocr
from urllib.request import urlretrieve
import socket


socket.setdefaulttimeout(60)

print("Downloading EasyOCR model...")
target = "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/latin.zip"

urlretrieve(target, "model.zip")
print("Model downloaded successfully. target = ", target)

print("Unzipping EasyOCR model...")
easyocr.utils.download_and_unzip(url=target, filename="latin.pth", model_storage_directory="./")
print("Model unzipped.")


print("Loading EasyOCR model...")
reader = easyocr.Reader(['en'], gpu=False, model_storage_directory='./model')

# 测试图像路径
image_path = "receipt.webp"

# 使用模型加载图像并执行 OCR
results = reader.readtext(image_path)

# 输出结果
for bbox, text, confidence in results:
    print(f"Detected text: {text}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Bounding box: {bbox}")
    print("-" * 30)