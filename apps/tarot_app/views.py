from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

CARD_LIST = [
    {'name': 'The Fool', 'image': 'images/fool.jpg', 'description': 'Free spirit and unlimited potential.', 'categories': {
        'love': 'The Fool encourages you to have an open, curious mind and a sense of excitement. Throw caution to the wind and be ready to embrace the unknown, leaving behind any fear, worry     or anxiety about what may or may not happen. Today is about new experiences, personal growth, development, and adventure.', 
        'career': 'This is a time of great potential and opportunity for you right now. The world is your oyster, and anything can happen. Use your creative mind with a dash of spontaneity to     make the most of this magical time and bring forth your new ideas in powerful ways.', 
        'moody':'This is an excellent card to meditate on if you are struggling with dread, worry or self-doubt in your life. The Fool is your guide, as someone who is daring and            carefree. He is the embodiment of who you really are – your free spirit, your inner child, and your playful soul. Any time you experience fear, remember the essence of the Fool as he encourages you to acknowledge that fear and do it anyway! You never know what the future holds, but like the Fool, you must step into the unknown, trusting that the Universe will catch you and escort you along the way. Take a chance and see what happens.'}},
    {'name': 'The Magician', 'image': 'images/magician.jpg', 'description': 'Resourcefulness and power.', 'categories': {
        'love': 'a thing', 
        'career': 'The Magician brings you the tools, resources and energy you need to make your dreams come true. Seriously, everything you need right now is at your fingertips. You have the  spiritual (fire), physical (earth), mental (air) and emotional (water) resources to manifest your desires. And when you combine them with the energy of the spiritual and earthly realms, you will become a manifestation powerhouse! The key is to bring these tools together synergistically so that the impact of what you create is greater than the separate parts. Put your work into motion today. All you are missing today is discipline and momentum.',
        'home': 'a thing',
        'friendship': 'a thing' }},
    {'name': 'The High Priestess', 'image': 'images/high_priestess.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Empress', 'image': 'images/empress.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Emperor', 'image': 'images/emperor.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Hierophant', 'image': 'images/hierophant.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Lovers', 'image': 'images/lovers.jpg', 'description': 'we live in a society', 'categories': {
        'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Chariot', 'image': 'images/chariot.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Strength', 'image': 'images/strength.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Hermit', 'image': 'images/hermit.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Wheel of Fortune', 'image': 'images/wheel_of_fortune.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Justice', 'image': 'images/justice.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Hanged Man', 'image': 'images/hanged_man.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Death', 'image': 'images/death.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Temperance', 'image': 'images/temperance.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Devil', 'image': 'images/devil.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Tower', 'image': 'images/tower.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Star', 'image': 'images/star.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Moon', 'image': 'images/moon.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The Sun', 'image': 'images/sun.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Judgement', 'image': 'images/judgement.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'The World', 'image': 'images/world.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ace of Wands', 'image': 'images/wands_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Wands', 'image': 'images/wands_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Wands', 'image': 'images/wands_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Wands', 'image': 'images/wands_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Wands', 'image': 'images/wands_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Wands', 'image': 'images/wands_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Wands', 'image': 'images/wands_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Wands', 'image': 'images/wands_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Wands', 'image': 'images/wands_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Wands', 'image': 'images/wands_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Wands', 'image': 'images/wands_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Wands', 'image': 'images/wands_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Wands', 'image': 'images/wands_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Wands', 'image': 'images/wands_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Swords', 'image': 'images/swords_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Swords', 'image': 'images/swords_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Swords', 'image': 'images/swords_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Swords', 'image': 'images/swords_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Swords', 'image': 'images/swords_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Swords', 'image': 'images/swords_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Swords', 'image': 'images/swords_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Swords', 'image': 'images/swords_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Swords', 'image': 'images/swords_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Swords', 'image': 'images/swords_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Swords', 'image': 'images/swords_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Swords', 'image': 'images/swords_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Swords', 'image': 'images/swords_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Swords', 'image': 'images/swords_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Cups', 'image': 'images/cups_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Cups', 'image': 'images/cups_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Cups', 'image': 'images/cups_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Cups', 'image': 'images/cups_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Cups', 'image': 'images/cups_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Cups', 'image': 'images/cups_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Cups', 'image': 'images/cups_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Cups', 'image': 'images/cups_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Cups', 'image': 'images/cups_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Cups', 'image': 'images/cups_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Cups', 'image': 'images/cups_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Cups', 'image': 'images/cups_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Cups', 'image': 'images/cups_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Cups', 'image': 'images/cups_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},

    {'name': 'Ace of Pentacles', 'image': 'images/pentacles_ace.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Two of Pentacles', 'image': 'images/pentacles_twp.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Three of Pentacles', 'image': 'images/pentacles_three.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Four of Pentacles', 'image': 'images/pentacles_four.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Five of Pentacles', 'image': 'images/pentacles_five.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Six of Pentacles', 'image': 'images/pentacles_six.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Seven of Pentacles', 'image': 'images/pentacles_seven.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Eight of Pentacles', 'image': 'images/pentacles_eight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Nine of Pentacles', 'image': 'images/pentacles_nine.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Ten of Pentacles', 'image': 'images/pentacles_ten.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Page of Pentacles', 'image': 'images/pentacles_page.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Knight of Pentacles', 'image': 'images/pentacles_knight.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'Queen of Pentacles', 'image': 'images/pentacles_queen.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
    {'name': 'King of Pentacles', 'image': 'images/pentacles_king.jpg', 'description': 'we live in a society', 'categories': {'love': 'a thing', 'career': 'another thing','home': 'a thing','friendship': 'a thing'}},
]




def index(request):
    context = {
        "cards" : CARD_LIST
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
