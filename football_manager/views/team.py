from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset




class Team(View):
    template_name = "team.html"

    def get(self, request, *args, **kwargs):

        try:
            id = args[0]

            conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
            cursor = conn.cursor()
            cursor.execute("""SELECT tm.name, st.name, ct.name, em.image FROM teams as tm
                              INNER JOIN sitys as st ON tm.city = st.id
                              INNER JOIN countrys as ct ON ct.id = st.country
                              INNER JOIN emblems as em ON em.id = tm.emblem
                              WHERE tm.id = {}""".format(id))

            info = cursor.fetchone()

            cursor.execute("""SELECT pl.id, pi.first_name, pi.last_name FROM players as pl
                              INNER JOIN personal_info as pi ON pi.id = pl.personal_info
                              WHERE pl.team = {}""".format(id))

            players = []
            rows = cursor.fetchall()
            for row in rows:
                players.append( {
                                    "id" : row[0],
                                    "first_name" : row[1],
                                    "last_name" : row[2],
                                })

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


        return render(request, self.template_name, {"name" : info[0],
            "city": info[1], "country": info[2], "players":players,  "emblem" : info[3]})

    def post(self, request):
        pass
