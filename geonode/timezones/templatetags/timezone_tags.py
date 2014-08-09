from django import template

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

import pytz

register = template.Library()

@register.assignment_tag
def astimezone(datetime, tz_code):
    datetime_utc = pytz.utc.localize(datetime)
    tz = pytz.timezone(tz_code)
    datetime_tz = tz.normalize(datetime_utc.astimezone(tz))
    return datetime_tz
