from django import forms
import cx_Oracle
import football_manager.db_settings as dbset



class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    password_again = forms.CharField()


    def clean(self):
        data = self.cleaned_data

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT api.user_exists('{}') FROM DUAL"
            .format(data['username'])
        )

        if (cursor.fetchone()[0]):
            cursor.close()
            conn.close()
            raise forms.ValidationError("User allready exist")

        cursor.close()
        conn.close()

        if data['password'] != data['password_again']:
            raise forms.ValidationError("Passwords don't match")

        return data
