from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.goal_form import GoalForm
import mysql.connector
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect



class AddGoal(View):

    template_name = 'add_goal.html'

    def get(self, request):

        goal_form = GoalForm([(1,"Nigga"),(2,"White")])
        return render(request, self.template_name, {"form": goal_form})

    def post(self, request):
        pass
