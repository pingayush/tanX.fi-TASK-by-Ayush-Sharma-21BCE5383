# price_alert/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the Price Alert App!")
