from django.db import models

class Attendance(models.Model):
    student_id = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default="face_recognition")

    def __str__(self):
        return f"{self.student_id} - {self.timestamp}"