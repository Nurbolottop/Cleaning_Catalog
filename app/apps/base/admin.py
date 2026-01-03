from django.contrib import admin
from apps.base import models as base_models
from django.contrib.auth.models import User, Group

# Register your models here.
@admin.register(base_models.Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'location')
    search_fields = ('title', 'phone', 'email', 'location')
    list_filter = ('title',)

    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'descriptions', 'icon', 'logo',  )
        }),
        ('Контакты', {
            'fields': ('phone', 'email', 'location')
        }),
        ('Социальные сети', {
            'fields': ('instagram', )
        }),
    )

@admin.register(base_models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'image')
    search_fields = ('title', 'subtitle')
    list_filter = ('title',)

admin.site.unregister(User)
admin.site.unregister(Group)
