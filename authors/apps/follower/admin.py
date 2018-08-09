from django.contrib import admin
from .models import Connect

class ConnectAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']

admin.site.register(Connect, ConnectAdmin)