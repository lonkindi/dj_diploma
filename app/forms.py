from django import forms

class LoginForm(forms.Form):
    user_login = forms.CharField(label='Логин', max_length=100)
    user_password = forms.CharField(label='Пароль', max_length=10, widget=forms.PasswordInput())