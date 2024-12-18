import os
import random
import string
from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

model = YOLO('./models/bugsV1.pt')

IMAGES_FOLDER = os.path.join(os.getcwd(), 'images')
os.makedirs(IMAGES_FOLDER, exist_ok=True)

def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    extension = os.path.splitext(original_filename)[1]
    return f"{timestamp}_{random_str}{extension}"

@app.route('/detect', methods=['POST'])
def detect_pests():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert('RGB')
    frame = np.array(image)

    results = model(frame)

    annotated_frame = results[0].plot()

    filename = generate_unique_filename(image_file.filename)
    file_path = os.path.join(IMAGES_FOLDER, filename)

    app.logger.info(f"Saving annotated image to: {file_path}")
    cv2.imwrite(file_path, annotated_frame)

    detections_dict = {}
    total_detections = 0
    for result in results[0].boxes:
        cls = int(result.cls)
        confidence = float(result.conf)
        label = results[0].names[cls]
        if label not in detections_dict:
            detections_dict[label] = {'count': 0, 'confidence': 0.0}
        detections_dict[label]['count'] += 1
        detections_dict[label]['confidence'] += confidence
        total_detections += 1

    detections = []
    for label, data in detections_dict.items():
        detections.append({
            'label': label,
            'confidence': data['confidence'] / data['count'],
            'count': data['count'],
            'percentage': (data['count'] / total_detections) * 100
        })

    return jsonify({
        'detections': detections,
        'image_path': f"images/{filename}"
    }), 200

@app.route('/images/<filename>')
def serve_image(filename):
    file_path = os.path.join(IMAGES_FOLDER, filename)
    app.logger.info(f"Requested file path: {file_path}")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg')
    else:
        app.logger.warning(f"File not found: {file_path}")
        return jsonify({'error': f'File {filename} not found'}), 404

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5001))

    app.run(host=host, port=port, debug=True)
