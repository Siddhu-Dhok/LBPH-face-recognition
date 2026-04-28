# train_lbph.py
import os
import cv2
import numpy as np
import pickle

dataset_dir = 'face-dataset'
model_dir = 'models'
os.makedirs(model_dir, exist_ok=True)

faces = []
labels = []
label_map = {}  # id->int
reverse_map = {}

current_label = 0
for student in os.listdir(dataset_dir):
    student_path = os.path.join(dataset_dir, student)
    if not os.path.isdir(student_path):
        continue
    label_map[student] = current_label
    reverse_map[current_label] = student
    for img_name in os.listdir(student_path):
        img_path = os.path.join(student_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(current_label)
    current_label += 1

faces = [cv2.resize(f, (200,200)) for f in faces]
labels = np.array(labels)

model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
model.train(faces, labels)
model.save(os.path.join(model_dir, 'lbph_model.yml'))
with open(os.path.join(model_dir, 'label_map.pkl'), 'wb') as f:
    pickle.dump(reverse_map, f)

print("Training complete. Saved model and label map.")
