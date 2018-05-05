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
        cursor.execute("SELECT * FROM TABLE(api.get_match_list)")

        matchs = []
        for m in cursor.fetchall():
            matchs.append({
                            'id' : m[0],
                            'name1' : m[1],
                            'name2' : m[2],
                            'teamid1' : m[3],
                            'teamid2' : m[4],
                            'score1' : m[7],
                            'score2' : m[8],
                            })

        cursor.close()
        conn.close()

        return render(request, self.template_name, { 'matchs' : matchs})

    def post(self, request):
        pass
