import json

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django_downloadview.response import DownloadResponse
from django.views.generic.edit import UpdateView, CreateView
from geonode.utils import resolve_object
from geonode.security.views import _perms_info_json
from geonode.people.forms import ProfileForm
from geonode.base.forms import CategoryForm
from geonode.base.models import TopicCategory
from geonode.contrib.cybergis.models import CyberGISClient
from geonode.contrib.cybergis.forms import CyberGISClientForm, CyberGISClientConfigurationForm

_PERMISSION_MSG_DELETE = _("You are not permitted to delete this document")
_PERMISSION_MSG_GENERIC = _('You do not have permissions for this document.')
_PERMISSION_MSG_MODIFY = _("You are not permitted to modify this document")
_PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this document's metadata")
_PERMISSION_MSG_VIEW = _("You are not permitted to view this document")


def _resolve_client(request, clientid, permission='base.change_resourcebase',
                      msg=_PERMISSION_MSG_GENERIC, **kwargs):
    '''
    Resolve the layer by the provided typename and check the optional permission.
    '''
    return resolve_object(request, CyberGISClient, {'pk': clientid},
                          permission=permission, permission_msg=msg, **kwargs)

@login_required
def client_create(request):
    if request.method == "POST":
        form = CyberGISClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            form.save_m2m()
            return HttpResponseRedirect(
                reverse(
                    "client_detail",
                    args=[
                        client.id]))
    else:
        form = CyberGISClientForm()

    return render_to_response("cybergis/client_create.html", {
        "form": form,
    }, context_instance=RequestContext(request))


def client_viewer(request, clientid):
    """
    The viewer for the specified client
    """
    client = get_object_or_404(CyberGISClient, pk=clientid)

    return render_to_response(
        "cybergis/client_viewer.html",
        RequestContext(
            request,
            {
                'permissions_json': _perms_info_json(client),
                'client': client}))

def client_properties(request, clientid):
    """
    The properties for the specified client
    """
    client = get_object_or_404(CyberGISClient, pk=clientid)

    return render_to_response(
        "cybergis/client_properties.json",
        RequestContext(
            request,
            {
                'permissions_json': _perms_info_json(client),
                'client': client}))

def client_proto(request, clientid):
    """
    The proto for the specified client
    """
    client = get_object_or_404(CyberGISClient, pk=clientid)

    return render_to_response(
        "cybergis/client_proto.json",
        RequestContext(
            request,
            {
                'permissions_json': _perms_info_json(client),
                'client': client}))

def client_carto(request, clientid):
    """
    The carto for the specified client
    """
    client = get_object_or_404(CyberGISClient, pk=clientid)

    return render_to_response(
        "cybergis/client_carto.json",
        RequestContext(
            request,
            {
                'permissions_json': _perms_info_json(client),
                'client': client}))

def client_bookmarks(request, clientid):
    """
    The carto for the specified client
    """
    client = get_object_or_404(CyberGISClient, pk=clientid)
    bookmarks = client.get_bookmarks_for_client()

    return render_to_response(
        "cybergis/client_bookmarks.tsv",
        RequestContext(
            request,
            {
                'permissions_json': _perms_info_json(client),
                'bookmarks': bookmarks}),
        mimetype="text/plain")

def client_detail(request, clientid):
    """
    The view that show details of each CyberGIS Client
    """
    client = get_object_or_404(CyberGISClient, pk=clientid)
    if not request.user.has_perm(
            'view_resourcebase',
            obj=client.get_self_resource()):
        return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to view this CyberGIS Client.")})), status=403)
    
    return render_to_response(
        "cybergis/client_detail.html",
        RequestContext(
            request,
            {
                'permissions_json': _perms_info_json(client),
                'resource': client}))

@login_required
def client_conf(
        request,
        clientid,
        template='cybergis/client_conf.html'):
    client = CyberGISClient.objects.get(id=clientid)

    if request.method == "POST":
        client_form = CyberGISClientConfigurationForm(
            request.POST,
            instance=client,
            prefix="resource")
    else:
        client_form = CyberGISClientConfigurationForm(instance=client, prefix="resource")

    if request.method == "POST" and client_form.is_valid():
            the_client = client_form.save()
            the_client.save()
            return HttpResponseRedirect(
                reverse(
                    'client_detail',
                    args=(
                        client.id,
                    )))


    return render_to_response(template, RequestContext(request, {
        "client": client,
        "client_form": client_form,
    }))

@login_required
def client_metadata(
        request,
        clientid,
        template='cybergis/client_metadata.html'):
    client = CyberGISClient.objects.get(id=clientid)

    poc = client.poc
    metadata_author = client.metadata_author
    topic_category = client.category

    if request.method == "POST":
        client_form = CyberGISClientForm(
            request.POST,
            instance=client,
            prefix="resource")
        category_form = CategoryForm(
            request.POST,
            prefix="category_choice_field",
            initial=int(
                request.POST["category_choice_field"]) if "category_choice_field" in request.POST else None)
    else:
        client_form = CyberGISClientForm(instance=client, prefix="resource")
        category_form = CategoryForm(
            prefix="category_choice_field",
            initial=topic_category.id if topic_category else None)

    if request.method == "POST" and client_form.is_valid(
    ) and category_form.is_valid():
        new_poc = client_form.cleaned_data['poc']
        new_author = client_form.cleaned_data['metadata_author']
        new_keywords = client_form.cleaned_data['keywords']
        new_category = TopicCategory.objects.get(
            id=category_form.cleaned_data['category_choice_field'])

        if new_poc is None:
            if poc.user is None:
                poc_form = ProfileForm(
                    request.POST,
                    prefix="poc",
                    instance=poc)
            else:
                poc_form = ProfileForm(request.POST, prefix="poc")
            if poc_form.has_changed and poc_form.is_valid():
                new_poc = poc_form.save()

        if new_author is None:
            if metadata_author is None:
                author_form = ProfileForm(request.POST, prefix="author",
                                          instance=metadata_author)
            else:
                author_form = ProfileForm(request.POST, prefix="author")
            if author_form.has_changed and author_form.is_valid():
                new_author = author_form.save()

        if new_poc is not None and new_author is not None:
            the_client = client_form.save()
            the_client.poc = new_poc
            the_client.metadata_author = new_author
            the_client.keywords.add(*new_keywords)
            the_client.category = new_category
            the_client.save()
            return HttpResponseRedirect(
                reverse(
                    'client_detail',
                    args=(
                        client.id,
                    )))

    if poc is None:
        poc_form = ProfileForm(request.POST, prefix="poc")
    else:
        if poc is None:
            poc_form = ProfileForm(instance=poc, prefix="poc")
        else:
            client_form.fields['poc'].initial = poc.id
            poc_form = ProfileForm(prefix="poc")
            poc_form.hidden = True

    if metadata_author is None:
        author_form = ProfileForm(request.POST, prefix="author")
    else:
        if metadata_author is None:
            author_form = ProfileForm(
                instance=metadata_author,
                prefix="author")
        else:
            client_form.fields[
                'metadata_author'].initial = metadata_author.id
            author_form = ProfileForm(prefix="author")
            author_form.hidden = True

    return render_to_response(template, RequestContext(request, {
        "client": client,
        "client_form": client_form,
        "poc_form": poc_form,
        "author_form": author_form,
        "category_form": category_form,
    }))


def document_search_page(request):
    # for non-ajax requests, render a generic search page

    if request.method == 'GET':
        params = request.GET
    elif request.method == 'POST':
        params = request.POST
    else:
        return HttpResponse(status=405)

    return render_to_response(
        'cybergis/client_search.html',
        RequestContext(
            request,
            {
                'init_search': json.dumps(
                    params or {}),
                "site": settings.SITEURL}))


@login_required
def client_remove(request, clientid, template='cybergis/client_remove.html'):
    try:
        client = _resolve_client(
            request,
            clientid,
            'base.delete_resourcebase',
            _PERMISSION_MSG_DELETE)

        if request.method == 'GET':
            return render_to_response(template, RequestContext(request, {
                "client": client
            }))
        if request.method == 'POST':
            client.delete()
            return HttpResponseRedirect(reverse("client_browse"))
        else:
            return HttpResponse("Not allowed", status=403)

    except PermissionDenied:
        return HttpResponse(
            'You are not allowed to delete this CyberGIS Client',
            mimetype="text/plain",
            status=401
        )
