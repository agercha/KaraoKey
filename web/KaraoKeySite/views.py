from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from KaraoKeySite.Pitch_detection import process_wav_output_pitch
from KaraoKeySite.forms import *
from django.core.files.storage import default_storage
import wave


import json, time

def get_pitch(request):
  # right now, just return datetime
  
  # FOR KELLY!
  #request.FILES.get['small_recorded_audio'] is the wav file!
  full_audio_file = request.FILES.get("full_recorded_audio")
  small_audio_file = request.FILES.get("small_recorded_audio")

  with default_storage.open('tmp/'+small_audio_file.name, 'wb+'):
    wf = wave.open('tmp/'+small_audio_file.name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(1)
    wf.setframerate(44100)
    wf.writeframes(full_audio_file.read())
    wf.close()

  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  response = []

  response.append({'curr_pitch': process_wav_output_pitch('tmp/'+small_audio_file.name)})
  response_json = json.dumps(response)
  response_to_send = HttpResponse(response_json, content_type='application/json')
  response_to_send['Access-Control-Allow-Origin'] = '*'
  return response_to_send

@login_required
def home(request):
  return render(request, 'KaraoKeySite/home.html', {})

def dummy_chart(request):
  return render(request, 'KaraoKeySite/chart.html', {})

def dummy_record(request):
  return render(request, 'KaraoKeySite/record.html', {})

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