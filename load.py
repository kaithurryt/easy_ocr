import easyocr
from urllib.request import urlretrieve
import socket
import os
from zipfile import ZipFile
import logging

socket.setdefaulttimeout(60)

easyocr.easyocr.LOGGER.setLevel(logging.DEBUG)

print("Downloading EasyOCR model...")
target = "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/latin.zip"

urlretrieve(target, "model.zip")
print("Model downloaded successfully. target = ", target)

def download_and_unzip(url, filename, model_storage_directory, verbose=True):
    zip_path = os.path.join(model_storage_directory, 'temp.zip')
    print("Downloading EasyOCR model...")
    urlretrieve(url, zip_path)
    print("Model downloaded successfully. target = ", url)
    print("Unzipping EasyOCR model..., zip_path = ", zip_path)
    with ZipFile(zip_path, 'r') as zipObj:
        print("Extracting EasyOCR model..., filename = , model_storage_directory = ", filename, model_storage_directory)
        zipObj.extract(filename, model_storage_directory)
        print("Model unzipped.")
    print("Removing temporary zip file...")
    os.remove(zip_path)

print("Unzipping EasyOCR model...")
download_and_unzip(url=target, filename="latin.pth", model_storage_directory="./")
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