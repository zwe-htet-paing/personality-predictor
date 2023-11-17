from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_personality, name='predict_personality'),
    # Add other URL patterns as needed
    path('predict_text/', views.predict_text, name='predict_text'),
    path('result/', views.result, name="result"),
    path('login/', views.login, name="login")
]
