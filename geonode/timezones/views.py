########################################################################
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

from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.db.models import Q
from geonode.groups.models import GroupProfile
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

import pytz

from .utils import check_for_timezone

#def set_timezone(request):
#    if request.method == 'POST':
#        request.session['django_timezone'] = request.POST['timezone']
#        return redirect('/')
#    else:
#        return render(request, 'template.html', {'timezones': pytz.common_timezones})

def set_timezone(request):
    """
    Redirect to a given url while setting the chosen timezone in the
    session or cookie. The url and the timezone code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'POST':
        tz_code = request.POST.get('timezone', None)
        if tz_code and check_for_timezone(tz_code):
            if hasattr(request, 'session'):
                request.session['tz_code'] = tz_code
            else:
                response.set_cookie('tz_code', tz_code, )
    return response
