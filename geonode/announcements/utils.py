import json, os

from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django_downloadview.response import DownloadResponse
from django.views.generic.edit import UpdateView, CreateView

from geonode.people.models import Profile
from geonode.contrib.groups.models import Group
from geonode.announcements.models import Announcement, AnnouncementResourceTarget, AnnouncementUserTarget, AnnouncementGroupTarget, Dismissal

def get_visible_announcements(request, welcome=False, resource=None):
    announcements_visible = []
    user = request.user
    #print user
    #print user.is_authenticated()
    if user.is_authenticated():
        announcements_audience = []
        profile = Profile.objects.filter(user=user)
        groups = Group.groups_for_user(user)

        #Get Resources For Various Filters
        dismissed_announcements = get_dismissed_announcements_for_user(profile)
        targeted_users_announcements = get_announcements_for_user(profile)
        targeted_groups_announcements = get_announcements_for_groups(groups)
        targeted_resources_announcements = get_announcements_for_resource(resource)
        announcements_notdismissed = Announcement.objects.exclude(id__in=dismissed_announcements)

        #Filter Audience
        for announcement in announcements_notdismissed:
            if announcement.audience_public:
                announcements_audience.append(announcement)
            elif announcement.audience_all_users:
                announcements_audience.append(announcement)
            elif announcement.id in targeted_users_announcements:
                announcements_audience.append(announcement)
            elif announcement.id in targeted_groups_announcements:
                announcements_audience.append(announcement)

        #Filter Scope
        for announcement in announcements_audience:
            if announcement.scope_sitewide:
                announcements_visible.append(announcement)
            elif welcome and announcement.scope_welcome:
                announcements_visible.append(announcement)
            elif resource and (announcement.id in targeted_resources_announcements):
                announcements_visible.append(announcement)
    else:
        announcements = Announcement.objects.filter(audience_public=True)
        announcements_visible = announcements

    return announcements_visible

def get_dismissed_announcements_for_user(profile):
    return ([dismissal.announcement.id for dismissal in Dismissal.objects.filter(user=profile)])

def get_announcements_for_user(profile):
    return ([target.announcement.id for target in AnnouncementUserTarget.objects.filter(target=profile)])

def get_announcements_for_groups(groups):
    return ([target.announcement.id for target in AnnouncementGroupTarget.objects.filter(target__in=groups)])

def get_announcements_for_resource(resource):
    if resource is None:
        return []
    else:
        return ([target.announcement.id for target in AnnouncementResourceTarget.objects.filter(target=resource)])
