import easyocr

# 初始化 EasyOCR 模型
reader = easyocr.Reader(['en', 'ch_sim', 'ch_tra', 'ja', 'ko'])

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