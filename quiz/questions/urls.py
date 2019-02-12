from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="list_tests"),
    path('<int:test_id>/', views.test_detail, name="test_detail"),
    path('test/<int:test_id>/', views.testrun, name="test"),
    path('testruns/', views.testrun_list, name="testruns"),
    path('testruns/<int:id>/', views.testrun_detail, name="testrun_detail"),
    path('testrun/add_notes/<int:id>', views.TestrunAddNotes.as_view(), name="testrun_add_notes"),

    path('questions/', views.QuestionListView.as_view(), name="questions_show"),
    path('question/create/', views.QuestionCreate.as_view(), name="question_create"),
    path('question/update/<int:id>/', views.QuestionUpdate.as_view(), name="question_update"),

    path('tests/', views.TestListView.as_view(), name="tests_show"),
    path('test/create/', views.TestCreate.as_view(), name="test_create"),
    path('test/update/<int:id>/', views.TestUpdate.as_view(), name="test_update"),
    path('test/add_notes/<int:id>', views.TestAddNotes.as_view(), name="test_add_notes"),

    path('register/', views.UserCreate.as_view(), name="user_create"),
    path('login/', views.UserAuthentication.as_view(), name="user_login"),
    path('logout/', views.UserLogout.as_view(), name="user_logout")

]
