from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


class LogView(View):

    template_name = 'log_view.html'
    not_admin_url = reverse_lazy("login")

    def get(self, request):

        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)


        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute("""SELECT user_id, time, user_name, text
                          FROM TABLE(api.get_log_list)""")

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
