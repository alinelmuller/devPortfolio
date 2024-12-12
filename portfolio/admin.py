from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    exclude = ('password',)

admin.site.register(User, CustomUserAdmin)
