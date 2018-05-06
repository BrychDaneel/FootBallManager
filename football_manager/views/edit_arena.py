from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.arena_form import ArenaForm
import cx_Oracle
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

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT name, sity, country
               FROM TABLE(api.get_arena_info({}))"""
            .format(id)
        )
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

        conn = cx_Oracle.connect(dbset.URL)
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

        cursor.execute("""BEGIN api.edit_arena({}, '{}', '{}', '{}'); END;"""
                          .format(id, name, city, county))

        cursor.close()
        conn.commit()
        conn.close()
        return redirect(self.success_url)
