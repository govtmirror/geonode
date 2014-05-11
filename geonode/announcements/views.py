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

from geonode.announcements.models import Announcement
from geonode.announcements.forms import AnnouncementForm
from geonode.announcements.signals import announcement_published

def announcement_list(request):
    return render_to_response("announcements/announcement_list.html", RequestContext(request, {}))

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

class AnnouncementPublishView(CreateView):
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.owner = self.request.user
        announcement.save()
        announcement_published.send(sender=announcement,announcement=announcement,request=self.request)
        #self.object = announcement
        return super(AnnouncementPublishView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("announcements_list")

@login_required
def announcement_publish(request, template='annoucements/annoucement_form.html'):
    poc = document.poc
    metadata_author = document.metadata_author

    if request.method == "POST":
        document_form = DocumentForm(request.POST, instance=document, prefix="resource")
    else:
        document_form = DocumentForm(instance=document, prefix="resource")

    if request.method == "POST" and document_form.is_valid():
        new_poc = document_form.cleaned_data['poc']
        new_author = document_form.cleaned_data['metadata_author']
        new_keywords = document_form.cleaned_data['keywords']

    return render_to_response(template, RequestContext(request, {
        "document": document,
        "document_form": document_form,
        "poc_form": poc_form,
        "author_form": author_form,
    }))
