from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset


class ArenaList(View):

    template_name = 'arena_list.html'

    def get(self, request):


        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM TABLE(api.get_arena_list)")

        ars = cursor.fetchall()

        arenas = []
        for a in ars:
            arenas.append({
                            'name' : a[1],
                            'city' : a[2],
                            'country' : a[3],
                            'id' : a[0],
                            })

        cursor.close()
        conn.close()

        return render(request, self.template_name, {"arenas": arenas})

    def post(self, request):
        pass
