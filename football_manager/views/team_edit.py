from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.team_form import TeamForm

class TeamEdit(View):

    template_name = 'team_edit.html'

    def get(self, request):

        team_form = TeamForm();

        return render(request, self.template_name, {"form":team_form,
                                                    "type" : 1})

    def post(self, request):
        pass
