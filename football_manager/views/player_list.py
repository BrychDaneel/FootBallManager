from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset


class PlayerList(View):

    template_name = 'player_list.html'

    def get(self, request):

        try:
            conn = cx_Oracle.connect(dbset.URL)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TABLE(api.get_player_list)")

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
