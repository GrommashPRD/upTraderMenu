from django.contrib import admin
from .models import Menu, MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order')
    list_filter = ('menu',)
    search_fields = ('title',)

admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)