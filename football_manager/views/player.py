from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset


class Player(View):

    template_name = 'player.html'

    def get(self, request, *args, **kwargs):

        try:
            id = args[0]

            conn = cx_Oracle.connect(dbset.URL)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TABLE(api.get_player_info({}))".format(id))

            info = cursor.fetchone()

            cursor.execute("SELECT api.count_player_goals({}) FROM DUAL".format(id))

            goals = cursor.fetchone()[0]

            cursor.execute("SELECT * FROM TABLE(api.get_player_matchs({}))".format(id))

            matchs = []
            rows = cursor.fetchall()
            for row in rows:
                matchs.append( {
                                    "home" : row[1],
                                    "guest" : row[2],
                                    "id" : row[0]
                                })

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


        return render(request, self.template_name, {
                                                        "first_name" : info[2],
                                                        "last_name" : info[3],
                                                        "team_id" : info[1],
                                                        "team_name" : info[4],
                                                        "goals" : goals,
                                                        "matchs" : matchs
                                                    })

    def post(self, request):
        pass
