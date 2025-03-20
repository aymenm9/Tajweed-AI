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
    path('goals/', views.GoalsView.as_view()),
    path('recitation_correction/', views.RecitationCorrectionView.as_view()),
    path('get_verse/<str:topic>/', views.VerseView.as_view()),
    path('quiz_stats/', views.QuizStatsView.as_view()),
    
]