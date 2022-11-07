from django.contrib import admin

from books.models import Author, Book, Genre

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
