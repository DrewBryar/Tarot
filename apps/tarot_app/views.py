from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, "tarot_app/tarot.html")

def main(request):
    context ={

    }
    pass