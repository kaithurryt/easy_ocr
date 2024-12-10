import easyocr as easyocr
from urllib.request import urlretrieve
import socket
import os
from zipfile import ZipFile
import logging

# socket.setdefaulttimeout(60)

# print("Downloading EasyOCR model...")
# target = "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/latin.zip"

# target2= "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip"

# urlretrieve(target, "model.zip")
# print("Model downloaded successfully. target = ", target)

# def download_and_unzip(url, filename, model_storage_directory, verbose=True):
#     zip_path = os.path.join(model_storage_directory, 'temp.zip')
#     print("Downloading EasyOCR model...")
#     urlretrieve(url, zip_path)
#     print("Model downloaded successfully. target = ", url)
#     print("Unzipping EasyOCR model..., zip_path = ", zip_path)
#     with ZipFile(zip_path, 'r') as zipObj:
#         print("Extracting EasyOCR model..., filename = , model_storage_directory = ", filename, model_storage_directory)
#         zipObj.extract(filename, model_storage_directory)
#         print("Model unzipped.")
#     print("Removing temporary zip file...")
#     os.remove(zip_path)

# urlretrieve(target2, "model2.zip")
# print("Model downloaded successfully. target = ", target2)

# print("Unzipping EasyOCR2 model...")
# download_and_unzip(url=target2, filename="craft_mlt_25k.pth", model_storage_directory="./")
# print("Model unzipped.")

# # print("Unzipping EasyOCR2 model... in ./model")
# # download_and_unzip(url=target2, filename="craft_mlt_25k.pth", model_storage_directory="./model")
# # print("Model unzipped.")

# print("Unzipping EasyOCR model...")
# download_and_unzip(url=target, filename="latin.pth", model_storage_directory="./")
# print("Model unzipped.")

# print("Loading EasyOCR model...")
# target3 = "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip"
# print("Downloading EasyOCR model...", target3)
# download_and_unzip(url=target3, filename="english_g2.pth", model_storage_directory="./")
# print("Model unzipped.")


print("Loading EasyOCR model...")
reader = easyocr.Reader(
    ["ch_sim", "en"],
    gpu=False,
    model_storage_directory="./",
    verbose=False,
)

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
