from user import views
from django.urls import path

urlpatterns = [
    path('login/', views.home, name="login"),
]
