from django.urls import path
from . import views

urlpatterns = [
    path('conversation/<str:username>/', views.conversation_view, name='conversation'),
]