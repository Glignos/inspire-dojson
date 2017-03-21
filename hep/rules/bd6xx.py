# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""DoJSON rules for MARC fields in 6xx."""

from __future__ import absolute_import, division, print_function

from dojson import utils

from inspire_schemas.utils import load_schema
from inspirehep.utils.helpers import force_list

from ..model import hep, hep2marc
from ...utils import get_record_ref


@hep.over('accelerator_experiments', '^693..')
def accelerator_experiments(self, key, value):
    result = self.get('accelerator_experiments', [])

    for value in force_list(value):
        e_values = force_list(value.get('e'))
        zero_values = force_list(value.get('0'))

        # XXX: we zip only when they have the same length, otherwise
        #      we might match a value with the wrong recid.
        if len(e_values) == len(zero_values):
            for e_value, zero_value in zip(e_values, zero_values):
                result.append({
                    'legacy_name': e_value,
                    'record': get_record_ref(zero_value, 'experiments'),
                })
        else:
            for e_value in e_values:
                result.append({'legacy_name': e_value})

    return result


@hep2marc.over('693', '^accelerator_experiments$')
@utils.for_each_value
def accelerator_experiments2marc(self, key, value):
    return {'e': value.get('legacy_name')}


@hep.over('keywords', '^(653|695)..')
@utils.for_each_value
def keywords(self, key, value):
    """Parse keywords.

    We have 2 types of keywords from marc, the 'thesaurus_terms' and
    'freekeys', and we want to merge them for json into a big 'keywords' and
    extract the 'energy_ranges' too that is represented in marc as special
    value of some keywords.
    """
    def _is_thesaurus(key):
        return key.startswith('695')

    def _is_energy(value):
        return 'e' in value

    def _freekey_get_source(source_value):
        if not isinstance(source_value, (list, tuple, set)):
            return source_value

        source_value = [source.lower() for source in source_value]
        if 'conference' in source_value:
            return ''

        for source in source_value:
            if source in ['author', 'publisher']:
                return source

        return ''

    def _freekey_get_dict(elem):
        keyword = {
            'value': elem.get('a'),
        }

        source = _freekey_get_source(elem.get('9'))
        if source:
            keyword['source'] = source

        return keyword

    def _get_keyword_dict(key, elem):
        if _is_thesaurus(key) and elem.get('a'):
            _schema = load_schema('hep')
            valid_keywords = _schema['properties']['keywords']['items']['properties']['schema']['enum']
            schema_in_marc = elem.get('2').upper()
            schema = schema_in_marc if schema_in_marc in valid_keywords else ''

            return {
                'schema': schema,
                'source': elem.get('9', ''),
                'value': elem.get('a'),
            }
        elif _is_energy(elem):
            return {}
        else:
            return _freekey_get_dict(elem)

    if _is_energy(value):
        if 'energy_ranges' not in self:
            self['energy_ranges'] = list()

        self['energy_ranges'].append(int(value.get('e')))
        self['energy_ranges'].sort()

    result = _get_keyword_dict(key, value)
    if 'value' in result and result['value']:
        return result


@hep2marc.over('695', '^keywords$')
def keywords2marc(self, key, values):
    values = force_list(values)

    def _is_thesaurus(elem):
        return elem.get('schema', '') is not ''

    def _thesaurus_to_marc_dict(elem):
        result = {
            'a': elem.get('value'),
            '2': elem.get('schema'),
        }
        source = elem.get('source', None)
        if source:
            result['9'] = elem.get('source')

        return result

    def _freekey_to_marc_dict(elem):
        return {
            'a': elem.get('value'),
            '9': elem.get('source', ''),
        }

    thesaurus_terms = self.get('695', [])

    for value in values:
        if _is_thesaurus(value):
            marc_dict = _thesaurus_to_marc_dict(value)
            thesaurus_terms.append(marc_dict)
        else:
            marc_dict = _freekey_to_marc_dict(value)
            if '653' not in self:
                self['653'] = []

            self['653'].append(marc_dict)
            continue

    return thesaurus_terms


@hep2marc.over('_energy_ranges', '^energy_ranges$')
@utils.ignore_value
def energy_ranges2marc(self, key, values):
    values = force_list(values)

    def _energy_to_marc_dict(energy_range):
        return {
            'e': energy_range,
            '2': 'INSPIRE',
        }

    thesaurus_terms = self.get('695', [])

    for value in values:
        marc_dict = _energy_to_marc_dict(value)
        thesaurus_terms.append(marc_dict)

    self['695'] = thesaurus_terms
