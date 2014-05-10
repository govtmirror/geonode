import logging
import os
import sys
import uuid

from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from geonode.layers.models import Layer
from geonode.base.models import ResourceBase, Thumbnail, Link

class AnnouncementType(models.Model):
    identifier = models.CharField(max_length=255, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    severity = models.PositiveSmallIntegerField(null=True, default=0)
    urgency = models.PositiveSmallIntegerField(null=True, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = _("-severity","-urgency")
        verbose_name_plural = _("Announcement Types")

class DismissalType(models.Model):
    identifier = models.CharField(max_length=255, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class Announcement(models.Model):
    """
    An announcement is information that can be broadcast to a specified audience: public, all users, specific layers, maps, documents, etc.
    """
    title = models.CharField(max_length=100)
    type = models.ForeignKey(AdnnouncementType)
    message = models.TextField(null=True, blank=True)
    dateCreated = models.DateTimeField(_('date'), default = datetime.datetime.now, help_text=_('Date & Time announcement created by owner'))
    owner = models.ForeignKey(Profile, null=False, blank=False)
    dateStart = models.DateTimeField(_('date'), default = datetime.datetime.now, help_text=_('Date & Time announcement starts'))
    dateEnd = models.DateTimeField(_('date'), default = datetime.datetime.now, help_text=_('Date & Time announcement ends'))
    
    def __unicode__(self):
        return self.title
    
    @property
    def url(self):
        return ("announcement_detail", [str(self.pk)])

    class Meta:
        ordering = _("-dateCreated")
        verbose_name_plural = _("Announcements")

class Dismissal(models.Model):
    announcement = models.ForeignKey(Announcement, null=False, blank=False)
    dismissalType = models.ForeignKey(DismissalType, null=False, blank=False)
    user = models.ForeignKey(Profile, null=False, blank=False)
    dismissalDate = models.DateTimeField(_('date'), default = datetime.datetime.now, help_text=_('Date & Time announcement was dismissed by user'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = _("-dismissalDate")
        verbose_name_plural = _("Dismissals")


