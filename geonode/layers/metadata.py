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

"""Utilities for managing GeoNode resource metadata
"""

# Standard Modules
import logging
import datetime
from lxml import etree

# Geonode functionality
from geonode import GeoNodeException
# OWSLib functionality
from owslib.csw import CswRecord
from owslib.iso import MD_Metadata
from owslib.fgdc import Metadata

LOGGER = logging.getLogger(__name__)


def set_metadata(xml):
    """Generate dict of model properties based on XML metadata"""

    # check if document is XML
    try:
        exml = etree.fromstring(xml)
    except Exception as err:
        raise GeoNodeException(
            'Uploaded XML document is not XML: %s' % str(err))

    # check if document is an accepted XML metadata format
    tagname = get_tagname(exml)

    if tagname == 'GetRecordByIdResponse':  # strip CSW element
        LOGGER.info('stripping CSW root element')
        exml = exml.getchildren()[0]
        tagname = get_tagname(exml)

    if tagname == 'MD_Metadata':  # ISO
        vals, keywords = iso2dict(exml)
    elif tagname == 'metadata':  # FGDC
        vals, keywords = fgdc2dict(exml)
    elif tagname == 'Record':  # Dublin Core
        vals, keywords = dc2dict(exml)
    else:
        raise RuntimeError('Unsupported metadata format')

    if not vals.get("date_revision"):
        vals["date_revision"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return [vals, keywords]


def iso2dict(exml):
    """generate dict of properties from gmd:MD_Metadata"""

    vals = {}
    keywords = []

    mdata = MD_Metadata(exml)
    vals['language'] = mdata.language or mdata.languagecode or 'eng'
    vals['spatial_representation_type'] = mdata.hierarchy
    #vals['date'] = sniff_date(mdata.datestamp)

    if hasattr(mdata, 'identification'):
        vals['title'] = mdata.identification.title
        vals['abstract'] = mdata.identification.abstract
        vals['purpose'] = mdata.identification.purpose
        if mdata.identification.supplementalinformation is not None:
            vals['supplemental_information'] = \
                mdata.identification.supplementalinformation

        vals['temporal_extent_start'] = \
            mdata.identification.temporalextent_start
        vals['temporal_extent_end'] = \
            mdata.identification.temporalextent_end

        if len(mdata.identification.topiccategory) > 0:
            vals['topic_category'] = mdata.identification.topiccategory[0]

        if (hasattr(mdata.identification, 'keywords') and
                len(mdata.identification.keywords) > 0):
            if None not in mdata.identification.keywords[0]['keywords']:
                keywords = mdata.identification.keywords[0]['keywords']

        if len(mdata.identification.securityconstraints) > 0:
            vals['constraints_use'] = \
                mdata.identification.securityconstraints[0]
        if len(mdata.identification.otherconstraints) > 0:
            vals['constraints_other'] = \
                mdata.identification.otherconstraints[0]

        vals['purpose'] = mdata.identification.purpose

        dateTypes = (
            ('creation', 'date_creation'),
            ('publication', 'date_publication'),
            ('revision', 'date_revision'),
        )
        dates = mdata.identification.date
        if dates:
            for date in dates:
                for date_code, date_attr in dateTypes:
                    if date.type == date_code:
                        vals[date_attr] = sniff_date(date.date)
                        break

    if vals['date_revision'] is None:
        vals['date_revision'] = sniff_date(mdata.datestamp)

    if mdata.dataquality is not None:
        vals['data_quality_statement'] = mdata.dataquality.lineage

    return [vals, keywords]


def fgdc2dict(exml):
    """generate dict of properties from FGDC metadata"""

    vals = {}
    keywords = []

    mdata = Metadata(exml)

    if hasattr(mdata.idinfo, 'citation'):
        if hasattr(mdata.idinfo.citation, 'citeinfo'):
            vals['spatial_representation_type'] = \
                mdata.idinfo.citation.citeinfo['geoform']
            vals['title'] = mdata.idinfo.citation.citeinfo['title']

    if hasattr(mdata.idinfo, 'descript'):
        vals['abstract'] = mdata.idinfo.descript.abstract
        vals['purpose'] = mdata.idinfo.descript.purpose
        if mdata.idinfo.descript.supplinf is not None:
            vals['supplemental_information'] = mdata.idinfo.descript.supplinf

    if hasattr(mdata.idinfo, 'keywords'):
        if mdata.idinfo.keywords.theme:
            for theme in mdata.idinfo.keywords.theme:
                if theme['themekt'] is not None:
                    lowered_themekt = theme['themekt'].lower()

                    # Owslib doesn't support extracting the Topic Category
                    # from FGDC.  So we add support here.
                    # http://www.fgdc.gov/metadata/geospatial-metadata-standards
                    if all(
                        ss in lowered_themekt for ss in [
                            'iso',
                            '19115',
                            'topic']) and any(
                        ss in lowered_themekt for ss in [
                            'category',
                            'categories']):
                        vals['topic_category'] = theme['themekey'][0]

                    keywords.extend(theme['themekey'])

    if hasattr(mdata.idinfo.timeperd, 'timeinfo'):
        if hasattr(mdata.idinfo.timeperd.timeinfo, 'rngdates'):
            vals['temporal_extent_start'] = \
                sniff_date(mdata.idinfo.timeperd.timeinfo.rngdates.begdate)
            vals['temporal_extent_end'] = \
                sniff_date(mdata.idinfo.timeperd.timeinfo.rngdates.enddate)

    vals['constraints_other'] = mdata.idinfo.useconst
    raw_date = mdata.metainfo.metd
    if raw_date is not None:
        vals['date'] = sniff_date(raw_date)

    return [vals, keywords]


def dc2dict(exml):
    """generate dict of properties from csw:Record"""

    vals = {}
    keywords = []

    mdata = CswRecord(exml)
    vals['language'] = mdata.language
    vals['spatial_representation_type'] = mdata.type
    keywords = mdata.subjects
    vals['temporal_extent_start'] = mdata.temporal
    vals['temporal_extent_end'] = mdata.temporal
    vals['constraints_other'] = mdata.license
    #vals['date'] = sniff_date(mdata.modified)
    vals['title'] = mdata.title
    vals['abstract'] = mdata.abstract

    dateTypes = (
        ('created', 'date_creation'),
        ('issued', 'date_publication'),
        ('modified', 'date_revision'),
    )
    for date_code, date_attr in dateTypes:
        if hasattr(mdata, date_code):
            vals[date_attr] = sniff_date(getattr(mdata, date_code))

    if vals['date_revision'] is None:
        vals['date_revision'] = sniff_date(mdata.date)

    if keywords:
        keywords = [keyword for keyword in keywords if keyword]

    return [vals, keywords]


def sniff_date(datestr):
    """
    Attempt to parse date into datetime.datetime object

    Possible inputs:

    '20001122'
    '2000-11-22'
    '2000-11-22T11:11:11Z'
    '2000-11-22T'
    """

    if datestr is None:
        return None

    dateformats = ('%Y%m%d', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%SZ',
                   '%Y-%m-%dT', '%Y/%m/%d')

    for dfmt in dateformats:
        try:
            return datetime.datetime.strptime(datestr.strip(), dfmt)
        except ValueError:
            pass

    return None


def get_tagname(element):
    """get tagname without namespace"""
    try:
        tagname = element.tag.split('}')[1]
    except IndexError:
        tagname = element.tag
    return tagname
