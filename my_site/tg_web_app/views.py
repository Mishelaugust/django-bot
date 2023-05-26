from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users,Chats


def home(request):
    users = Users.objects.all()
    return render(request, 'home.html', {'users':users})

def chat(request, pk):
    chats = Chats.objects.filter(user_id=pk)
    users = Users.objects.get(id=pk)
    return render(request, 'chat.html', {'chats':chats, 'users':users})
