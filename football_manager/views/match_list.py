from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset


class MatchList(View):

    template_name = 'match_list.html'

    def get(self, request):

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TABLE(api.match_list)")

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
