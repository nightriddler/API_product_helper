from django.contrib import admin

from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('author', 'user',)
    empty_value_display = '-пусто-'


admin.site.register(Follow, FollowAdmin)
