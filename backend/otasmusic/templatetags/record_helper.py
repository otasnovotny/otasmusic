from django import template
from otasmusic.models import Record
from django.utils.dateparse import parse_date

register = template.Library()


@register.filter
def get_next(record):
    return Record.objects.get_next(record)


@register.filter
def get_prev(record):
    return Record.objects.get_prev(record)


@register.filter
def get_youtube_comments(record):
    return Record.objects.get_youtube_comments(record)


@register.filter
def str2date(str):
    return parse_date(str[0:10])
