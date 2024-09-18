from django import template
from django.core.validators import URLValidator, EmailValidator
from otasmusic.util import source

register = template.Library()


@register.filter
def prepare_source(value):
    return source.prepare(value)


@register.filter
def is_valid_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except:
        return False

    return True


@register.filter
def is_valid_email(value):
    email_validator = EmailValidator()
    try:
        email_validator(value)
    except:
        return False

    return True