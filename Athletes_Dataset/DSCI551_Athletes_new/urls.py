"""DSCI551_Athletes_new URL Configuration

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
from Athlete_app01 import views

urlpatterns = [
    # path("index/", views.index),
    # path("example/test1", views.tryexample01),
    path("example/test2", views.orm),
    path("athletesDB/", views.mainpage_soccer),
    path("athletesDB/Tennis/", views.tennis_page),
    path("athletesDB/NBA/", views.nba_page),
    path("athletesDB/NFL/", views.nfl_page),
    path("athletesDB/Search_Soccer/",views.search_soccer_page),
    path("athletesDB/Search_Tennis/",views.search_tennis_page),
    path("athletesDB/Search_NBA/",views.search_nba_page),
    path("athletesDB/Search_NFL/",views.search_nfl_page),
]
