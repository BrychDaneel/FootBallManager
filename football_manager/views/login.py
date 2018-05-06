from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.login_form import LoginForm
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


class LoginView(View):

    template_name = 'login.html'
    success_url = reverse_lazy("team_list")

    def get(self, request):

        login_form = LoginForm()
        return render(request, self.template_name, {"form":login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)

        if not login_form.is_valid():
            return render(request, self.template_name, {"form":login_form})


        login = login_form.cleaned_data['username']

        conn = cx_Oracle.connect(dbset.URL)

        cursor = conn.cursor()

        cursor.execute("SELECT api.get_user_id('{}') FROM DUAL".format(login))
        id = cursor.fetchone()[0]

        cursor.execute("SELECT api.is_admin('{}') FROM DUAL".format(login))
        is_admin = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        request.session['user_id'] = id
        request.session['is_admin'] = is_admin
        request.session['username'] = login

        return redirect(self.success_url)
