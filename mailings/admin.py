from django.contrib import admin

from .models import Mailing, Client, Message, AuthUser

admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(AuthUser)
