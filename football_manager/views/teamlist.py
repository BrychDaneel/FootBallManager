from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext




class TeamList(View):
    template_name = "teamlist.html"

    def get(self, request):

        teams = [];
        teams.append( { "name" : "Bayern Munich", "eblem" : "B"})
        teams.append( { "name" : "Real Madrid", "eblem" : "R"})
        teams.append( { "name" : "PSG", "eblem" : "P"})
        teams.append( { "name" : "Manchester United", "eblem" : "MU"})
        teams.append( { "name" : "Chelsea", "eblem" : "C"})
        return render(request, self.template_name, { 'teams' : teams})

    def post(self, request):
        pass
