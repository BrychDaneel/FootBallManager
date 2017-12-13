from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


class LogView(View):

    template_name = 'log_view.html'
    not_admin_url = reverse_lazy("login")

    def get(self, request):

        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)
        

        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT us.id, log.time, us.login, log.`text`
                          FROM changes as log
                          INNER JOIN users as us ON us.id = log.admin
                          ORDER BY log.time""")

        logs = []
        rows = cursor.fetchall()
        for row in rows:
            logs.append( {
                                "id" : row[0],
                                "name" : row[2],
                                "time" : row[1],
                                "text" : row[3],
                            })

        cursor.close()
        conn.close()
        return render(request, self.template_name, {"logs": logs })

    def post(self, request):
        pass

