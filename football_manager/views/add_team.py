from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.team_form import TeamForm
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
import os
from PIL import Image
import io
from views.log import log


class AddTeam(View):

    template_name = 'add_team.html'
    success_url = reverse_lazy("team_list")
    static_path = 'static'
    not_admin_url = reverse_lazy("login")


    def get(self, request):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        team_form = TeamForm()

        return render(request, self.template_name, {"form":team_form})

    def post(self, request):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        team_form = TeamForm(request.POST, request.FILES)

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()

        if not team_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":team_form})

        files = os.listdir('static/emblems')
        pid = max([int(f.split('.')[0]) for f in files] + [0]) + 1
        pname = 'emblems/{}.png'.format(pid)
        full_pname = '{}/{}'.format(self.static_path, pname)

        image = Image.open(io.BytesIO(team_form.cleaned_data['emblem'].read()))

        name = team_form.cleaned_data['team_name']


        county = team_form .cleaned_data['country']
        city = team_form .cleaned_data['city']

        cursor.execute(
            """BEGIN api.add_team('{}', '{}', '{}', '{}'); END;"""
            .format(name, city, county, pname)
        )

        log(conn, request.session['user_id'], "Add team {}".format(name))

        cursor.close()
        conn.commit()
        conn.close()

        image.save(full_pname)

        return redirect(self.success_url)
