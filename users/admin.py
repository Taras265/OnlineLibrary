from django.contrib import admin

from users.models import Reader, LibraryUser, Debtor

admin.site.register(Reader)
admin.site.register(LibraryUser)
admin.site.register(Debtor)
