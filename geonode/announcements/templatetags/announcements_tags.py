from django import template
 
from geonode.announcements.models import Announcement

register = template.Library()

@register.assignment_tag
def all_announcements():
    all = Announcement.objects.all()
    return all
