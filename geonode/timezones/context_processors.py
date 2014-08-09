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

from django.conf import settings
from django.core.urlresolvers import reverse

def timezones(request):
    """Global values to pass to templates"""
    #tz_code = request.session['tz_code'] or request.user.profile.timezone or settings.TIME_ZONE
    tz_code = request.session.get('tz_code', None)
    #print "Session Value: "+str(tz_code)
    if tz_code is None:
        if request.user.is_authenticated():
            tz_code = request.user.account.timezone or settings.TIME_ZONE
        else:
            tz_code = settings.TIME_ZONE
            
    #print tz_code
    defaults = dict(
        TZ_CODE = tz_code,
    )
    return defaults
