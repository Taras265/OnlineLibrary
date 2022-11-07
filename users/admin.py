from django.contrib import admin

from users.models import Debtor, LibraryUser, Reader

admin.site.register(Reader)
admin.site.register(LibraryUser)
admin.site.register(Debtor)
