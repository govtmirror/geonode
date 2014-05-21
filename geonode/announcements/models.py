import datetime
import logging
import os
import sys
import uuid

from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from geonode.people.models import Profile
from geonode.contrib.groups.models import Group
from geonode.layers.models import Layer
from geonode.base.models import ResourceBase, Thumbnail, Link

class AnnouncementType(models.Model):
    identifier = models.CharField(max_length=255, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    severity = models.PositiveSmallIntegerField(null=True, default=0,help_text=_('A positive integer representing the severity of the announcement.  The severity increases as the value increases.'))
    urgency = models.PositiveSmallIntegerField(null=True, default=0,help_text=_('A positive integer respresenting the urgency of the announcement.  The urgency increases as the value increases.'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("-severity","-urgency",)
        verbose_name_plural = _("Announcement Types")

class Announcement(models.Model):
    """
    An announcement is information that can be broadcast to a specified audience: public, all users, specific layers, maps, documents, etc.
    """
    title = models.CharField(max_length=100)
    type = models.ForeignKey(AnnouncementType, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    dateCreated = models.DateTimeField(_('Date Created'), default = datetime.datetime.now, help_text=_('The date & time the announcement was created.'))
    dateStart = models.DateTimeField(_('Start Date'), default = None, null=True, blank=True, help_text=_('The date & time the announcement is published.  If null, announcement is published immediately.  Format is YYY-MM-DD HH:mm:ss.'))
    dateEnd = models.DateTimeField(_('End Date'), default = None, null=True, blank=True, help_text=_('The date & time the announcement expires.  If null, announcement never expires.  Format is YYY-MM-DD HH:mm:ss.'))
    owner = models.ForeignKey(User, null=True, blank=False)
    #Audience Variables
    audience_public = models.BooleanField(_("Visible to the Public (Audience)"), default=False, help_text=_('The announcement is visible to the public (i.e., anonymous users).'))
    audience_all_users = models.BooleanField(_("Visible to All Users (Audience)"), default=False, help_text=_('The announcement is visible to all authenticated users.'))

    scope_sitewide = models.BooleanField(_("Display Site-wide (Scope)"), default=False, help_text=_('The announcement is visible on almost all pages.  Use this scope for imminent unscheduled maintenance downtime, etc.'))
    scope_welcome = models.BooleanField(_("Display on Welcome Page (Scope)"), default=False, help_text=_('The announcement is visible on the welcome page.'))
    #target_users = models.ManyToManyField(AnnouncementUserTarget,related_name='target_users')

    #usertargets
    #grouptargets
    #resourcetargets

    def __unicode__(self):
        return self.title
    
    @property
    def url(self):
        return ("announcement_detail", [str(self.pk)])

    class Meta:
        ordering = ("-dateCreated",)
        verbose_name_plural = _("Announcements")

class AnnouncementUserTarget(models.Model):
    announcement = models.ForeignKey(Announcement, help_text=_("The announcement"))
    target = models.ForeignKey(Profile, help_text=_('A target user for the announcement.'))

    def __unicode__(self):
        return self.announcement.title+" - "+self.target.name

    class Meta:
        ordering = ("-announcement__dateCreated","target__name")
        verbose_name_plural = _("Announcement User Target")

class AnnouncementGroupTarget(models.Model):
    announcement = models.ForeignKey(Announcement, help_text=_("The announcement"))
    target = models.ForeignKey(Group, help_text=_('A target group for the announcement.'))

    def __unicode__(self):
        return self.announcement.title+" - "+self.target.name

    class Meta:
        ordering = ("-announcement__dateCreated","target__title")
        verbose_name_plural = _("Announcement Group Targets")

class AnnouncementResourceTarget(models.Model):
    announcement = models.ForeignKey(Announcement, help_text=_('The announcement'))
    target = models.ForeignKey(ResourceBase, help_text=_('The target resource for the announcement.  The announcement is displayed on each resource target detail page.'))

    def __unicode__(self):
        return self.announcement.title+" - "+self.target.title

    class Meta:
        ordering = ("-announcement__dateCreated","target__title")
        verbose_name_plural = _("Announcement Resource Targets")

class DismissalType(models.Model):
    identifier = models.CharField(max_length=255, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("identifier",)
        verbose_name_plural = _("Dismissal Types")

class AnnouncementDismissalOption(models.Model):
    announcement = models.ForeignKey(Announcement, help_text=_('The announcement'))
    type = models.ForeignKey(DismissalType, help_text=_('The type of dismissal available (none, session, permament, etc.).'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("-announcement__dateCreated","type__name")
        verbose_name_plural = _("Announcement Dismissal Options")

class Dismissal(models.Model):
    announcement = models.ForeignKey(Announcement, null=False, blank=False)
    dismissalType = models.ForeignKey(DismissalType, null=False, blank=False)
    user = models.ForeignKey(Profile, null=False, blank=False)
    dismissalDate = models.DateTimeField(_('Dismissal Date'), default = datetime.datetime.now, help_text=_('Date & Time announcement was dismissed by user'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("-dismissalDate",)
        verbose_name_plural = _("Dismissals")

def getActiveAnnouncements(request, **kwargs):
    return Announcement.objects.all();
