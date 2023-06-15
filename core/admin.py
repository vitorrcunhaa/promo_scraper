from django.contrib import admin
from core.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'keywords', 'instant_searches_left')


admin.site.register(CustomUser, CustomUserAdmin)

