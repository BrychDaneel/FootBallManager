from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
from forms.player_form import PlayerForm

class EditPlayer(View):

    template_name = 'edit_player.html'

    def get(self, request):

        player_form = PlayerForm([(1,"Bayern"),(2,"Real"), (3,"PSG")],
                                 [(1,"Forward"),(2,"Midfielder"),
                                  (3,"Вefender"),(4,"Goalkeeper")]);

        return render(request, self.template_name, {"form":player_form,
                                                    "type" : 1})

    def post(self, request):
        pass
