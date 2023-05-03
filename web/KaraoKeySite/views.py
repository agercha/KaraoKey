from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from KaraoKeySite.Pitch_detection import process_wav_output_pitch, pitch_detect_from_file
from KaraoKeySite.feedback import feedback_from_res
from KaraoKeySite.forms import *
from django.core.files.storage import default_storage
import wave


from django.views.generic import TemplateView
#from chartjs.views.lines import BaseLineChartView

import json, time, os

COUNT_OUTER = 0
COUNT_INNER = 0

TARGET_SONGS = ["hbd", "dont_stop_believin"]

def get_target_json(request):
  global TARGET_SONGS
  song_name = TARGET_SONGS[int(request.POST["song_num"])]
  with open(os.path.abspath(os.getcwd()) + f"/KaraoKeySite/static/KaraoKeySite/{song_name}.json", "r") as f:
    response_json = json.load(f)
  global COUNT_OUTER
  global COUNT_INNER
  curr_vals = response_json[COUNT_OUTER]
  COUNT_INNER += 1
  if COUNT_INNER == curr_vals["length"]:
    COUNT_INNER = 0
    COUNT_OUTER = (COUNT_OUTER + 1)%len(response_json)
  l = curr_vals["length"]
  times = [str(i) for i in range(l)]
  curr_vals['labels'] = times
  curr_vals['targetfill'] = (curr_vals['target'][:COUNT_INNER])
  curr_vals = json.dumps(curr_vals)
  curr_vals = HttpResponse(curr_vals, content_type='application/json')
  curr_vals['Access-Control-Allow-Origin'] = '*'
  return curr_vals

def get_chart_json(request):
  with open(os.path.abspath(os.getcwd()) + "/KaraoKeySite/static/KaraoKeySite/hbd.json", "r") as f:
    response_json = json.load(f)
  global COUNT_OUTER
  global COUNT_INNER
  curr_vals = response_json[COUNT_OUTER]
  COUNT_INNER += 1
  if COUNT_INNER == curr_vals["length"]:
    COUNT_INNER = 0
    COUNT_OUTER = (COUNT_OUTER + 1)%len(response_json)
  start_index = 0
  for vals in response_json[:COUNT_OUTER]:
    start_index += vals["length"]
  end_index =  start_index + COUNT_INNER
  l = curr_vals["length"]
  times = [str(i) for i in range(l)]
  curr_vals['labels'] = times
  # curr_vals['user'] = (curr_vals['user'][:COUNT_INNER])
  curr_vals['start_index'] = start_index
  curr_vals['end_index'] = end_index
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

def upload(request):
  if request.method == "POST":
      form = RecordingForm()
      ogg_f = request.FILES["file"]
      if ogg_f.content_type == 'video/ogg':
        res = pitch_detect_from_file(ogg_f)
        score = feedback_from_res(os.path.abspath(os.getcwd()) + "/KaraoKeySite/static/KaraoKeySite/hbd.json", res)
        return chart(request, res, score)
  else:
      form = RecordingForm()
  return render(request, 'KaraoKeySite/upload.html', {"form": form})

def get_pitch(request):
  full_audio_file = request.FILES.get("full_recorded_audio")
  # small_audio_file = request.FILES.get("small_recorded_audio")

  wf = wave.open('tmp/'+full_audio_file.name, 'wb')
  wf.setnchannels(1)
  wf.setsampwidth(1)
  wf.setframerate(44100)
  wf.writeframes(full_audio_file.read())
  wf.close()

  response = []
  response.append({'curr_pitch': process_wav_output_pitch('tmp/'+full_audio_file.name)})
  response_json = json.dumps(response)
  response_to_send = HttpResponse(response_json, content_type='application/json')
  response_to_send['Access-Control-Allow-Origin'] = '*'
  
  return response_to_send

@login_required
def home(request):
  return render(request, 'KaraoKeySite/home.html', {})

def summary(request):
  return render(request, 'KaraoKeySite/summary.html', {})

def chart(request, user_vals=[], score=0):
  global COUNT_INNER, COUNT_OUTER
  COUNT_OUTER = 0
  COUNT_INNER = 0
  return render(request, 'KaraoKeySite/chart.html', {'user_vals':user_vals, 'score':score})

def dummy_chart(request):
  global COUNT_INNER, COUNT_OUTER
  COUNT_OUTER = 0
  COUNT_INNER = 0
  return render(request, 'KaraoKeySite/chart.html', {})


def restart_chart(request):
  global COUNT_INNER, COUNT_OUTER
  COUNT_OUTER = 0
  COUNT_INNER = 0
  curr_vals = HttpResponse({}, content_type='application/json')
  return curr_vals

def record(request, song="hbd"):
  global COUNT_INNER, COUNT_OUTER
  COUNT_OUTER = 0
  COUNT_INNER = 0
  if song == "hbd":
    context = {"backing": "../../static/KaraoKeySite/songs/hbdnovocals.mp3", "song_num" : 0}
  else:
    context = {"backing": "../../static/KaraoKeySite/songs/don't_stop_believin_backing_track.wav", "song_num" : 1}
  context["song_name"] = song
  print(context)
  return render(request, 'KaraoKeySite/record.html', context)

def record_hbd(request):
  return record(request, "hbd")

def record_dontstop(request):
  return record(request, "dontstop")

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