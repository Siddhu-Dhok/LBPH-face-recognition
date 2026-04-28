
from PIL import Image
import os

def preprocess_dataset(dataset_dir='face-dataset'):
    for student in os.listdir(dataset_dir):
        p = os.path.join(dataset_dir, student)
        if not os.path.isdir(p):
            continue
        for imgf in os.listdir(p):
            img_path = os.path.join(p, imgf)
            im = Image.open(img_path).convert('L').resize((200,200))
            im.save(img_path)
