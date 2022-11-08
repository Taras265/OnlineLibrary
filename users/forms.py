from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
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


class EmailValidationForm(forms.Form):
    email_code = forms.CharField(label='Код підтвердження пошти', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': "Код підтвердження пошти"
               }))


class LoginForm(forms.Form):
    username = forms.CharField(label='Нік', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': "Нік"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': "Пароль"}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise ValueError('Нема користувача з таким ніком')
            if not check_password(password, qs[0].password):
                raise ValueError('Пароль не вірен')
            user = authenticate(username=username, password=password)
            if not user:
                raise ValueError('Користувач неактивен')
            return super().clean(*args, **kwargs)


class ReaderForm(forms.ModelForm):
    first_name = forms.CharField(label='Ім\'я', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': "Ім\'я"}))
    second_name = forms.CharField(label='По батькові', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                     'placeholder': "По батькові"}))
    last_name = forms.CharField(label='Фамілія', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                               'placeholder': "Фамілія"}))
    card_number = forms.CharField(label='Номер картки', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                      'placeholder': "Номер картки"}))
    clubber = forms.BooleanField(label='Учасник клубу?', required=False,
                                 widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    delays = forms.IntegerField(label='Затримки здачі', initial=0,
                                widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                'placeholder': "Затримки здачі"}))

    class Meta:
        model = Reader
        fields = ['first_name', 'second_name', 'last_name', 'card_number', 'clubber', 'delays']
