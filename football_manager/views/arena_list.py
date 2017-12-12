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
        cursor = conn.cursor()
        
        cursor.execute("""SELECT ar.id, ar.name, st.name, ct.name
                            FROM arena as ar
                            INNER JOIN sitys as st ON st.id = ar.sity
                            INNER JOIN countrys as ct ON ct.id = st.country""")
        
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
