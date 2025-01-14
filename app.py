from flask import Flask, request, jsonify, render_template
import torch
from PIL import Image
import io

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    img = Image.open(io.BytesIO(image_bytes))

    # Perform object detection
    results = model(img)

    # Convert results to JSON
    detections = results.pandas().xyxy[0].to_dict(orient='records')
    return jsonify(detections)

if __name__ == '__main__':
    app.run(debug=True)
