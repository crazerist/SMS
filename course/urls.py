from django.urls import path
from course.views import *

urlpatterns = [
    path('<slug:kind>/', home, name="course"),
]