import flask
import base64
import io
from PIL import Image, ImageDraw
import easyocr
import time

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
    reader = easyocr.Reader(['en', 'ch_sim', 'ch_tra', 'ja', 'ko'])
    print("OCR model loaded, time:", time.time() - start)
    # 检查是否有文件上传
    if "image" not in flask.request.files:
        return "No file part"
    
    img_file = flask.request.files["image"]
    if img_file.filename == "":
        return "No selected file"
    
    try:
        # 使用 PIL 加载图像
        img = Image.open(img_file)
        
        # 转换图像为 RGB 格式（部分图像可能是单通道）
        img = img.convert("RGB")

        # 使用 EasyOCR 进行 OCR
        results = reader.readtext(img)

        # 绘制识别框
        draw = ImageDraw.Draw(img)
        result_texts = []
        for (bbox, text, prob) in results:
            # bbox: 文本框的坐标 [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            x_min, y_min = bbox[0]
            x_max, y_max = bbox[2]
            draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
            result_texts.append(f"Text: {text}, Confidence: {prob:.2f}, Position: {bbox}")

        # 将处理后的图片转换为 base64 编码
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # 返回结果页面
        result_html = f"<h1>OCR Result:</h1>"
        for result_text in result_texts:
            result_html += f"<p>{result_text}</p>"
        result_html += f'<img src="data:image/png;base64,{img_base64}" alt="Processed Image"/>'

        end = time.time()
        print("Take {} seconds".format(end-start))
        result_html += f"<p>Take {end - start:.2f} seconds</p>"
        

        return result_html

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
