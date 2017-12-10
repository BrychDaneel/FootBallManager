from django import forms
import mysql.connector
import football_manager.db_settings as dbset

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        data = self.cleaned_data

        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM users
                          WHERE login = "{}" AND password = "{}"
                          """.format(data['username'], data['password']))

        ok = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if ok:
            return data

        raise forms.ValidationError("User not found or invalid password.")
