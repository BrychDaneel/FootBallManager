from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.register_form import RegisterForm
import cx_Oracle
import football_manager.db_settings as dbset
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


class RegisterView(View):

    template_name = 'register.html'
    success_url = reverse_lazy("team_list")

    def get(self, request):

        register_form = RegisterForm()

        return render(request, self.template_name, {"form":register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if not register_form.is_valid():
            return render(request, self.template_name, {"form":register_form})

        password = register_form.cleaned_data['password']
        if password != register_form.cleaned_data['password_again']:
            return render(request, self.template_name, {"form":register_form})

        login = register_form.cleaned_data['username']

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute("BEGIN api.register('{}','{}'); END;"
                        .format(login, password))
        cursor.close()
        conn.commit()
        conn.close()
        return redirect(self.success_url)
