from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext

import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect



class RemovePlayer(View):

    template_name = "d.html"
    not_admin_url = reverse_lazy("login")

    def get(self, request, id):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        try:
            conn = cx_Oracle.connect(dbset.URL)
            cursor = conn.cursor()

            cursor.execute("""BEGIN api.delete_player({}); END;""".format(id))
            cursor.close()
            conn.commit()
            conn.close()
        except:
            return render(request, 'error.html')


        return redirect('player_list')

    def post(self, request, id):
        pass
