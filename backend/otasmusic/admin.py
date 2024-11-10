from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from otasmusic.models import Album, Person, Song, Record, AuthorLyrics, Band, AuthorMusic, RecordContributor, Skill


class SkillAdmin(admin.ModelAdmin):
    list_display = ("slug", "order")

admin.site.register(Skill, SkillAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "city")

admin.site.register(Person, PersonAdmin)


class BandAdmin(admin.ModelAdmin):
    list_display = ("name", "city")

admin.site.register(Band, BandAdmin)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", )

admin.site.register(Album, AlbumAdmin)

# == song ==
class AuthorLyricsInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = AuthorLyrics


class AuthorMusicInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = AuthorMusic


class SongAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [AuthorLyricsInline, AuthorMusicInline]

admin.site.register(Song, SongAdmin)

# == record ==
class RecordContributorInline(admin.TabularInline):  # Or use StackedInline for a different layout
    model = RecordContributor


class RecordAdmin(admin.ModelAdmin):
    list_display = ("slug", "song_link")
    inlines = [RecordContributorInline]

    def song_link(self, obj):
        song_url = reverse('admin:%s_%s_change' % (obj.song._meta.app_label, obj.song._meta.model_name), args=[obj.song.id])
        return format_html('<a href="{}">{}</a>', song_url, obj.song.name)

    song_link.short_description = 'Song'

admin.site.register(Record, RecordAdmin)
