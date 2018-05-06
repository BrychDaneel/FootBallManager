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


class EditTeam(View):

    template_name = 'edit_team.html'
    success_url = reverse_lazy("team_list")
    static_path = 'static'
    not_admin_url = reverse_lazy("login")

    def get(self, request, id):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)


        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()


        cursor.execute(
            """SELECT name, sity, country
            FROM TABLE(api.get_team_info({}))"""
            .format(id)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            raise Http404

        team_form = TeamForm({
                                'team_name' : rows[0][0],
                                'city' : rows[0][1],
                                'country' : rows[0][2],
                            })

        return render(request, self.template_name, {"form":team_form})

    def post(self, request, id):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()

        cursor.execute("""SELECT id, image
                          FROM TABLE(api.get_team_emblem({}))
                          """.format(id))

        rows = cursor.fetchall()
        if not rows:
            raise Http404

        old_emblem = rows[0][0]
        old_image = rows[0][1]

        team_form = TeamForm(request.POST, request.FILES)

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
        country = team_form .cleaned_data['country']
        city = team_form .cleaned_data['city']

        cursor.execute("BEGIN api.edit_team({}, '{}', '{}', '{}', '{}'); END;"
                        .format(id, name, city, country, pname))

        if old_emblem:
            cursor.execute("BEGIN api.delete_emblem({}); END;".format(old_emblem))

        cursor.close()
        conn.commit()
        conn.close()

        image.save(full_pname)
        if old_emblem:
            os.remove(os.path.join(self.static_path, os.path.join(old_image)))

        return redirect(self.success_url)
