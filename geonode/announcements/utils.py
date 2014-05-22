import json, os

from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django_downloadview.response import DownloadResponse
from django.views.generic.edit import UpdateView, CreateView

from geonode.base.models import ResourceBase
from geonode.people.models import Profile
from geonode.contrib.groups.models import Group
from geonode.announcements.models import Announcement, AnnouncementResourceTarget, AnnouncementUserTarget, AnnouncementGroupTarget, Dismissal


## If override is true, return all announcements regardless of scope.
def get_visible_announcements(request, welcome=False, resource=None, overrideScope=False):
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
        if overrideScope:
            announcements_visible = announcements_audience
        else:
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

def get_audience_users_for_announcement(announcement):
    return ([target.target for target in AnnouncementUserTarget.objects.filter(announcement=announcement)])

def get_audience_groups_for_announcement(announcement):
    return ([target.target for target in AnnouncementGroupTarget.objects.filter(announcement=announcement)])

def get_scope_resources_for_announcement(announcement):
    return ([target.target for target in AnnouncementResourceTarget.objects.filter(announcement=announcement)])

def getProfileAsChoice(profile):
    return [str(profile.id),profile.name]

def get_audience_users_for_announcement_as_values(announcement):
    users = get_audience_users_for_announcement(announcement)
    return ([user.id for user in users])

def get_audience_users_as_choices():
    choices = []
    choices.append(['no_target', 'No User Audience'])
    for user in Profile.objects.all():
        choices.append(getProfileAsChoice(user))

    return choices

def getGroupAsChoice(group):
    return [str(group.id), group.title]

def get_audience_groups_for_announcement_as_values(announcement):
    groups = get_audience_groups_for_announcement(announcement)
    return ([group.id for group in groups])

def get_audience_groups_as_choices():
    choices = []
    choices.append(['no_target','No Group Audience'])
    for group in Group.objects.all():
        choices.append(getGroupAsChoice(group))

    return choices

def getResourceAsChoice(resource):
    type_id = ContentType.objects.get_for_model(resource.__class__).id
    obj_id = resource.id
    form_value = "type:%s-id:%s" % (type_id, obj_id)
    display_text = '%s (%s)' % (resource.name, resource.polymorphic_ctype.model)
    return [form_value, display_text]

def get_scope_resources_for_announcement_as_values(announcement):
    values = []
    resources = get_scope_resources_for_announcement(announcement)
    for resource in resources:
        type_id = ContentType.objects.get_for_model(resource.__class__).id
        obj_id = resource.id
        form_value = "type:%s-id:%s" % (type_id, obj_id)
        values.append(form_value)

    return values

def get_scope_resources_as_choices():
    choices = []
    choices.append(['no_target', 'No Resource Scope'])
    for resource in ResourceBase.objects.all():
        choices.append(getResourceAsChoice(resource))

    return choices
