from django import forms

from app.models import Review

CHOICES = [(1, 'Кол'), (2, 'Пара'), (3, 'Тройбан'), (4, 'Чепыре'), (5, 'Отл.')]


class LoginForm(forms.Form):
    user_login = forms.CharField(label='Логин или e-mail', max_length=50)
    user_password = forms.CharField(label='Пароль', max_length=10, widget=forms.PasswordInput())

    user_login.widget.attrs.update({'class': 'form-control'})
    user_password.widget.attrs.update({'class': 'form-control'})


class ReviewForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(widget=forms.RadioSelect(choices=CHOICES))

    name.widget.attrs.update({'class': 'form-control'})
    text.widget.attrs.update({'class': 'form-control'})
