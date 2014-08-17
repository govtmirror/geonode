import json
import os
import taggit
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.forms import HiddenInput, TextInput
from modeltranslation.forms import TranslationModelForm

from mptt.forms import TreeNodeMultipleChoiceField

from geonode.people.models import Profile
from geonode.contrib.cybergis.models import CyberGISClient
from geonode.maps.models import Map
from geonode.layers.models import Layer
from geonode.base.models import Region


class CyberGISClientConfigurationForm(TranslationModelForm):

    def __init__(self, *args, **kwargs):
        super(CyberGISClientConfigurationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {
                        'class': 'has-popover',
                        'data-content': help_text,
                        'data-placement': 'right',
                        'data-container': 'body',
                        'data-html': 'true'})

    def save(self, *args, **kwargs):

        return super(CyberGISClientConfigurationForm, self).save(*args, **kwargs)

    class Meta:
        model = CyberGISClient
        fields = [
            'title',
            'zoom', 'minzoom', 'maxzoom',
            'latitude', 'longitude',
            'proto', 'carto',
            'search_on'
        ]


class CyberGISClientForm(TranslationModelForm):
    date = forms.DateTimeField(widget=forms.SplitDateTimeWidget)
    date.widget.widgets[0].attrs = {
        "class": "datepicker",
        'data-date-format': "yyyy-mm-dd"}
    date.widget.widgets[1].attrs = {"class": "time"}
    temporal_extent_start = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "datepicker",
                'data-date-format': "yyyy-mm-dd"}))
    temporal_extent_end = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "datepicker",
                'data-date-format': "yyyy-mm-dd"}))

    poc = forms.ModelChoiceField(
        empty_label="Person outside GeoNode (fill form)",
        label="Point Of Contact",
        required=False,
        queryset=Profile.objects.exclude(
            username='AnonymousUser'))

    metadata_author = forms.ModelChoiceField(
        empty_label="Person outside GeoNode (fill form)",
        label="Metadata Author",
        required=False,
        queryset=Profile.objects.exclude(
            username='AnonymousUser'))

    keywords = taggit.forms.TagField(
        required=False,
        help_text=_("A space or comma-separated list of keywords"))

    regions = TreeNodeMultipleChoiceField(
        required=False,
        queryset=Region.objects.all(),
        level_indicator=u'___')
    regions.widget.attrs = {"size": 20}

    def __init__(self, *args, **kwargs):
        super(CyberGISClientForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {
                        'class': 'has-popover',
                        'data-content': help_text,
                        'data-placement': 'right',
                        'data-container': 'body',
                        'data-html': 'true'})

    def save(self, *args, **kwargs):
        
        return super(CyberGISClientForm, self).save(*args, **kwargs)

    class Meta:
        model = CyberGISClient
        exclude = (
            'uuid',
            'contacts',
            'workspace',
            'store',
            'uuid',
            'storeType',
            'typename',
            'bbox_x0',
            'bbox_x1',
            'bbox_y0',
            'bbox_y1',
            'srid',
            'csw_typename',
            'csw_schema',
            'csw_mdsource',
            'csw_type',
            'csw_wkt_geometry',
            'metadata_uploaded',
            'metadata_xml',
            'csw_anytext',
            'popular_count',
            'share_count',
            'thumbnail')
