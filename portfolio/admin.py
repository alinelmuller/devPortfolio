from django.contrib import admin
from .models import User, Portfolio, Skill, SkillPort

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    exclude = ('password',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Portfolio)
admin.site.register(Skill)
admin.site.register(SkillPort)
