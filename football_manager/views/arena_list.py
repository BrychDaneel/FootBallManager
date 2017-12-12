from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class ArenaList(View):

    template_name = 'arena_list.html'

    def get(self, request):


        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)


        return render(request, self.template_name, {"arenas": [{"name":"1",
                                                                "city":"2",
                                                                "country":"3",
                                                                "id": 1}]})

    def post(self, request):
        pass
