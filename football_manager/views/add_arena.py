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
from views.log import log


class AddArena(View):

    template_name = 'add_arena.html'
    success_url = reverse_lazy("team_list")
    not_admin_url = reverse_lazy("login")

    def get(self, request):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)
        arena_form = ArenaForm()
        return render(request, self.template_name, {"form":arena_form})

    def post(self, request):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        arena_form = ArenaForm(request.POST)
        if not arena_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":arena_form})


        conn = mysql.connector.connect(host=dbset.HOST,
                                        database=dbset.DATABASE,
                                        user=dbset.USER,
                                        password=dbset.PASSWORD)
        cursor = conn.cursor()

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

        cursor.execute('INSERT INTO arena(name, sity) VALUES ("{}", {})'.format(name, city_id))
        
        log(conn, request.session['user_id'], "Add arena {}".format(name))

        cursor.close()
        conn.commit()
        conn.close()
        return redirect(self.success_url)
