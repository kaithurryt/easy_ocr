import flask
import base64
import io
from PIL import Image, ImageDraw
import easyocr
import time
import numpy as np

app = flask.Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <body>
    <form action="/ocr" method="post" enctype="multipart/form-data">
        Select image to upload:
        <input type="file" name="image" id="image">
        <input type="submit" value="Upload Image" name="submit">
    </form>
    </body>
    </html>
    """

@app.route("/ocr", methods=["POST"])
def ocr():
    start = time.time()

    # 加载 OCR 模型
    reader = easyocr.Reader(["ch_sim", "en"], gpu=False, model_storage_directory="./", verbose=False)
    print("OCR model loaded, time:", time.time() - start)

    # 检查文件上传
    if "image" not in flask.request.files:
        return "No file part"
    img_file = flask.request.files["image"]
    if img_file.filename == "":
        return "No selected file"

    # 加载图像并转换为 RGB 格式
    img = Image.open(img_file).convert("RGB")
    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format="JPEG")  # 使用 JPEG 格式保存
    img_bytes = img_bytes_io.getvalue() # 转换为 NumPy 数组以供 OCR 使用

    print("Start OCR")
    results = reader.readtext(img_bytes)  # 使用 NumPy 数组作为输入

    # 绘制检测框并记录结果
    draw = ImageDraw.Draw(img)
    result_texts = []
    for bbox, text, prob in results:
        # bbox: 文本框的坐标 [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        x_min, y_min = bbox[0]
        x_max, y_max = bbox[2]
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
        result_texts.append(f"Text: {text}, Confidence: {prob:.2f}, Position: {bbox}")

    # 将处理后的图片转换为 base64 编码
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 生成结果页面
    result_html = "<h1>OCR Result:</h1>"
    for result_text in result_texts:
        result_html += f"<p>{result_text}</p>"
    result_html += f'<img src="data:image/png;base64,{img_base64}" alt="Processed Image"/>'

    end = time.time()
    print("OCR completed, time taken: {:.2f} seconds".format(end - start))
    result_html += f"<p>Time taken: {end - start:.2f} seconds</p>"

    return result_html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
