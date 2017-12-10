from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.player_form import PlayerForm
import mysql.connector
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404


class EditPlayer(View):

    template_name = 'edit_player.html'
    player_form = None
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
        cursor.execute('SELECT id, name FROM teams')
        teams = cursor.fetchall()
        cursor.execute('SELECT id, name FROM team_roles')
        roles = cursor.fetchall()

        cursor.execute("""SELECT pi.first_name, pi.last_name, pi.birthday,
                          pl.team, pl.role, pl.number
                          FROM players as pl
                          INNER JOIN personal_info as pi ON pi.id = pl.personal_info
                          WHERE pl.id = {}
                          """.format(id))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            raise Http404

        self.player_form = PlayerForm(teams, roles, {
                                                        'first_name' : rows[0][0],
                                                        'last_name' : rows[0][1],
                                                        'date' : rows[0][2],
                                                        'number' : rows[0][5],
                                                        'role' : rows[0][4],
                                                        'team' : rows[0][3]
                                                     })
        return render(request, self.template_name, {"form":self.player_form})

    def post(self, request, id):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)


        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM players WHERE id = {}".format(id))

        if not cursor.fetchone()[0]:
            cursor.close()
            conn.close()
            raise Http404


        cursor.execute('SELECT id, name FROM teams')
        teams = cursor.fetchall()
        cursor.execute('SELECT id, name FROM team_roles')
        roles = cursor.fetchall()


        self.player_form = PlayerForm(teams, roles, request.POST)

        if not self.player_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":self.player_form})


        first_name = self.player_form.cleaned_data['first_name']
        last_name = self.player_form.cleaned_data['last_name']
        date = self.player_form.cleaned_data['date'].isoformat()
        team = self.player_form.cleaned_data['team']
        role = self.player_form.cleaned_data['role']
        number = self.player_form.cleaned_data['number']

        cursor.execute("""UPDATE players as pl
                          INNER JOIN personal_info as pi ON pl.personal_info = pi.id
                          SET
                                pi.first_name = "{1}",
                                pi.last_name = "{2}",
                                pi.birthday = "{3}",
                                pl.team = {4},
                                pl.role = {5},
                                pl.number = {6}
                          WHERE pl.id = {0}
                       """.format(id, first_name, last_name, date, team, role, number))


        cursor.close()
        conn.commit()
        conn.close()

        return redirect(self.success_url)
