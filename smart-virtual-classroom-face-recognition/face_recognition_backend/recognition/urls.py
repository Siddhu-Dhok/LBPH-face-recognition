from django.urls import path
from .views import recognize_face

urlpatterns = [
    path('recognize/', recognize_face),
]