from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext

import mysql.connector
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect



class RemoveGoal(View):

    template_name = "d.html"

    def get(self, request, id):

        return render(request, self.template_name)

    def post(self, request, id):
        pass
