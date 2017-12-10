"""football_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from views.match_list import MatchList
from views.teamlist import TeamList
from views.team import Team
from views.player_list import PlayerList
from views.player import Player
from views.match_info import MatchInfo
from views.add_player import AddPlayer
from views.add_team import AddTeam
from views.add_arena import AddArena
from views.login import LoginView
from views.register import RegisterView



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^matchs', MatchList.as_view(), name='match_list'),
    url(r'^teams', TeamList.as_view(), name='team_list'),
    url(r'^team/([0-9]+)', Team.as_view(), name='team_info'),
    url(r'^players/', PlayerList.as_view(), name='player_list'),
    url(r'^player/([0-9]+)', Player.as_view(), name='player_info'),
    url(r'^match/([0-9]+)', MatchInfo.as_view(), name='match_info'),
    url(r'^player/add', AddPlayer.as_view(), name='add_player'),
    url(r'^team/add/', TeamEdit.as_view(), name='add_team'),
    url(r'^arena/add/', ArenaEdit.as_view(), name='add_arena'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^register', RegisterView.as_view(), name='register'),

]
