from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class UserList(View):

    template_name = 'user_list.html'

    def get(self, request):

        return render(request, self.template_name, { 'users' : [
        {"id" : 1, "name" : "Nigga1"}, {"id" : 2, "name" : "Nigga2"},
        {"id" : 3, "name" : "Nigga3"}
    ]})


    def post(self, request):
        pass
