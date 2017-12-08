from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext

class PlayerList(View):

    template_name = 'player_list.html'

    def get(self, request):


        return render(request, self.template_name, { 'teams' : [1,2,3]})

    def post(self, request):
        pass
