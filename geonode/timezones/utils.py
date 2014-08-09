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

import httplib2
import base64
import math
import copy
import string

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.http import HttpResponse
from django.core.cache import cache

import pytz

#tz_code_re = re.compile(r'^[a-z]{1,8}(?:-[a-z0-9]{1,8})*$', re.IGNORECASE)
timezones = list(zip(pytz.all_timezones, pytz.all_timezones))

#@lru_cache.lru_cache(maxsize=1000)
def check_for_timezone(tz_code):
    """
    Checks whether there is timezone ifo for the given timezone
    code. This is used to decide whether a user-provided language is
    available.

    lru_cache should have a maxsize to prevent from memory exhaustion attacks,
    as the provided timezone codes are taken from the HTTP request. See also
    <https://www.djangoproject.com/weblog/2007/oct/26/security-fix/>.
    """
    # First, a quick check to make sure lang_code is well-formed (#21458)
    #if not tz_code_re.search(tz_code):
    #    return False
    for code, label in timezones:
        print code
        if tz_code == code:
            return True
    return False
