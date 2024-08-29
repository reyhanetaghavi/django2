# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def menu(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user = request.user)
        except Profile.DoesNotExist:
            profile = None

    pizzas = Pizza.objects.all()
    burgers = Burger.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    appetizers = Appetizer.objects.all()
    drinks = Drink.objects.all()

    context = {
        'pizzas': pizzas,
        'burgers': burgers,
        'pastas': pastas,
        'salads': salads,
        'appetizers': appetizers,
        'drinks': drinks,
        'profile': profile
    }

    return render(request, 'menu.html', context)

def first_page(request):
    return render(request, 'first_page.html')


def info(request):
    return render(request, 'information.html')