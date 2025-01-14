from flask import Flask, request, jsonify, render_template
import torch
from PIL import Image
import io
import numpy as np
import cv2
from stereo.dianyuntu_yolo import get_d435_frames, undistortion, getRectifyTransform, rectifyImage, stereoMatchSGBM
from stereo.stereoconfig import stereoCamera

app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialize stereo camera
stereo = stereoCamera()

def calculate_distance(left_img, right_img, bbox):
    # Preprocess images
    left_img, right_img = preprocess(left_img, right_img)

    # Undistort images
    left_img = undistortion(left_img, stereo.cam_matrix_left, stereo.distortion_l)
    right_img = undistortion(right_img, stereo.cam_matrix_right, stereo.distortion_r)

    # Rectify images
    map1x, map1y, map2x, map2y, Q = getRectifyTransform(left_img.shape[0], left_img.shape[1], stereo)
    left_img, right_img = rectifyImage(left_img, right_img, map1x, map1y, map2x, map2y)

    # Compute disparity
    disparity_left, _ = stereoMatchSGBM(left_img, right_img)

    # Calculate distance
    x_center = int((bbox['xmin'] + bbox['xmax']) / 2)
    y_center = int((bbox['ymin'] + bbox['ymax']) / 2)
    distance = Q[2, 3] / (disparity_left[y_center, x_center] + Q[3, 3])

    return distance

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

    # Get stereo images
    left_img, right_img = get_d435_frames(stereo)

    if left_img is not None and right_img is not None:
        for detection in detections:
            distance = calculate_distance(left_img, right_img, detection)
            detection['distance'] = distance

    return jsonify(detections)

if __name__ == '__main__':
    app.run(debug=True)
