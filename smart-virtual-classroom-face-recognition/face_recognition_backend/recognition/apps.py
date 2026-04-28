# from django.apps import AppConfig
# import cv2
# import pickle
# import os

# class RecognitionConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'recognition'

#     def ready(self):
#         global LBPH_MODEL, LABEL_MAP

#         model_path = os.path.join(os.path.dirname(__file__), "lbph/model.yml")
#         label_map_path = os.path.join(os.path.dirname(__file__), "lbph/label_map.pkl")

#         LBPH_MODEL = cv2.face.LBPHFaceRecognizer_create()
#         LBPH_MODEL.read(model_path)

#         with open(label_map_path, "rb") as f:
#             LABEL_MAP = pickle.load(f)
# from django.apps import AppConfig
# import os
# import cv2
# import pickle

# class RecognitionConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'recognition'

#     def ready(self):
#         # Load LBPH model
#         model_path = os.path.join(os.path.dirname(__file__), "lbph/model.yml")
#         label_map_path = os.path.join(os.path.dirname(__file__), "lbph/label_map.pkl")

#         if not os.path.exists(model_path):
#             print("❌ LBPH model not found:", model_path)
#             return

#         if not os.path.exists(label_map_path):
#             print("❌ Label map not found:", label_map_path)
#             return

#         print("✔ Loading LBPH model from:", model_path)

#         self.LBPH_MODEL = cv2.face.LBPHFaceRecognizer_create()
#         self.LBPH_MODEL.read(model_path)

#         with open(label_map_path, "rb") as f:
#             self.LABEL_MAP = pickle.load(f)

#         print("✔ LBPH model loaded successfully.")

from django.apps import AppConfig

class RecognitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recognition'