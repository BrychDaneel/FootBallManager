from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset


class TeamList(View):
    template_name = "teamlist.html"

    def get(self, request):

        conn = None
        cursor = None
        try:
            conn = cx_Oracle.connect(dbset.URL)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TABLE(api.get_team_list)")

            teams = []
            rows = cursor.fetchall()

            for row in rows:
                teams.append( { "name" : row[1], "eblem" : row[4],
                               "id" : row[0]})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render(request, self.template_name, { 'teams' : teams})

    def post(self, request):
        pass
