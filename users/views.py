import random

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View

from users import forms
from users.models import LibraryUser, Reader


class RegisterView(View):
    template_name = 'form.html'
    form_class = forms.ReaderRegisterForm
    success_message = "Користувач зареєстрован"

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form,
                                                            'message': message,
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
        except ValueError as e:
            messages.error(request, e)

        return render(request, self.template_name, context={'form': form,
                                                            'button': 'Зареєструватись'})
