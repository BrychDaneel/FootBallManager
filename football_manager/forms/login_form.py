from django import forms
import cx_Oracle
import football_manager.db_settings as dbset

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        data = self.cleaned_data

        conn = cx_Oracle.connect(dbset.URL)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT api.authificate('{}', '{}') FROM DUAL"
            .format(data['username'], data['password'])
        )

        ok = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if ok:
            return data

        raise forms.ValidationError("User not found or invalid password.")
