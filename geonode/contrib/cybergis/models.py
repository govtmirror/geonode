import logging
import os
import uuid

from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.contrib.contenttypes import generic
from django.contrib.staticfiles import finders
from django.utils.translation import ugettext_lazy as _

from geonode.layers.models import Layer
from geonode.base.models import ResourceBase, Thumbnail, Link, resourcebase_post_save
from geonode.maps.signals import map_changed_signal
from geonode.maps.models import Map

logger = logging.getLogger(__name__)


class CyberGISLayer(models.Model):

    name = models.CharField(max_length=100)
    classification = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("name", )
        verbose_name_plural = 'CyberGIS Layers'


class SpatiotemporalBookmark(models.Model):

    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    zoom = models.PositiveSmallIntegerField(
        _('Zoom'),
        help_text=_('default zoom for this app'),
        default=7)
    layer = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    @property
    def as_tsv(self):
        values = []
        values.append(self.name)
        values.append(self.label)
        values.append(self.type)
        if (self.latitude and self.longitude) or (self.latitude == 0 and self.longitude == 0):
            values.append(str(self.latitude))
            values.append(str(self.longitude))
        else:
            values.append("-")
            values.append("-")
        if self.zoom or (self.zoom == 0):
            values.append(str(self.zoom))
        else:
            values.append("-")
        if self.layer and self.field and self.value:
            values.append(self.layer)
            values.append(self.field)
            values.append(self.value)
        else:
            values.append("-")
            values.append("-")
            values.append("-")

        return "\t".join(values)

    class Meta:
        ordering = ("name", )
        verbose_name = _("Spatiotemporal Bookmark")
        verbose_name_plural = 'Spatiotemporal Bookmarks'

class CyberGISClient(ResourceBase):

    """
    A CyberGIS Client is a viewer.
    """
    name_help_text = _('name of the viewer')

    #name = models.CharField(_('Name'), max_length=255, blank=True, null=True, help_text=name_help_text)
    proto = models.TextField(_('Proto'), null=True, blank=True,default="{\"layers\":{\"osm\":{\"name\":\"OSM\",\"classification\":\"Unclassified\",\"description\":\"OpenStreetMap is a free, editable map of the whole world.\",\"type\":\"OSM\"}}}")
    carto = models.TextField(_('Carto'), null=True, blank=True,default="{\"layers\":{}}")

    zoom = models.PositiveSmallIntegerField(
        _('Default Zoom'),
        help_text=_('default zoom for this app'),
        default=7)
    minzoom = models.PositiveSmallIntegerField(
        _('Min Zoom'),
        help_text=_('minimum zoom for this app'),
        default=0)
    maxzoom = models.PositiveSmallIntegerField(
        _('Max Zoom'),
        help_text=_('max zoom for this app'),
        default=18)

    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    search_on = models.BooleanField(_("Search On"),default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('client_detail', args=(self.id,))

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def has_bookmarks(self):
        return CyberGISClientBookmark.objects.filter(client=self).count() > 0

    def get_bookmarks_for_client(self):
        """
        Returns the bookmarks that are part of this client.
        """
        return  ([bookmark.bookmark for bookmark in CyberGISClientBookmark.objects.filter(client=self).order_by("order",)])

    class Meta(ResourceBase.Meta):
        ordering = ("id", )
        verbose_name = _("CyberGIS Client")
        verbose_name_plural = 'CyberGIS Clients'


class CyberGISClientBookmark(models.Model):
    client = models.ForeignKey(CyberGISClient, help_text=_("The CyberGIS Client"))
    bookmark = models.ForeignKey(SpatiotemporalBookmark, help_text=_('A bookmark for the CyberGIS Client.'))
    order = models.PositiveSmallIntegerField(
        _('Bookmark'),
        help_text=_('position of this bookmark'),
        default=0)

    def __unicode__(self):
        return self.client.title+" - "+self.bookmark.name

    class Meta:
        ordering = ("client__title","bookmark__name")
        verbose_name = _("CyberGIS Client Bookmark")
        verbose_name_plural = _("CyberGIS Client Bookmarks")

class CyberGISClientFeatureLayer(models.Model):
    client = models.ForeignKey(CyberGISClient, help_text=_("The CyberGIS Client"))
    layer = models.ForeignKey(CyberGISLayer, help_text=_('A layer for the CyberGIS Client.'))
    order = models.PositiveSmallIntegerField(
        _('Bookmark'),
        help_text=_('position of this bookmark'),
        default=0)

    def __unicode__(self):
        return self.client.title+" - "+self.bookmark.name

    class Meta:
        ordering = ("client__name","bookmark__name")
        verbose_name_plural = _("CyberGIS Client Bookmark")


signals.post_save.connect(resourcebase_post_save, sender=CyberGISClient)
