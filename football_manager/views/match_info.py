from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset

class MatchInfo(View):

    template_name = 'match_info.html'

    def get(self, request, *args, **kwargs):


        id = args[0]

        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT home.name, guest.name, hc.name, gc.name,  

                (SELECT COUNT(*) FROM goals as gl
                INNER JOIN team_state as ts ON gl.player = ts.playerId
                WHERE gl.match = mt.id 
                AND ts.playHomeTeam = 1), 
    
                (SELECT COUNT(*) FROM goals as gl
                INNER JOIN team_state as ts ON gl.player = ts.playerId
                WHERE gl.match = mt.id 
                AND ts.playHomeTeam = 0),
                
                em1.image, em2.image
                
            FROM matchs as mt
            INNER JOIN teams as home ON home.id = mt.home_team
            INNER JOIN teams as guest ON guest.id = mt.guest_team
            INNER JOIN sitys as hs ON hs.id = home.city
            INNER JOIN sitys as gs ON gs.id = guest.city
            INNER JOIN countrys as hc ON hs.country = hc.id
            INNER JOIN countrys as gc ON gs.country = gc.id
            INNER JOIN emblems as em1 ON em1.id = home.emblem
            INNER JOIN emblems as em2 ON em2.id = guest.emblem
            WHERE mt.id = {}""".format(id))

        info = cursor.fetchone()

        cursor.execute("""SELECT ts.playHomeTeam, gl.time, pi.first_name, pi.last_name, gl.id
                          FROM goals as gl
                          INNER JOIN matchs as mt ON mt.id = gl.match
                          INNER JOIN players as pl ON pl.id = gl.player
                          INNER JOIN personal_info as pi ON pi.id = pl.personal_info
                          INNER JOIN team_state as ts
                                ON ts.matchId = mt.id AND ts.playerId = pl.id
                          WHERE mt.id = {}
                          ORDER BY gl.time""".format(id))

        goals = cursor.fetchall()

        cursor.execute("""SELECT ts.playHomeTeam, cr.time, ct.color, pi.first_name, pi.last_name, cr.id
                          FROM cards as cr
                          INNER JOIN matchs as mt ON mt.id = cr.match
                          INNER JOIN players as pl ON pl.id = cr.player
                          INNER JOIN personal_info as pi ON pi.id = pl.personal_info
                          INNER JOIN card_types as ct ON ct.id = cr.type
                          INNER JOIN team_state as ts
                                ON ts.matchId = mt.id AND ts.playerId = pl.id
                          WHERE mt.id = {}
                          ORDER BY cr.time""".format(id))

        cards = cursor.fetchall()

        cursor.close()
        conn.close()

        goals = [
                    {
                        'is_home' : g[0],
                        'time' : (int(g[1].total_seconds()) + 59) // 60,
                        'player_name' : g[2],
                        'player_last_name' : g[3],
                        'id' : g[4]
                    }
                    for g in goals
                ]

        cards = [
                    {
                        'is_home' : c[0],
                        'time' : (int(c[1].total_seconds()) + 59) // 60,
                        'color' : c[2],
                        'player_name' : c[3],
                        'player_last_name' : c[4],
                        'id' : c[5]
                    }
                    for c in cards
                ]

        context = {
                    'match_id' : id,
                    'goals' : goals,
                    'cards' : cards,
                    'team1' : info[0],
                    'team2' : info[1],
                    'country1' : info[2],
                    'country2' : info[3],
                    'score1' : info[4],
                    'score2' : info[5],
                    'logo1' : info[6],
                    'logo2' : info[7],
                  }
        return render(request, self.template_name, context)

    def post(self, request):
        pass
