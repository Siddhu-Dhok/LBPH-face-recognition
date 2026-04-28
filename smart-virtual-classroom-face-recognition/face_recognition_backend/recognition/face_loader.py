import os
import cv2
import pickle

MODEL = None
LABEL_MAP = None

def load_model():
    global MODEL, LABEL_MAP

    # Already loaded?
    if MODEL is not None and LABEL_MAP is not None:
        return MODEL, LABEL_MAP

    # Correct path
    model_path = os.path.join(os.path.dirname(__file__), "lbph/lbph_model.yml")
    label_map_path = os.path.join(os.path.dirname(__file__), "lbph/label_map.pkl")

    print("🔍 Loading LBPH model from:", model_path)

    if not os.path.exists(model_path):
        print("❌ Model file missing:", model_path)
        return None, None

    if not os.path.exists(label_map_path):
        print("❌ Label map missing:", label_map_path)
        return None, None

    # Load model
    MODEL = cv2.face.LBPHFaceRecognizer_create()
    MODEL.read(model_path)

    # Load label map
    with open(label_map_path, "rb") as f:
        LABEL_MAP = pickle.load(f)

    print("✔ LBPH model loaded successfully.")

    return MODEL, LABEL_MAP