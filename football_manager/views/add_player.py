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
from views.log import log



class AddPlayer(View):

    template_name = 'add_player.html'
    player_form = None
    success_url = reverse_lazy("team_list")
    not_admin_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):

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
        cursor.close()
        conn.close()

        self.player_form = PlayerForm(teams, roles);
        return render(request, self.template_name, {"form":self.player_form})

    def post(self, request):

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


        self.player_form = PlayerForm(teams, roles, request.POST)

        if not self.player_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":self.player_form})


        first_name = self.player_form.cleaned_data['first_name']
        last_name = self.player_form.cleaned_data['last_name']
        date = self.player_form.cleaned_data['date'].isoformat()

        cursor.execute("""INSERT INTO personal_info(first_name, last_name, birthday) VALUES
                          ("{}", "{}", "{}")""".format(first_name, last_name, date))


        team = self.player_form.cleaned_data['team']
        role = self.player_form.cleaned_data['role']
        number = self.player_form.cleaned_data['number']

        cursor.execute(
                        """INSERT INTO players(personal_info, team, `number`, role) VALUES
                           ((SELECT MAX(id) FROM personal_info), {}, {}, {})
                        """.format(team, number, role)
                      )
        
        log(conn, request.session['user_id'], "Add foul at {}".format(minute))

        cursor.close()
        conn.commit()
        conn.close()

        return redirect(AddPlayer.success_url)
