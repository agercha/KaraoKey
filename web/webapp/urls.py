"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from KaraoKeySite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"), # song select
    path('login', views.login_action, name='login'),
    path('welcome', views.welcome, name='welcome'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('quick_enter', views.quick_enter, name='quick_enter'),
    path('song/<str:song>', views.game, name="song"),
    path('chart', views.dummy_chart, name="chart"),
    path('restart-chart', views.restart_chart, name="restart_chart"),
    path('record', views.dummy_record, name="record"),
    path('get-pitch', views.get_pitch, name="get_pitch"),
    path('get-json', views.get_json, name="get_json"),
    path('get-chart-json', views.get_chart_json, name="get_chart_json"),
    path('get-target-json', views.get_target_json, name="get_target_json"),
]