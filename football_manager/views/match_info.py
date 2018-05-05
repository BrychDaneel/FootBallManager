from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset

class MatchInfo(View):

    template_name = 'match_info.html'

    def get(self, request, *args, **kwargs):


        id = args[0]

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TABLE(api.get_match_info({}))".format(id))

        info = cursor.fetchone()
        print(info)

        cursor.execute("SELECT * FROM TABLE(api.get_goals({}))".format(id))
        goals = cursor.fetchall()

        cursor.execute("SELECT * FROM TABLE(api.get_cards({}))".format(id))
        cards = cursor.fetchall()

        cursor.close()
        conn.close()

        goals = [
                    {
                        'is_home' : g[0],
                        'time' : (
                            int(
                            g[1].second + (g[1].minute + g[1].hour * 60) * 60
                            ) + 59) // 60,
                        'player_name' : g[2],
                        'player_last_name' : g[3],
                        'id' : g[4]
                    }
                    for g in goals
                ]

        cards = [
                    {
                        'is_home' : c[0],
                        'time' : (
                            int(
                            c[1].second + (c[1].minute + c[1].hour * 60) * 60
                            ) + 59) // 60,
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
                    'team1' : info[1],
                    'team2' : info[2],
                    'country1' : info[5],
                    'country2' : info[6],
                    'score1' : info[7],
                    'score2' : info[8],
                    'logo1' : info[9],
                    'logo2' : info[10],
                  }
        return render(request, self.template_name, context)

    def post(self, request):
        pass
