from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset


class UserList(View):

    template_name = 'user_list.html'

    def get(self, request):


        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()

        cursor.execute("SELECT id, login FROM TABLE(api.get_user_list)")

        ars = cursor.fetchall()

        users = []
        for a in ars:
            users.append({
                            'name' : a[1],
                            'id' : a[0],
                            })

        cursor.close()
        conn.close()

        return render(request, self.template_name, { 'users' : users})


    def post(self, request):
        pass
