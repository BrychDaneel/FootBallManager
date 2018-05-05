from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.foul_form import FoulForm
from forms.goal_form import GoalForm
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from views.log import log



class AddFoul(View):

    template_name = 'add_foul.html'

    template_name = 'add_foul.html'
    not_admin_url = reverse_lazy("login")
    success_url = reverse_lazy("team_list")

    def get(self, request, match):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM TABLE(api.get_match_info({}))"
            .format(match)
        )

        if not cursor.fetchall():
            cursor.close()
            conn.close()
            raise Http404


        cursor.execute(
            "SELECT id, first_name FROM TABLE(api.get_match_players({}))"
            .format(match)
        )
        players = cursor.fetchall()

        cursor.execute("""SELECT id, color FROM card_types""")

        colors = cursor.fetchall()

        cursor.close()
        conn.close()

        foul_form = FoulForm(colors, players)
        return render(request, self.template_name, {'form' : foul_form})

    def post(self, request, match):


        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()

        cursor.execute(" SELECT COUNT(*) FROM matchs WHERE id = {} ".format(match))


        if not cursor.fetchall():
            cursor.close()
            conn.close()
            raise Http404


        cursor.execute(
            "SELECT * FROM TABLE(api.get_match_info({}))"
            .format(match)
        )
        players = cursor.fetchall()

        cursor.execute("""SELECT id, color FROM card_types""")

        colors = cursor.fetchall()

        foul_form = FoulForm(colors, players, request.POST)

        if not foul_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form": foul_form})


        card = foul_form.cleaned_data['card']
        player = foul_form.cleaned_data['player']
        minute = foul_form.cleaned_data['minute']

        cursor.execute("alter SESSION set NLS_TIMESTAMP_FORMAT = 'hh24:mi:ss';")
        cursor.execute(
            "BEGIN api.add_foul({}, {}, '{}:{}:0', {}); END;"
            .format(card, match, minute // 60, minute % 60, player)
        )

        log(conn, request.session['user_id'], "Add foul at {} minute to match {}".format(minute, match))

        cursor.close()
        conn.commit()
        conn.close()

        return redirect(reverse('match_info', args=(match,)))
