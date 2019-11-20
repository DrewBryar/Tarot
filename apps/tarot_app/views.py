from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

CARD_LIST = [
    {'name': 'The Fool', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Magician', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The High Priestess', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Empress', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Emperor', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Hierophant', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Lovers', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Chariot', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Strength', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Hermit', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Wheel of Fortune', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Justice', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Hanged Man', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Death', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Temperance', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Devil', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Tower', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Star', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Moon', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Sun', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Judgement', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The World', 'image': 'image.png', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}}
]




def index(request):
    return render(request, "tarot_app/tarot.html")


def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birthday=request.POST['birthday'],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['first_name'] = new_user.first_name
            request.session['email'] = new_user.email
            return render(request, 'welcome.html')


def welcome(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in!")
        return redirect ('/')
    return render(request,'welcome.html')


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, "Either your email or password was input incorrectly.")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()): 
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            return redirect('/welcome')
        else:
            messages.error(
                request, "Either your email or password was input incorrectly.")
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
