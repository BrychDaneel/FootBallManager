from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.login_form import LoginForm

class LoginView(View):

    template_name = 'login.html'

    def get(self, request):

        login_form = LoginForm()

        return render(request, self.template_name, {"form":login_form,
                                                        })

    def post(self, request):
        pass
