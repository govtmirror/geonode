from django.contrib import admin
from geonode.announcements.models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'dateCreated', 'type', 'description')
    list_display_links = ('id')
    list_filter  = ('date')
    search_fields = ('title')
    date_hierarchy = 'dateCreated'

admin.site.register(Announcement, AnnouncementAdmin)
