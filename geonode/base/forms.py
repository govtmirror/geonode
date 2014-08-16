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

from django import forms
from django.utils.translation import ugettext as _

from geonode.base.models import TopicCategory


class SplitDateTimeField_GN(forms.SplitDateTimeField):

    """
    The base datetime field used in GeoNode.  The Django field uses a different date format language
    than the Bootstrap datepicker.  Default is ISO 8601 Compliant.  For example, 1980-01-01.
    See https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date and 
    http://bootstrap-datepicker.readthedocs.org/en/release/options.html#format
    """    

    def __init__(self, required=False, input_date_formats=None, input_time_formats=None, *args, **kwargs):
        super(SplitDateTimeField_GN, self).__init__(
            required=False,
            input_date_formats=input_date_formats,
            input_time_formats=input_time_formats,
            *args,
            **kwargs)
        self.widget.widgets[0].attrs = {
        "class": "datepicker",
        'data-date-format': "yyyy-mm-dd"}
        self.widget.widgets[1].attrs = {"class": "time"}

    def clean(self, value):
        return super(SplitDateTimeField_GN, self).clean(value)


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '<span class="has-popover" data-container="body" data-toggle="popover" data-placement="top" ' \
               'data-content="' + obj.description + '" trigger="hover">' + obj.gn_description + '</span>'


class CategoryForm(forms.Form):
    category_choice_field = CategoryChoiceField(required=False,
                                                label='*' + _('Category'),
                                                empty_label=None,
                                                queryset=TopicCategory.objects.extra(order_by=['description']))

    def clean(self):
        cleaned_data = self.data
        ccf_data = cleaned_data.get("category_choice_field")

        if not ccf_data:
            msg = _("Category is required.")
            self._errors = self.error_class([msg])

        # Always return the full collection of cleaned data.
        return cleaned_data
