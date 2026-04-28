from flask import Flask, request, jsonify
import cv2
import numpy as np
import pickle
import os
from datetime import datetime
import requests  # to call your main backend attendance API

app = Flask(__name__)
model_path = 'models/lbph_model.yml'
label_map_path = 'models/label_map.pkl'

model = cv2.face.LBPHFaceRecognizer_create()
model.read(model_path)
with open(label_map_path, 'rb') as f:
    reverse_map = pickle.load(f)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Config: your main backend attendance endpoint
#BACKEND_ATTENDANCE_URL = 'http://<backend-host>/api/attendance/mark'  # change
BACKEND_ATTENDANCE_URL = "http://127.0.0.1:8000/api/attendance/mark"

def recognize_image(image_bytes, threshold=60):
    # image_bytes: raw bytes of image (BGR or grayscale)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return {'status': 'no_face'}

    # choose largest face
    x,y,w,h = max(faces, key=lambda f: f[2]*f[3])
    face_img = cv2.resize(gray[y:y+h, x:x+w], (200,200))
    label, confidence = model.predict(face_img)  # lower confidence = better match for LBPH
    # LBPH returns 'confidence' where lower is better; threshold tuned empirically
    if confidence < threshold:
        student_id = reverse_map.get(label)
        return {'status': 'recognized', 'student_id': student_id, 'confidence': float(confidence)}
    else:
        return {'status': 'unknown', 'confidence': float(confidence)}

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({'error': 'no image provided'}), 400
    file = request.files['image']
    img_bytes = file.read()
    result = recognize_image(img_bytes)
    if result['status'] == 'recognized':
        # Mark attendance in your main backend
        payload = {
            'student_id': result['student_id'],
            'timestamp': datetime.utcnow().isoformat()
        }
        # try:
        #     r = requests.post(BACKEND_ATTENDANCE_URL, json=payload, timeout=5)
        #     if r.status_code == 200:
        #         result['attendance_status'] = 'marked'
        #     else:
        #         result['attendance_status'] = f'backend_error:{r.status_code}'
        # except Exception as e:
        #     result['attendance_status'] = f'error:{str(e)}'
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
