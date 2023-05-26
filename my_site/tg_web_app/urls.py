from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name = 'home'),
    path('chat/<int:pk>', views.chat, name = 'chat')
]