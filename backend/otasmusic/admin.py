from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from otasmusic.models import Album, Person, Song, Record, AuthorLyrics, Band, AuthorMusic


class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "city")

admin.site.register(Person, PersonAdmin)


class BandAdmin(admin.ModelAdmin):
    list_display = ("name", "city")

admin.site.register(Band, BandAdmin)


class AuthorLyricsInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = AuthorLyrics


class AuthorMusicInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = AuthorMusic


class SongAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [AuthorLyricsInline, AuthorMusicInline]

admin.site.register(Song, SongAdmin)


class RecordAdmin(admin.ModelAdmin):
    list_display = ("slug", "song_link")

    def song_link(self, obj):
        song_url = reverse('admin:%s_%s_change' % (obj.song._meta.app_label, obj.song._meta.model_name), args=[obj.song.id])
        return format_html('<a href="{}">{}</a>', song_url, obj.song.name)

    song_link.short_description = 'Song'  # Optional: you can set a custom header for the column

admin.site.register(Record, RecordAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", )

admin.site.register(Album, AlbumAdmin)