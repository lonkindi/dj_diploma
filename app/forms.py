from django import forms

class LoginForm(forms.Form):
    user_login = forms.CharField(label='Логин', max_length=100)
    user_password = forms.CharField(label='Пароль', max_length=10, widget=forms.PasswordInput())

class ReviewForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    rating = forms.RadioSelect(choices=(1, 2, 3, 4, 5))
    # rating = forms.ChoiceField(choices=(1, 2, 3, 4, 5), widget=forms.RadioSelect)

    name.widget.attrs.update({'class': 'form-control'})
    text.widget.attrs.update({'class': 'form-control'})

