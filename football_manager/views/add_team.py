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


class AddTeam(View):

    template_name = 'add_team.html'
    success_url = reverse_lazy("team_list")
    static_path = 'static'

    def get(self, request):

        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT ar.id, ar.name, st.name
                          FROM arena as ar
                          INNER JOIN sitys as st ON ar.sity = st.id""")

        arenas = [(r[0], "{}({})".format(r[1], r[2])) for r in cursor.fetchall()]

        cursor.close()
        conn.close()

        team_form = TeamForm(arenas)

        return render(request, self.template_name, {"form":team_form})

    def post(self, request):
        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT ar.id, ar.name, st.name
                          FROM arena as ar
                          INNER JOIN sitys as st ON ar.sity = st.id""")

        arenas = [(r[0], "{}({})".format(r[1], r[2])) for r in cursor.fetchall()]

        team_form = TeamForm(arenas, request.POST, request.FILES)

        if not team_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":team_form})

        files = os.listdir('static/emblems')
        pid = max([int(f.split('.')[0]) for f in files] + [0]) + 1
        pname = 'emblems/{}.png'.format(pid)
        full_pname = '{}/{}'.format(self.static_path, pname)

        image = Image.open(io.BytesIO(team_form.cleaned_data['emblem'].read()))
        image.save(full_pname)

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


        cursor.execute('INSERT INTO teams(name, city, emblem) VALUES ("{}", {}, {})'
                       .format(name, city_id, emblem))

        cursor.close()
        conn.commit()
        conn.close()
        return redirect(self.success_url)
