from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset

class Team(View):
    template_name = "team.html"

    def get(self, request, *args, **kwargs):

        try:
            id = args[0]

            conn = cx_Oracle.connect(dbset.URL)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TABLE(api.get_team_info({}))".format(id))

            info = cursor.fetchone()

            cursor.execute("SELECT * FROM TABLE(api.get_team_players({}))".format(id))

            players = []
            rows = cursor.fetchall()
            for row in rows:
                players.append( {
                                    "id" : row[0],
                                    "first_name" : row[2],
                                    "last_name" : row[3],
                                })

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


        return render(request, self.template_name, {"name" : info[1],
            "city": info[2], "country": info[3], "players":players,  "emblem" : info[4]})

    def post(self, request):
        pass
