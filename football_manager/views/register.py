from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.register_form import RegisterForm

class RegisterView(View):

    template_name = 'register.html'

    def get(self, request):

        register_form = RegisterForm()

        return render(request, self.template_name, {"form":register_form,
                                                        })

    def post(self, request):
        pass
