import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from users import forms
from users.models import LibraryUser, Reader


class RegisterView(View):
    template_name = 'form.html'
    form_class = forms.ReaderRegisterForm
    success_message = "Користувач зареєстрован\nВведіть код, який вам прислали на пошту"

    def get(self, request):
        form = self.form_class()
        context = {'title': 'Регестрація',
                   'form': form,
                   'button': 'Зареєструватись'}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'title': 'Регестрація',
                   'form': form,
                   'button': 'Зареєструватись'}
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
                return render(request, self.template_name, context=context)
        except ValueError as e:
            messages.error(request, e)
            return render(request, self.template_name, context=context)


class EmailValidationView(View):
    template_name = 'form.html'
    form_class = forms.EmailValidationForm
    success_message = "Користувач активован"

    def get(self, request, pk):
        qs = LibraryUser.objects.filter(id=pk, is_active=False)
        if qs.exists():
            form = self.form_class()
            context = {'title': 'Перевірка пошти',
                       'form': form,
                       'button': 'Перевірити'}
            return render(request, self.template_name, context=context)
        else:
            return render(request, '404.html')

    def post(self, request, pk):
        qs = LibraryUser.objects.filter(id=pk, is_active=False)
        if qs.exists():
            form = self.form_class(request.POST)
            context = {'title': 'Перевірка пошти',
                       'form': form,
                       'button': 'Перевірити'}
            if form.data['email_code'] == qs[0].email_code:
                qs = qs[0]
                qs.is_active = True
                qs.save()
                messages.success(request, self.success_message)
                return redirect(reverse('login'))
            else:
                messages.error(request, "Невірний код\nСпробуйте ще раз")
            return render(request, self.template_name, context=context)
        else:
            return render(request, '404.html')


class LoginView(View):
    template_name = 'form.html'
    form_class = forms.LoginForm
    success_message = "Ви увійшли"

    def get(self, request):
        form = self.form_class()
        context = {'title': 'Вхід',
                   'form': form,
                   'button': 'Увійти'}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'title': 'Вхід',
                   'form': form,
                   'button': 'Увійти'}
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
            return render(request, self.template_name, context=context)


class LogoutView(LoginRequiredMixin, View):
    success_message = "Ви вийшли"

    def get(self, request):
        logout(request)
        messages.success(request, self.success_message)
        return redirect(reverse('login'))


class ReaderListView(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Reader

    def get(self, request, *args, **kwargs):
        user = LibraryUser.objects.filter(id=request.user.id, user_type='Librarian')
        if user.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, "403.html")

    def get_context_data(self, **kwargs):
        context = super(ReaderListView, self).get_context_data(**kwargs)
        context['title'] = 'Список читачів'
        return context


class ReaderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Reader

    def get(self, request, *args, **kwargs):
        user = LibraryUser.objects.filter(id=request.user.id, user_type='Librarian')
        if user.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, "403.html")

    def get_context_data(self, **kwargs):
        context = super(ReaderDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Про читача'
        return context


class CreateReaderView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Reader
    form_class = forms.ReaderForm
    success_url = reverse_lazy('users:create_reader')
    success_message = "Нового читача додано"

    def get(self, request, *args, **kwargs):
        user = LibraryUser.objects.filter(id=request.user.id, user_type='Librarian')
        if user.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, "403.html")

    def get_context_data(self, **kwargs):
        context = super(CreateReaderView, self).get_context_data(**kwargs)
        context['title'] = 'Додати читача'
        context['button'] = 'Додати'
        return context


class UpdateReaderView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Reader
    form_class = forms.ReaderForm
    success_url = reverse_lazy('users:readers_list')
    success_message = "Читач був змінен"

    def get(self, request, *args, **kwargs):
        user = LibraryUser.objects.filter(id=request.user.id, user_type='Librarian')
        if user.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, "403.html")

    def get_context_data(self, **kwargs):
        context = super(UpdateReaderView, self).get_context_data(**kwargs)
        context['title'] = 'Зміна читача'
        context['button'] = 'Змінити'
        return context


class DeleteReaderView(LoginRequiredMixin, DeleteView):
    model = Reader
    success_url = reverse_lazy('users:readers_list')
    success_message = "Читач був видалин"

    def get(self, request, *args, **kwargs):
        user = LibraryUser.objects.filter(id=request.user.id, user_type='Librarian')
        if user.exists():
            messages.success(request, self.success_message)
            return super().delete(request, *args, **kwargs)
        else:
            return render(request, "403.html")
