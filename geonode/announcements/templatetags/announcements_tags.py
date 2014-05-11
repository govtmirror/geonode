from django import template
 
from geonode.announcements.models import Announcement

register = template.Library()

@register.assignment_tag
def announcements():
    all = Announcement.objects.all()
    return all
