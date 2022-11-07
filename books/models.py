from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='first name')
    second_name = models.CharField(max_length=150, verbose_name='second name', null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name='last name')
    photo = models.ImageField(upload_to="authors/", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name}"


class Genre(models.Model):
    genre = models.CharField(max_length=150)

    def __str__(self):
        return self.genre


class Book(models.Model):
    book = models.CharField(max_length=250)
    author = models.ForeignKey(Author, related_name="authors", on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    addition_date = models.DateField()
    free = models.BooleanField(default=False)
    translator = models.ForeignKey(Author, related_name="translators", on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to="books/", null=True, blank=True)
    code = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.book}, {self.author}"
