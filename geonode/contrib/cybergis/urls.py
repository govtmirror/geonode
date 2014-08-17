# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

js_info_dict = {
    'packages': ('geonode.contrib.cybergis',),
}

urlpatterns = patterns(
    'geonode.contrib.cybergis.views',
    url(r'^$',
        TemplateView.as_view(template_name='cybergis/client_list.html'),
        name='client_browse'),
    url(r'^client_library_proto$',
        TemplateView.as_view(template_name='cybergis/client_library_proto.html'),
        name='client_library_proto'),
    url(r'^client_library_carto$',
        TemplateView.as_view(template_name='cybergis/client_library_carto.html'),
        name='client_library_carto'),
    url(r'^(?P<clientid>\d+)/?$',
        'client_detail',
        name='client_detail'),
    url(r'^(?P<clientid>\d+)/metadata$',
        'client_metadata',
        name='client_metadata'),
    url(r'^(?P<clientid>\d+)/conf$',
        'client_conf',
        name='client_conf'),
    url(r'^(?P<clientid>\d+)/remove$',
        'client_remove',
        name="client_remove"),
    url(r'^create/$',
        'client_create',
        name="client_create"),


    url(r'^(?P<clientid>\d+)/viewer.html$', 'client_viewer', name="client_viewer"),
    url(r'^(?P<clientid>\d+)/properties.json$', 'client_properties', name="client_properties"),
    url(r'^(?P<clientid>\d+)/proto.json$', 'client_proto', name="client_proto"),
    url(r'^(?P<clientid>\d+)/carto.json$', 'client_carto', name="client_carto"),
    url(r'^(?P<clientid>\d+)/bookmarks.tsv$', 'client_bookmarks', name="client_bookmarks"),
)
