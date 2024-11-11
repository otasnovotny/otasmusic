# TODO Otas: optimize queries

import urllib
import requests, json
from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Max
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from config import settings


class Person(models.Model):
  slug = models.SlugField(unique=True)
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.EmailField(null=True, blank=True)
  city = models.CharField(max_length=30, null=True, blank=True)

  class Meta:
    ordering = ['last_name', 'first_name']

  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'

  def __str__(self):
    return self.full_name


class PersonContact(models.Model):
  person = models.ForeignKey(Person, on_delete=models.PROTECT)
  contact = models.CharField(max_length=256)
  order = models.SmallIntegerField()

  class Meta:
    ordering = ['order', 'contact']

  def __str__(self):
    return f'{self.person.full_name} - {self.contact}'


class Band(models.Model):
  slug = models.SlugField(unique=True)
  name = models.CharField(max_length=50)
  city = models.CharField(max_length=30)
  date_from = models.DateField(null=True, blank=True)
  date_to = models.DateField(null=True, blank=True)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name


class BandContact(models.Model):
  band = models.ForeignKey(Band, on_delete=models.PROTECT)
  contact = models.CharField(max_length=256)
  order = models.SmallIntegerField()

  class Meta:
    ordering = ['order', 'contact']


class Song(models.Model):
  slug = models.SlugField(unique=True)
  name = models.CharField(max_length=50)
  band = models.ForeignKey(Band, null=True, blank=True, on_delete=models.PROTECT)
  lyrics = models.TextField(null=True, blank=True)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name


class AuthorLyrics(models.Model):
  song = models.ForeignKey(Song, on_delete=models.CASCADE)
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  order = models.SmallIntegerField(null=True, blank=True)

  class Meta:
    ordering = ['song__name', 'order']
    unique_together = ['song', 'person']


class AuthorMusic(models.Model):
  song = models.ForeignKey(Song, on_delete=models.CASCADE)
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  order = models.SmallIntegerField(null=True, blank=True)

  class Meta:
    ordering = ['song__name', 'order']
    unique_together = ['song', 'person']


class AlbumManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().annotate(release_date=Max('record__release_date')).order_by('-release_date')


class Album(models.Model):
  objects = AlbumManager()

  slug = models.SlugField(unique=True)
  title = models.CharField(max_length=50)
  band = models.ForeignKey(Band, null=True, blank=True, on_delete=models.PROTECT)
  url_img_front = models.CharField(max_length=1024, null=True, blank=True)

  def __str__(self):
    return self.title


class RecordManager(models.Manager):
  # Find closest Record in the future
  def get_next(self, record):
    all_next = self.filter(release_date__gt=record.release_date).order_by('release_date')
    try:
      return all_next[0]
    except IndexError:
      return None

  # Find closest Record in the past
  def get_prev(self, record):
    try:
      all_prev = self.filter(release_date__lt=record.release_date).order_by('-release_date')
      return all_prev[0]
    except IndexError:
      return None

  # If YouTube record, get comments
  def get_youtube_comments(self, record):
    if not record.url.startswith('https://youtu.be/'):
      return None

    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params = (
      ('key', settings.YOUTUBE_API_KEY),
      ('textFormat', 'plainText'),
      ('part', 'snippet'),
      ('videoId', record.url.split('/')[-1])
    )

    link = '?'.join([url, urllib.parse.urlencode(params)])
    comments_content = requests.get(link)
    return json.loads(comments_content.text).get('items')


class Record(models.Model):
  objects = RecordManager()

  slug = models.SlugField(unique=True)
  song = models.ForeignKey(Song, null=True, blank=True, on_delete=models.PROTECT)
  band = models.ForeignKey(Band, null=True, blank=True, on_delete=models.SET_NULL)
  url = models.CharField(max_length=1024)
  title = models.CharField(max_length=50)
  creation_date = models.DateField(null=True, blank=True)
  release_date = models.DateField()
  album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.SET_NULL)
  album_order = models.SmallIntegerField(null=True, blank=True)

  class Meta:
    ordering = ['-release_date', 'album_order']

  def __str__(self):
    return f'{self.song.name} - {self.title}'


class RecordContributor(models.Model):
  record = models.ForeignKey(Record, on_delete=models.CASCADE)
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  order = models.SmallIntegerField(null=True, blank=True)

  class Meta:
    ordering = ['order']
    unique_together = ['record', 'person']

  def __str__(self):
    return f'{self.record.title} - {self.person.full_name}'


class EventManager(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(start_datetime__date__gte=timezone.now())


class Event(models.Model):
  objects = EventManager()

  title = models.CharField(max_length=50)
  start_datetime = models.DateTimeField()
  where = models.CharField(max_length=100)
  band = models.ForeignKey(Band, on_delete=models.CASCADE)
  event_url = models.CharField(max_length=1024)
  image_url = models.CharField(max_length=1024)
  gig_datetime = models.DateTimeField(null=True, blank=True)
  gig_order = models.SmallIntegerField(null=True, blank=True)

  class Meta:
    ordering = ['start_datetime']


class Skill(models.Model):
  ACCOUSTIC_GUITAR = 'accoustic-guitar'
  BASS = 'bass'
  BACKING_VOCAL = 'backing-vocal'
  CAMERA = 'camera'
  DRUMS_TRACK = 'drums-track'
  DRUMS = 'drums'
  ELECTRIC_GUITAR = 'electric-guitar'
  KEYBOARD = 'keyboard'
  KEYBOARD_TRACK = 'keyboard-track'
  LEAD_VOCAL = 'lead-vocal'
  MASTERING = 'mastering'
  METALLOPHONE = 'metallophone'
  MIX = 'mix'
  MOUTH_ORGAN = 'mouth-organ'
  RECORDING = 'recording'
  SAXOPHONE = 'saxophone'
  TROMBONE = 'trombone'
  TRUMPET = 'trumpet'
  VIDEO = 'video'

  CHOICES = (
    (ACCOUSTIC_GUITAR, _('accoustic guitar')),
    (BASS, _('bass')),
    (BACKING_VOCAL, _('backing vocal')),
    (CAMERA, _('camera')),
    (DRUMS_TRACK, _('drums track')),
    (DRUMS, _('drums')),
    (ELECTRIC_GUITAR, _('electric guitar')),
    (KEYBOARD, _('keyboard')),
    (KEYBOARD_TRACK, _('keyboard track')),
    (LEAD_VOCAL, _('lead vocal')),
    (MASTERING, _('mastering')),
    (METALLOPHONE, _('metallophone')),
    (MIX, _('mix')),
    (MOUTH_ORGAN, _('mouth organ')),
    (RECORDING, _('recording')),
    (SAXOPHONE, _('saxophone')),
    (TROMBONE, _('trombone')),
    (TRUMPET, _('trumpet')),
    (VIDEO, _('video')),
  )

  slug = models.SlugField(unique=True, choices=CHOICES)
  order = models.SmallIntegerField(null=True, blank=True)

  def __str__(self):
    return self.get_slug_display()

class RecordContributorSkill(models.Model):
  record_contributor = models.ForeignKey(RecordContributor, on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.PROTECT)

  class Meta:
    ordering = ['skill__order']
    unique_together = ['record_contributor', 'skill']
