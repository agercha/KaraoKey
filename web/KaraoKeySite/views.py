from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from KaraoKeySite.forms import *

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

import json, time, os

COUNT = 0

class chartJSON(BaseLineChartView):
  def get_curr_vals(self):
    with open(os.path.abspath(os.getcwd()) + "/KaraoKeySite/static/KaraoKeySite/dummy_data2.json", "r") as f:
      response_json = json.load(f)

    global COUNT
    curr_vals = response_json[COUNT]
    COUNT = (COUNT + 1)%len(response_json)
    # print(curr_vals)
    get_chart_json1()
    return curr_vals


  def get_labels(self):
    """Return 7 labels for the x-axis."""
    len = self.get_curr_vals()["length"]
    return [str(i) for i in range(len)]

  def get_providers(self):
    """Return names of datasets."""
    return [self.get_curr_vals()["lyrics"]]

  def get_data(self):
    """Return 1 dataset to plot."""
    return [self.get_curr_vals()["vals"]]

get_chart_json1 = chartJSON.as_view()

def get_chart_json(request):
  with open(os.path.abspath(os.getcwd()) + "/KaraoKeySite/static/KaraoKeySite/dummy_data2.json", "r") as f:
    response_json = json.load(f)
  global COUNT
  curr_vals = response_json[COUNT]
  COUNT = (COUNT + 1)%len(response_json)
  l = curr_vals["length"]
  times = [str(i) for i in range(l)]
  curr_vals['labels'] = times
  curr_vals = json.dumps(curr_vals)
  curr_vals = HttpResponse(curr_vals, content_type='application/json')
  curr_vals['Access-Control-Allow-Origin'] = '*'
  return curr_vals

def get_json(request):
  with open(os.path.abspath(os.getcwd()) + "/KaraoKeySite/static/KaraoKeySite/dummy_data.json", "r") as f:
    response_json = json.load(f)
  response_json = json.dumps(response_json)
  response_to_send = HttpResponse(response_json, content_type='application/json')
  response_to_send['Access-Control-Allow-Origin'] = '*'
  return response_to_send

def get_pitch(request):
  # right now, just return datetime
  
  # FOR KELLY!
  #request.FILES.get['small_recorded_audio'] is the wav file!
  full_audio_file = request.FILES.get("full_recorded_audio")
  small_audio_file = request.FILES.get("small_recorded_audio")

  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  response = []
  response.append({'curr_pitch': current_time}) # change this!
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