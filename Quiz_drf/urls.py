"""Quiz_drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from account import views
from django.contrib import admin
from quiz import views as views_quiz


urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher_registration/',views.TeacherRegister.as_view()),
    path('student_registration/',views.StudentRegister.as_view()),
    path("login/",views.Login.as_view()),
    path('exam_topic/<int:pk>/',views_quiz.ExamTopicList.as_view()),
    path('exam_details/<int:pk>/',views_quiz.ExamDetails.as_view()),
    path('question_details/<int:pk>/<int:q_pk>/',views_quiz.QuestionDetails.as_view()),



]
