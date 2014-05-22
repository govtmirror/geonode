import json, os, datetime

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

from geonode.announcements.models import Announcement, AnnouncementResourceTarget, AnnouncementUserTarget, AnnouncementGroupTarget
from geonode.announcements.forms import AnnouncementForm
from geonode.announcements.signals import announcement_published
from geonode.announcements.utils import get_visible_announcements

def announcement_list(request, welcome=False, resource=None):
    announcement_list = get_visible_announcements(request, welcome, resource)
    announcement_list_2 = get_visible_announcements(request, welcome, resource, True)

    return render_to_response("announcements/announcement_list.html", RequestContext(request,
    {
        'announcements': announcement_list,
        'announcements_2': announcement_list_2
    }))

def announcement_dismiss(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    #if announcement.dismissal_type == Announcement.DISMISSAL_SESSION:
    #    dismissed = request.session.get("announcements_dismissed", set())
    #    dismissed.add(announcement.pk)
    #    request.session["announcements_dismissed"] = dismissed
    #    status = 200
    #elif announcement.dismissal_type == Announcement.DISMISSAL_PERMANENT and request.user.is_authenticated():
    #    announcement.dismissals.create(user=request.user)
    #    status = 200
    #else:
    #    status = 409
    status = 200
    return HttpResponse(json.dumps({}), status=status, mimetype="application/json")

#class AnnouncementPublishView(CreateView):
#    model = Announcement
#    form_class = AnnouncementForm
#
#    def form_valid(self, form):
#        announcement = form.save(commit=False)
#        announcement.owner = self.request.user
#        announcement.save()
#        announcement_published.send(sender=announcement,announcement=announcement,request=self.request)
#        #self.object = announcement
#        return super(AnnouncementPublishView, self).form_valid(form)
#    
#    def get_success_url(self):
#        return reverse("announcements_list")

@login_required
def announcement_publish(request, template='announcements/announcement_form.html'):
    if request.method == "POST":
        announcement_form = AnnouncementForm(request.POST)
    else:
        announcement_form = AnnouncementForm(instance=None)

    if request.method == "POST" and announcement_form.is_valid():
        the_announcement = announcement_form.save(commit=False)
        #the_announcement.dateCreated = datetime.datetime.now
        the_announcement.owner = request.user    
        the_announcement.save()
    
        audience_users = announcement_form.cleaned_data['audience_users']
        if not (audience_users is None) and len(audience_users) > 0:
            for target in audience_users:
                obj = AnnouncementUserTarget()
                obj.announcement = the_announcement
                obj.target = target
                obj.save()

        audience_groups = announcement_form.cleaned_data['audience_groups']
        if not (audience_groups is None) and len(audience_groups) > 0:
            for target in audience_groups:
                obj = AnnouncementGroupTarget()
                obj.announcement = the_announcement
                obj.target = target
                obj.save()

        scope_resources = announcement_form.cleaned_data['scope_resources']
        if not (scope_resources is None) and len(scope_resources) > 0:
            for target in scope_resources:
                obj = AnnouncementResourceTarget()
                obj.announcement = the_announcement
                obj.target = target
                obj.save()

        return HttpResponseRedirect(reverse('announcement_list'))
            
    return render_to_response(template, RequestContext(request, {
        'announcement': None,
        'form': announcement_form,
    }))

@login_required
def announcement_edit(request, announcement_id, template='announcements/announcement_form.html'):
    announcement = Announcement.objects.get(id=announcement_id)

    if request.method == "POST":
        announcement_form = AnnouncementForm(request.POST, instance=announcement)
    else:
        announcement_form = AnnouncementForm(instance=announcement)

    if request.method == "POST" and announcement_form.is_valid():
        the_announcement = announcement_form.save()

        AnnouncementUserTarget.objects.filter(announcement__id=announcement_id).delete()
        audience_users = announcement_form.cleaned_data['audience_users']
        if not (audience_users is None) and len(audience_users) > 0:
            for target in audience_users:
                obj = AnnouncementUserTarget()
                obj.announcement = the_announcement
                obj.target = target
                obj.save()

        AnnouncementGroupTarget.objects.filter(announcement__id=announcement_id).delete()
        audience_groups = announcement_form.cleaned_data['audience_groups']
        if not (audience_groups is None) and len(audience_groups) > 0:
            for target in audience_groups:
                obj = AnnouncementGroupTarget()
                obj.announcement = the_announcement
                obj.target = target
                obj.save()


        AnnouncementResourceTarget.objects.filter(announcement__id=announcement_id).delete()
        scope_resources = announcement_form.cleaned_data['scope_resources']
        if not (scope_resources is None) and len(scope_resources) > 0:
            for target in scope_resources:
                obj = AnnouncementResourceTarget()
                obj.announcement = the_announcement
                obj.target = target
                obj.save()

        return HttpResponseRedirect(reverse('announcement_list'))


    return render_to_response(template, RequestContext(request, {
        'announcement': announcement,
        'form': announcement_form,
    }))

@login_required
def announcement_delete (request, announcement_id, template='announcements/announcement_delete.html'):
    announcement = Announcement.objects.get(id=announcement_id)

    if request.method == "POST":
        announcement.delete()
        return HttpResponseRedirect(reverse("announcement_list"))
    elif request.method == "GET":
        return render_to_response(template, RequestContext(request, {
            'announcement': announcement,
        }))
    else:
        return HttpResponse("Not allowed",status=403)
