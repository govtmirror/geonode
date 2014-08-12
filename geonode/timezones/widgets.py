"""
HTML Widget classes
"""

from __future__ import unicode_literals

import copy
from django.conf import settings


class SplitDateTimeWidgetWithTimeZone(MultiWidget):
    """
    A Widget that splits datetime input into three <input type="text"> boxes: date, time, and timezone.
    """
    supports_microseconds = False

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DateInput(attrs=attrs, format=date_format),
                   TimeInput(attrs=attrs, format=time_format))
        super(SplitDateTimeWidgetWithTimeZone, self).__init__(widgets, attrs)

    #Value is in UTC
    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
