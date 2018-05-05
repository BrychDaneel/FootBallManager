from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.goal_form import GoalForm
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from views.log import log



class AddGoal(View):

    template_name = 'add_goal.html'
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
        cursor.close()
        conn.close()
        goal_form = GoalForm(players)
        return render(request, self.template_name, {"form": goal_form})

    def post(self, request, match):
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

        goal_form = GoalForm(players, request.POST)

        if not goal_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form": goal_form})

        minutes = goal_form.cleaned_data['minute']
        player = goal_form.cleaned_data['player']

        cursor.execute("alter SESSION set NLS_TIMESTAMP_FORMAT = 'hh24:mi:ss'");
        cursor.execute(
            """BEGIN api.add_goal({}, '{}:{}:0', {}); END;"""
            .format(match, minutes // 60, minutes % 60, player)
        )

        log(conn, request.session['user_id'], "Add goal at {} minute to match {}".format(minutes, match))

        cursor.close()
        conn.commit()
        conn.close()
        return redirect(reverse('match_info', args=(match,)))
