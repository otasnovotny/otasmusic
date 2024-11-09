from django.contrib import admin
from otasmusic.models import Album


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", )

admin.site.register(Album, AlbumAdmin)