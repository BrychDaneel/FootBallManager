from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.team_form import TeamForm
import mysql.connector
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


        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()


        cursor.execute("""SELECT tm.name, st.name, ct.name
                          FROM teams as tm
                          INNER JOIN sitys as st ON st.id = tm.city
                          INNER JOIN countrys as ct ON ct.id = st.country
                          WHERE tm.id = {}
                          """.format(id))

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

        conn = mysql.connector.connect(host=dbset.HOST,
                            database=dbset.DATABASE,
                            user=dbset.USER,
                            password=dbset.PASSWORD)
        cursor = conn.cursor()

        cursor.execute("""SELECT em.id, em.image
                          FROM teams as tm
                          LEFT JOIN emblems as em ON tm.emblem = em.id
                          WHERE tm.id = {}
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


        cursor.execute("""INSERT INTO emblems(image) VALUES ("{}")""".format(pname))
        cursor.execute("""SELECT id FROM emblems WHERE image = "{}" """.format(pname))

        emblem = cursor.fetchone()[0]

        name = team_form.cleaned_data['team_name']


        county = team_form .cleaned_data['country']
        city = team_form .cleaned_data['city']

        cursor.execute('SELECT id FROM countrys WHERE name = "{}"'.format(county))

        rows = cursor.fetchall()

        if not rows:
            cursor.execute('INSERT INTO countrys(name) VALUES ("{}")'.format(county))
            cursor.execute('SELECT id FROM countrys WHERE name = "{}"'.format(county))
            rows = cursor.fetchall()

        county_id = rows[0][0]


        cursor.execute('SELECT id FROM sitys WHERE name = "{}"'.format(city))
        rows = cursor.fetchall()

        if not rows:
            cursor.execute('INSERT INTO sitys(name, country) VALUES ("{}", {})'.format(city, county_id))
            cursor.execute('SELECT id FROM sitys WHERE name = "{}"'.format(city))
            rows = cursor.fetchall()

        city_id = rows[0][0]


        cursor.execute("""UPDATE teams SET
                            name = "{1}",
                            city = {2},
                            emblem = {3}
                        WHERE id = {0}"""
                       .format(id, name, city_id, emblem))

        if old_emblem:
            cursor.execute("DELETE FROM emblems WHERE id = {}".format(old_emblem))

        cursor.close()
        conn.commit()
        conn.close()

        image.save(full_pname)
        if old_emblem:
            os.remove(os.path.join(self.static_path, os.path.join(old_image)))

        return redirect(self.success_url)
