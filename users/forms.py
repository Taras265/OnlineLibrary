from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import Reader

User = get_user_model()


class ReaderRegisterForm(forms.Form):
    username = forms.CharField(label='Нік', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': "Нік"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': "Пароль"}))
    password2 = forms.CharField(label='Пароль ще раз', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': "Пароль ще раз"
               }))

    email = forms.EmailField(label='Пошта', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'placeholder': "Пошта"}))

    reader_card_number = forms.CharField(label='Код читача', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                           'placeholder': "Код читача"}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        card_number = self.cleaned_data.get('reader_card_number')

        if password and password2:
            if password != password2:
                raise ValueError('Паролі не однакові.')
            if not Reader.objects.filter(card_number=card_number).exists():
                raise ValueError('Такого читача немає в базі.')
            if User.objects.filter(username=username).exists():
                raise ValueError('Користувач з таким ніком вже існує.')
            if User.objects.filter(email=email).exists():
                raise ValueError('Користувач з такою поштою вже існує.')
            try:
                validate_password(password)
            except ValidationError:
                raise ValidationError('Пароль заслабкий.')