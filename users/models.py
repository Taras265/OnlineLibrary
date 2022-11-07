from django.contrib.auth.models import AbstractUser
from django.db import models
from users.enums import UserTypeChoice


class Reader(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='first name')
    second_name = models.CharField(max_length=150, verbose_name='second name')
    last_name = models.CharField(max_length=150, verbose_name='last name')
    card_number = models.CharField(max_length=150, verbose_name='card number')
    clubber = models.BooleanField()
    delays = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name}, {self.card_number}"


class LibraryUser(AbstractUser):
    first_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='first name')
    second_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='second name')
    last_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='last name')
    email = models.CharField(max_length=150)
    email_code = models.IntegerField(max_length=4, default=1298)

    user_type = models.CharField(max_length=10,
                                 choices=[(tag, tag.value) for tag in UserTypeChoice])
    reader = models.ForeignKey(
        Reader, related_name="readers", on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name}, {self.user_type}"


class Debtor(models.Model):
    book = models.ForeignKey(
        "books.Book", related_name="debtor_books", on_delete=models.CASCADE
    )
    reader = models.ForeignKey(
        Reader, related_name="debtors", on_delete=models.SET_NULL,
        null=True, blank=True
    )
    taking_date = models.DateField(verbose_name="taking date")
    requested_return_date = models.DateField(verbose_name="requested return date")
    returned = models.BooleanField()
    return_date = models.DateField(verbose_name="return date")

    def __str__(self):
        return f"{self.book} - {self.reader}"
