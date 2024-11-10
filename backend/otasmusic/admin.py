from django.contrib import admin

from otasmusic.models import Album, Person, Song, Record, AuthorLyrics, Band, AuthorMusic, RecordContributor, Skill, \
  RecordContributorSkill


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
  list_display = ("title",)


admin.site.register(Album, AlbumAdmin)


# == song ==
class AuthorLyricsInline(admin.TabularInline):
  model = AuthorLyrics
  extra = 1

class AuthorMusicInline(admin.TabularInline):
  model = AuthorMusic
  extra = 1

class RecordInline(admin.StackedInline):
  model = Record
  extra = 1


class SongAdmin(admin.ModelAdmin):
  list_display = ("name",)
  inlines = [AuthorLyricsInline, AuthorMusicInline, RecordInline]

admin.site.register(Song, SongAdmin)


# == record ==
class RecordContributorInline(admin.TabularInline):
  model = RecordContributor


class RecordAdmin(admin.ModelAdmin):
  list_display = ("title", "song", "creation_date", "release_date")
  inlines = [RecordContributorInline]

admin.site.register(Record, RecordAdmin)


class RecordContributorSkillInline(admin.TabularInline):  # Or use StackedInline for a different layout
  model = RecordContributorSkill
  extra = 1

class RecordContributorAdmin(admin.ModelAdmin):
  list_display = ("person", "record")
  list_filter = ("record__song__name", )
  inlines = [RecordContributorSkillInline]

admin.site.register(RecordContributor, RecordContributorAdmin)
