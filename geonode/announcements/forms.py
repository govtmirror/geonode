import json
import os
import taggit
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.forms import HiddenInput, TextInput

from geonode.base.models import ResourceBase
from geonode.people.models import Profile
from geonode.contrib.groups.models import Group
from geonode.documents.models import Document
from geonode.maps.models import Map
from geonode.layers.models import Layer
from geonode.announcements.models import Announcement, AnnouncementType, AnnouncementUserTarget, AnnouncementGroupTarget, AnnouncementResourceTarget, AnnouncementDismissalOption, Dismissal, DismissalType

class AnnouncementForm(forms.ModelForm):
    type = forms.ModelChoiceField(required=True,queryset=AnnouncementType.objects.order_by("severity","urgency",))
    #dateCreated = forms.DateField(label = "Date Created", required=False,widget=forms.DateInput(attrs={"class":"datepicker", 'data-date-format': "yyyy-mm-dd"}))
    dateStart = forms.DateTimeField(label="Start Date",required=False,widget=forms.SplitDateTimeWidget,help_text=_('The date & time the announcement is published.  If null, announcement is published immediately.  Format is YYY-MM-DD HH:mm:ss.'))
    dateStart.widget.widgets[0].attrs = {"class":"datepicker", 'data-date-format': "yyyy-mm-dd"}
    dateStart.widget.widgets[1].attrs = {"class":"time"}
    dateEnd = forms.DateTimeField(label="End Date",required=False,widget=forms.SplitDateTimeWidget,help_text=_('The date & time the announcement expires.  If null, announcement never expires.  Format is YYY-MM-DD HH:mm:ss.'))
    dateEnd.widget.widgets[0].attrs = {"class":"datepicker", 'data-date-format': "yyyy-mm-dd"}
    dateEnd.widget.widgets[1].attrs = {"class":"time"}

    #Audience Fields
    audience_users = forms.ModelMultipleChoiceField(label="Users (Audience)",required=False,queryset=Profile.objects.all(),help_text=_("The users who will receive the announcement.  This variable sets the audience, but not how the messages will be received."))
    audience_groups = forms.ModelMultipleChoiceField(label="Groups (Audience)",required=False,queryset=Group.objects.all(),help_text=_("The groups to receive the announcement.  This variable sets the audience, but not how the messages will be received."))

    #Pages Fields
    scope_resources = forms.ModelMultipleChoiceField(label="Resources (Scope)",required=False,queryset=ResourceBase.objects.all(),help_text=_("Resources (documents, layers, and maps) to display the announcement.  Resouces selected will display the announcement on their detail page.  Additionally, subscribers to a resource may recieve emails notifications depending on their preferences."))

    #Dismissal Fields
    dismissalOptions = forms.ModelMultipleChoiceField(label="Dismissal Options",required=False,queryset=DismissalType.objects.all(),help_text=_("What options users have to dismiss the announcement."))

    #def save(self, user, commit=True):
    #    announcement = super(AnnouncementForm, self).save(commit=False)
    #    announcement.owner = user
    #    if commit:
    #        super(AnnouncementForm, self).save()
    #    announcement_published.send(sender=self.o,announcement=self.object,request=self.request)
    #    return announcement

    class Meta:
        model = Announcement
        fields = ["title","type","message","dateStart","dateEnd","audience_public","audience_all_users","audience_users","audience_groups","scope_sitewide","scope_welcome","scope_resources"]
