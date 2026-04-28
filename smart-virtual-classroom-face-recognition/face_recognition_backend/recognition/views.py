from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance
import cv2
import numpy as np

from .face_loader import load_model
from django.http import HttpResponse

def home(request):
    return HttpResponse("Face Recognition Backend is running!")

@api_view(['POST'])
def recognize_face(request):

    MODEL, LABEL_MAP = load_model()

    if MODEL is None:
        return Response({"error": "Model not loaded"}, status=500)

    if "image" not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)
    
    img_bytes = request.FILES["image"].read()
    np_img = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return Response({"status": "no_face"})

    x, y, w, h = faces[0]
    face_img = cv2.resize(gray[y:y+h, x:x+w], (200,200))

    label, confidence = MODEL.predict(face_img)

    if confidence < 60:
        student_id = LABEL_MAP.get(label)

        Attendance.objects.create(student_id=student_id)

        return Response({
            "status": "recognized",
            "student_id": student_id,
            "confidence": confidence
        })

    return Response({"status": "unknown", "confidence": confidence})