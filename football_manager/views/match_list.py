from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class MatchList(View):

    template_name = 'match_list.html'

    def get(self, request):
        
        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT home.name, guest.name,

                (SELECT COUNT(*) FROM goals as gl
                INNER JOIN team_state as ts ON gl.player = ts.playerId
                WHERE gl.match = mt.id 
                AND ts.playHomeTeam = 1), 
    
                (SELECT COUNT(*) FROM goals as gl
                INNER JOIN team_state as ts ON gl.player = ts.playerId
                WHERE gl.match = mt.id 
                AND ts.playHomeTeam = 0),
                
                mt.id,
                home.id,
                guest.id
                
            FROM matchs as mt
            INNER JOIN teams as home ON home.id = mt.home_team
            INNER JOIN teams as guest ON guest.id = mt.guest_team""")

        matchs = []
        for m in cursor.fetchall():
            matchs.append({
                            'name1' : m[0],
                            'name2' : m[1],
                            'score1' : m[2],
                            'score2' : m[3],
                            'id' : m[4],
                            'teamid1' : m[5],
                            'teamid2' : m[6],
                            })
        
        cursor.close()
        conn.close()

        return render(request, self.template_name, { 'matchs' : matchs})

    def post(self, request):
        pass
