from django import forms
import mysql.connector
import football_manager.db_settings as dbset



class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    password_again = forms.CharField()


    def clean(self):
        data = self.cleaned_data

        conn = mysql.connector.connect(host=dbset.HOST,
                                    database=dbset.DATABASE,
                                    user=dbset.USER,
                                    password=dbset.PASSWORD)
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM users
                          WHERE login = "{}"
                          """.format(data['username']))

        if (cursor.fetchone()[0]):
            cursor.close()
            conn.close()
            raise forms.ValidationError("User allready exist")

        cursor.close()
        conn.close()

        if data['password'] != data['password_again']:
            raise forms.ValidationError("Passwords don't match")

        return data
