from django.contrib import admin
from geonode.contrib.cybergis.models import CyberGISClient, SpatiotemporalBookmark, CyberGISClientBookmark
from geonode.base.admin import MediaTranslationAdmin

import autocomplete_light

class CyberGISClientBookmarkAdmin(admin.ModelAdmin):
    model = CyberGISClientBookmark
    list_display = ('id', 'client', 'bookmark', 'order')
    list_display_links = ('id',)

class SpatiotemporalBookmarkAdmin(admin.ModelAdmin):
    model = SpatiotemporalBookmark
    list_display = ('id', 'name', 'type')
    list_display_links = ('id',)


class CyberGISClientAdmin(MediaTranslationAdmin):
    list_display = ('id', 'title', 'date', 'category')
    list_display_links = ('id',)
    list_filter = ('date', 'date_type', 'restriction_code_type', 'category')
    search_fields = ('title', 'abstract', 'purpose',)
    date_hierarchy = 'date'
    form = autocomplete_light.modelform_factory(CyberGISClient)


admin.site.register(CyberGISClientBookmark, CyberGISClientBookmarkAdmin)
admin.site.register(CyberGISClient, CyberGISClientAdmin)
admin.site.register(SpatiotemporalBookmark, SpatiotemporalBookmarkAdmin)
