# questions/urls.py
from django.urls import path
from .views import QuestionListCreateView, QuestionDetailView,UserRegistrationView

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),

]
