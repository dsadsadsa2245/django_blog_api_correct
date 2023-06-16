from django.urls import path

from . import views

urlpatterns = [
    path('', views.LIkeCreateView.as_view()),
    path('<int:pk>/',views.LikeDeleteView.as_view()),
]
