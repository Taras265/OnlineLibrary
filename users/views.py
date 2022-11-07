import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View

from users import forms
from users.models import LibraryUser, Reader


class RegisterView(View):
    template_name = 'form.html'
    form_class = forms.ReaderRegisterForm
    success_message = "Користувач зареєстрован\nВведіть код, який вам прислали на пошту"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form,
                                                            'button': 'Зареєструватись'})

    def post(self, request):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data

                qs = Reader.objects.get(card_number=form.data.get('reader_card_number'))
                data['reader'] = qs.id

                user = LibraryUser.objects.create_user(data['username'], data['email'], data['password'])
                user.is_active = False
                user.first_name = qs.first_name
                user.second_name = qs.second_name
                user.last_name = qs.last_name
                user.email_code = random.randint(100000, 999999)
                user.reader = qs
                user.user_type = 'Reader'

                user.save()
                messages.success(request, self.success_message)
                return redirect(reverse('email_validation', kwargs={'pk': user.id}))
            else:
                return render(request, self.template_name, context={'form': form,
                                                                    'button': 'Зареєструватись'})
        except ValueError as e:
            messages.error(request, e)
            return render(request, self.template_name, context={'form': form,
                                                                'button': 'Зареєструватись'})


class EmailValidationView(View):
    template_name = 'form.html'
    form_class = forms.EmailValidationForm
    success_message = "Користувач активован"

    def get(self, request, pk):
        qs = LibraryUser.objects.filter(id=pk, is_active=False)
        if qs.exists():
            form = self.form_class()
            return render(request, self.template_name, context={'form': form,
                                                                'button': 'Перевірити'})
        else:
            return render(request, '404.html')

    def post(self, request, pk):
        qs = LibraryUser.objects.filter(id=pk, is_active=False)
        if qs.exists():
            form = self.form_class(request.POST)
            if form.data['email_code'] == qs[0].email_code:
                qs = qs[0]
                qs.is_active = True
                qs.save()
                messages.success(request, self.success_message)
                return redirect(reverse('login'))
            else:
                messages.error(request, "Невірний код\nСпробуйте ще раз")
            return render(request, self.template_name, context={'form': form,
                                                                'button': 'Перевірити'})
        else:
            return render(request, '404.html')


class LoginView(View):
    template_name = 'form.html'
    form_class = forms.LoginForm
    success_message = "Ви увійшли"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form,
                                                            'button': 'Увійти'})

    def post(self, request):
        form = self.form_class(request.POST)
        _next = request.GET.get('next')
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                _next = _next or '/'
                messages.success(request, self.success_message)
                return redirect(_next)
        except ValueError as e:
            messages.error(request, e)
            return render(request, self.template_name, context={'form': form,
                                                                'button': 'Увійти'})


class LogoutView(View):
    success_message = "Ви вийшли"

    def get(self, request):
        logout(request)
        messages.success(request, self.success_message)
        return redirect(reverse('login'))
