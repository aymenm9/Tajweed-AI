from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserViewSet.as_view()),
    path('user/', views.UserView.as_view()),
    path('generate_quiz/<str:topic>/', views.GenerateQuizView.as_view()),
    path('quiz/', views.QuizViewSet.as_view()),
    path('quiz/<int:pk>/', views.QuizView.as_view()),
    path('chatbot/', views.ChatbotView.as_view()),
    path('lessons/<int:pk>/', views.LessonsListView.as_view()),
    path('lessons/', views.lessonsView.as_view()),
    
]