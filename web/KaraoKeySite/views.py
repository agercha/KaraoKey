from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from KaraoKeySite.forms import *

# Create your views here.

@login_required
def home(request):
  return render(request, 'KaraoKeySite/home.html', {})

def quick_enter(request):
  if not User.objects.filter(username="admin").exists():
    admin = User.objects.create_user(username="admin", 
                                        password="password",
                                        email="user@aol.com",
                                        first_name="admin",
                                        last_name="user")
    admin.save()
    admin_profile = Profile(user=admin, 
                            first_name="admin",
                            last_name="user")
    admin_profile.save()
  else: 
    admin = User.objects.get(username="admin")

  admin = authenticate(username="admin", password="password")
  login(request, admin)
  return render(request, 'KaraoKeySite/home.html',  {})

def welcome(request):
    context = {}

    return render(request, 'KaraoKeySite/welcome.html',  context)

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'KaraoKeySite/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'KaraoKeySite/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return render(request, 'KaraoKeySite/home.html',  context)

def register_action(request):
  context = {}

  # Just display the registration form if this is a GET request.
  if request.method == 'GET':
      context['form'] = RegisterForm()
      return render(request, 'KaraoKeySite/register.html', context)

  # Creates a bound form from the request POST parameters and makes the 
  # form available in the request context dictionary.
  form = RegisterForm(request.POST)
  context['form'] = form

  # Validates the form.
  if not form.is_valid():
      return render(request, 'KaraoKeySite/register.html', context)

  # At this point, the form data is valid.  Register and login the user.
  new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                      password=form.cleaned_data['password'],
                                      email=form.cleaned_data['email'],
                                      first_name=form.cleaned_data['first_name'],
                                      last_name=form.cleaned_data['last_name'])
  new_user.save()

  new_user = authenticate(username=form.cleaned_data['username'],
                          password=form.cleaned_data['password'])

  new_user_profile = Profile(user=new_user, 
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'])
  new_user_profile.save()

  login(request, new_user)
  return render(request, 'KaraoKeySite/home.html',  context)

def logout_action(request):
  logout(request)
  return redirect(reverse('login'))

@login_required
def game(request, song):
  context = {"title": f'../../static/KaraoKeySite/songs/{song}'}
  print(context["title"])
  return render(request, "KaraoKeySite/game.html", context)