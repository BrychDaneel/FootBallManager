from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.foul_form import FoulForm
import mysql.connector
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect



class AddFoul(View):

    template_name = 'add_foul.html'

    def get(self, request):

        foul_form = FoulForm(["Yelow","Red"],[(1,"Nigga"),
                                               (2,"White")])
        return render(request, self.template_name, {"form":foul_form})

    def post(self, request):
        pass
