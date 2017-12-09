from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class PlayerList(View):

    template_name = 'player_list.html'

    def get(self, request):

        try:
            conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
            cursor = conn.cursor()
            cursor.execute("""SELECT pl.id, tm.id, pi.first_name, pi.last_name, tm.name
                           FROM players as pl
                           INNER JOIN teams as tm ON pl.team = tm.id
                           INNER JOIN personal_info as pi on pi.id = pl.personal_info""")

            players = []
            rows = cursor.fetchall()
            for row in rows:
                players.append( {
                                    "id" : row[0],
                                    "team_id" : row[1],
                                    "name" : row[2],
                                    "last_name" : row[3],
                                    "team_name" : row[4]
                                })

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render(request, self.template_name, {"players": players})

    def post(self, request):
        pass
