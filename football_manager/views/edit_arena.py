from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.arena_form import ArenaForm
import mysql.connector
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404


class EditArena(View):

    template_name = 'edit_arena.html'
    success_url = reverse_lazy("team_list")
    not_admin_url = reverse_lazy("login")

    def get(self, request, id):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
        cursor = conn.cursor()

        cursor.execute("""SELECT ar.name, st.name, ct.name
                          FROM arena as ar
                          INNER JOIN sitys as st ON st.id = ar.sity
                          INNER JOIN countrys as ct ON ct.id = st.country
                          WHERE ar.id = {}
                          """.format(id))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            raise Http404

        arena_form = ArenaForm({
                                'arena_name' : rows[0][0],
                                'country' : rows[0][1],
                                'city' : rows[0][2]
                                })
        return render(request, self.template_name, {"form":arena_form})

    def post(self, request, id):

        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
        cursor = conn.cursor()


        cursor.execute(" SELECT COUNT(*) FROM arena WHERE id = {} ".format(id))

        if not cursor.fetchall():
            raise Http404

        arena_form = ArenaForm(request.POST)
        if not arena_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":arena_form})




        county = arena_form.cleaned_data['country']
        name = arena_form.cleaned_data['arena_name']
        city = arena_form.cleaned_data['city']

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

        cursor.execute("""UPDATE arena
                          SET name = "{1}", sity = {2}
                          WHERE id = {0}"""
                          .format(id, name, city_id))

        cursor.close()
        conn.commit()
        conn.close()
        return redirect(self.success_url)
