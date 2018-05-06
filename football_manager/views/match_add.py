from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.match_form import MatchForm
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.shortcuts import redirect



class AddMatch(View):

    template_name = 'match_add.html'
    not_admin_url = reverse_lazy("login")
    success_url = reverse_lazy("team_list")

    def get(self, request):

        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()


        cursor.execute("""SELECT id, name FROM teams""")
        teams = cursor.fetchall()


        cursor.execute("""SELECT id, name FROM arena""")
        arenas = cursor.fetchall()

        cursor.close()
        conn.close()
        match_form = MatchForm(teams, arenas)
        return render(request, self.template_name, {"form":  match_form})

    def post(self, request):
        if not request.session.get('is_admin', False):
            return redirect(self.not_admin_url)

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()


        cursor.execute("""SELECT id, name FROM teams""")
        teams = cursor.fetchall()

        cursor.execute("""SELECT id, name FROM arena""")
        arenas = cursor.fetchall()

        match_form = MatchForm(teams, arenas, request.POST)

        if not match_form.is_valid():
            cursor.close()
            conn.close()
            return render(request, self.template_name, {"form":  match_form})


        home_team = match_form.cleaned_data['home_team']
        guest_team = match_form.cleaned_data['guest_team']
        arena = match_form.cleaned_data['arena']

        cursor.execute(
            "alter SESSION set NLS_DATE_FORMAT = 'yyyy-mm-dd hh24:mi:ss'"
        )
        cursor.execute(
            """BEGIN api.add_match({}, {}, {}, '{}'); END;"""
            .format(home_team, guest_team, arena, "2017-12-9 12:00:00")
        )

        cursor.close()
        conn.commit()
        conn.close()
        return redirect(reverse('match_list'))
