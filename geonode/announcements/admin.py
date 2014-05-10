from django.contrib import admin
from geonode.announcements.models import Announcement, AnnouncementType, Dismissal, DismissalType

class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    list_display = ('id', 'title', 'dateCreated', 'type', 'message','owner')
    list_display_links = ('id',)
    list_filter  = ('dateCreated',)
    search_fields = ('title',)
    date_hierarchy = 'dateCreated'

class AnnouncementTypeAdmin(admin.ModelAdmin):
    model = AnnouncementType
    list_display_links = ('identifier',)
    list_display = ('identifier', 'description')
    
    def has_add_permission(self, request):
            return False
        
    def has_delete_permission(self, request, obj=None):
            return False

class DismissalAdmin(admin.ModelAdmin):
    model = Dismissal
    list_display_links = ('id',)
    list_display = ('id',)

class DismissalTypeAdmin(admin.ModelAdmin):
    model = DismissalType
    list_display_links = ('identifier',)
    list_display = ('identifier', 'description')
    
    def has_add_permission(self, request):
            return False
        
    def has_delete_permission(self, request, obj=None):
            return False

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(AnnouncementType, AnnouncementTypeAdmin)
admin.site.register(Dismissal, DismissalAdmin)
admin.site.register(DismissalType, DismissalTypeAdmin)
