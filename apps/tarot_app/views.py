from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

CARD_LIST = [
    {'name': 'The Fool', 'image': 'images/fool.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Magician', 'image': 'images/magician.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The High Priestess', 'image': 'images/high_priestess.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Empress', 'image': 'images/empress.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Emperor', 'image': 'images/emperor.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Hierophant', 'image': 'images/hierophant.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Lovers', 'image': 'images/lovers.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Chariot', 'image': 'images/chariot.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Strength', 'image': 'images/strength.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Hermit', 'image': 'images/hermit.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Wheel of Fortune', 'image': 'images/wheel_of_fortune.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Justice', 'image': 'images/justice.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Hanged Man', 'image': 'images/hanged_man.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Death', 'image': 'images/death.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Temperance', 'image': 'images/temperance.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Devil', 'image': 'images/devil.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Tower', 'image': 'images/tower.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Star', 'image': 'images/star.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Moon', 'image': 'images/moon.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The Sun', 'image': 'images/sun.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'Judgement', 'image': 'images/judgement.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}},
    {'name': 'The World', 'image': 'images/world.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing'}}
]




def index(request):
    context = {
        "cards":CARD_LIST
    }
    return render(request, "tarot_app/tarot.html",context)


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
