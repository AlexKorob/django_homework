from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name = "list_tests"),
    path('<int:test_id>/', views.test_detail, name="test_detail"),
    path('questions/<int:test_id>/', views.questions, name="questions"),
    path('success/', views.success, name="success"),
]
