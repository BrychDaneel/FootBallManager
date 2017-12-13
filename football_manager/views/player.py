from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class Player(View):

    template_name = 'player.html'

    def get(self, request, *args, **kwargs):

        try:
            id = args[0]

            conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
            cursor = conn.cursor()
            cursor.execute("""SELECT pi.first_name, pi.last_name, tm.id, tm.name FROM players as pl
                              LEFT JOIN teams as tm ON tm.id = pl.team
                              INNER JOIN personal_info as pi ON pi.id = pl.personal_info
                              WHERE pl.id = {}""".format(id))

            info = cursor.fetchone()

            cursor.execute("""SELECT COUNT(*) FROM goals as gl
                              INNER JOIN players as pl ON pl.id = gl.player
                              WHERE pl.id = {}""".format(id))

            goals = cursor.fetchone()[0]

            cursor.execute("""SELECT ht.name, gt.name, mt.id
                              FROM players as pl
                              LEFT JOIN team_state as ts ON ts.playerId = pl.id
                              INNER JOIN matchs as mt ON ts.matchId = mt.id
                              INNER JOIN teams as ht ON ht.id = mt.home_team
                              INNER JOIN teams as gt ON gt.id = mt.guest_team
                              WHERE pl.id = {}""".format(id))

            matchs = []
            rows = cursor.fetchall()
            for row in rows:
                matchs.append( {
                                    "home" : row[0],
                                    "guest" : row[1],
                                    "id" : row[2]
                                })

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


        return render(request, self.template_name, {
                                                        "first_name" : info[0],
                                                        "last_name" : info[1],
                                                        "team_id" : info[2],
                                                        "team_name" : info[3],
                                                        "goals" : goals,
                                                        "matchs" : matchs
                                                    })

    def post(self, request):
        pass
