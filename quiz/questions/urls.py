from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name = "list_tests"),
    path('<int:test_id>', views.test_detail, name="test_detail"),
    path('question/<int:test_id>/<int:question_id>', views.question, name="question_name"),
    path('success/', views.success, name="success"),
]
