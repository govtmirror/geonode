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

from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import patterns, url

from geonode.announcements.views import AnnouncementPublishView

js_info_dict = {
    'packages': ('geonode.announcements',),
}

urlpatterns = patterns('geonode.announcements.views',
    url(r'^$', 'announcement_list', name='announcements_list'),
    url(r"^announcement/(?P<pk>\d+)/dismiss/$", 'announcement_dismiss', name="announcements_dismiss"),
    #url(r"^announcement/publish/$", AnnouncementPublishView.as_view(), name="announcements_publish")
    url(r"^announcement/publish/$", "announcement_publish", name="annoucements_publish")
)
