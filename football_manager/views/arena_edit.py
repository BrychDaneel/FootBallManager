from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.arena_form import ArenaForm

class ArenaEdit(View):

    template_name = 'arena_edit.html'

    def get(self, request):

        arena_form = ArenaForm()

        return render(request, self.template_name, {"form":arena_form,
                                                    "type" : 1})

    def post(self, request):
        pass
