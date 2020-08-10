from django import forms

from app.models import Review
CHOICES = [(1, 'Кол'), (2, 'Пара'), (3, 'Тройбан'), (4, 'Чепыре'), (5, 'Отл.')]


class LoginForm(forms.Form):
    user_login = forms.CharField(label='Логин', max_length=100)
    user_password = forms.CharField(label='Пароль', max_length=10, widget=forms.PasswordInput())


class ReviewForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(widget=forms.RadioSelect(choices=CHOICES))

    name.widget.attrs.update({'class': 'form-control'})
    text.widget.attrs.update({'class': 'form-control'})
