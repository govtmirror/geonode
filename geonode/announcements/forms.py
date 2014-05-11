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
    type = forms.ModelChoiceField(queryset=AnnouncementType.objects.order_by("severity","urgency",))
    #dateCreated = forms.DateField(label = "Date Created", required=False,widget=forms.DateInput(attrs={"class":"datepicker", 'data-date-format': "yyyy-mm-dd"}))
    dateStart = forms.DateTimeField(label="Start Date",required=False,widget=forms.SplitDateTimeWidget,help_text=_('The date & time the announcement is published.  If null, announcement is published immediately.'))
    dateStart.widget.widgets[0].attrs = {"class":"datepicker", 'data-date-format': "yyyy-mm-dd"}
    dateStart.widget.widgets[1].attrs = {"class":"time"}
    dateEnd = forms.DateTimeField(label="End Date",required=False,widget=forms.SplitDateTimeWidget,help_text=_('The date & time the announcement expires.  If null, announcement never expires.'))
    dateEnd.widget.widgets[0].attrs = {"class":"datepicker", 'data-date-format': "yyyy-mm-dd"}
    dateEnd.widget.widgets[1].attrs = {"class":"time"}

    target_users = forms.ModelMultipleChoiceField(label="Users",queryset=Profile.objects.all(),help_text=_("Users to receive the announcement."))
    target_groups = forms.ModelMultipleChoiceField(label="Groups",queryset=Group.objects.all(),help_text=_("Groups to receive the announcement."))
    target_resources = forms.ModelMultipleChoiceField(label="Resources",queryset=ResourceBase.objects.all(),help_text=_("Resources (documents, layers, and maps) to receive the announcement."))
    dismissalOptions = forms.ModelMultipleChoiceField(label="Dismissal Options",queryset=DismissalType.objects.all(),help_text=_("What options users have to dismiss the announcement."))

    #def save(self, user, commit=True):
    #    announcement = super(AnnouncementForm, self).save(commit=False)
    #    announcement.owner = user
    #    if commit:
    #        super(AnnouncementForm, self).save()
    #    announcement_published.send(sender=self.o,announcement=self.object,request=self.request)
    #    return announcement

    class Meta:
        model = Announcement
        fields = ["title","type","message","dateStart","dateEnd","target_public","target_all_users","target_users","target_groups","target_resources"]
