from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context, RequestContext
import mysql.connector
import football_manager.db_settings as dbset


class UserList(View):

    template_name = 'user_list.html'

    def get(self, request):
        
        
        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        
        cursor.execute("""SELECT us.id, us.login FROM users as us
                          WHERE 0 = 
                            (SELECT COUNT(*) FROM admins as ad WHERE ad.user = us.id)
                            AND us.hiden = 0""")
        
        ars = cursor.fetchall()
        
        users = []
        for a in ars:
            users.append({
                            'name' : a[1],
                            'id' : a[0],
                            })
        
        cursor.close()
        conn.close()

        return render(request, self.template_name, { 'users' : users})


    def post(self, request):
        pass
