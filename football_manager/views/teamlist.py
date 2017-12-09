from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class TeamList(View):
    template_name = "teamlist.html"

    def get(self, request):

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
            cursor = conn.cursor()
            cursor.execute("SELECT name, emblem, id FROM teams")

            teams = []
            rows = cursor.fetchall()

            for row in rows:
                teams.append( { "name" : row[0], "eblem" : row[1],
                               "id" : row[2]})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render(request, self.template_name, { 'teams' : teams})

    def post(self, request):
        pass
