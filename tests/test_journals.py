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

from __future__ import absolute_import, division, print_function

from dojson.contrib.marc21.utils import create_record

from inspire_dojson.journals import journals
from inspire_schemas.api import load_schema, validate


def test_issns_from_022__a():
    schema = load_schema('journals')
    subschema = schema['properties']['issns']

    snippet = (
        '<datafield tag="022" ind1=" " ind2=" ">'
        '  <subfield code="a">2213-1337</subfield>'
        '</datafield> '
    )  # record/1445059

    expected = [
        {'value': '2213-1337'},
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['issns'], subschema) is None
    assert expected == result['issns']


def test_issns_from_022__a_b():
    schema = load_schema('journals')
    subschema = schema['properties']['issns']

    snippet = (
        '<datafield tag="022" ind1=" " ind2=" ">'
        '  <subfield code="a">1812-9471</subfield>'
        '  <subfield code="b">Print</subfield>'
        '</datafield>'
    )  # record/1513418

    expected = [
        {
            'medium': 'print',
            'value': '1812-9471',
        },
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['issns'], subschema) is None
    assert expected == result['issns']


def test_issns_from_double_022__a_b():
    schema = load_schema('journals')
    subschema = schema['properties']['issns']

    snippet = (
        '<record>'
        '  <datafield tag="022" ind1=" " ind2=" ">'
        '    <subfield code="a">1812-9471</subfield>'
        '    <subfield code="b">Print</subfield>'
        '  </datafield>'
        '  <datafield tag="022" ind1=" " ind2=" ">'
        '    <subfield code="a">1817-5805</subfield>'
        '    <subfield code="b">Online</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1513418

    expected = [
        {
            'medium': 'print',
            'value': '1812-9471',
        },
        {
            'medium': 'online',
            'value': '1817-5805',
        },
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['issns'], subschema) is None
    assert expected == result['issns']


def test_issns_from_022__a_b_handles_electronic():
    schema = load_schema('journals')
    subschema = schema['properties']['issns']

    snippet = (
        '<datafield tag="022" ind1=" " ind2=" ">'
        '  <subfield code="a">2469-9888</subfield>'
        '  <subfield code="b">electronic</subfield>'
        '</datafield>'
    )  # record/1415879

    expected = [
        {
            'medium': 'online',
            'value': '2469-9888',
        },
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['issns'], subschema) is None
    assert expected == result['issns']


def test_journal_title_from_130__a():
    schema = load_schema('journals')
    subschema = schema['properties']['journal_title']

    snippet = (
        '<datafield tag="130" ind1=" " ind2=" ">'
        '  <subfield code="a">Physical Review Special Topics - Accelerators and Beams</subfield>'
        '</datafield>'
    )  # record/1212820

    expected = {'title': 'Physical Review Special Topics - Accelerators and Beams'}
    result = journals.do(create_record(snippet))

    assert validate(result['journal_title'], subschema) is None
    assert expected == result['journal_title']


def test_journal_title_from_130__a_b():
    schema = load_schema('journals')
    subschema = schema['properties']['journal_title']

    snippet = (
        '<datafield tag="130" ind1=" " ind2=" ">'
        '  <subfield code="a">Humana Mente</subfield>'
        '  <subfield code="b">Journal of Philosophical Studies</subfield>'
        '</datafield>'
    )  # record/1325601

    expected = {
        'title': 'Humana Mente',
        'subtitle': 'Journal of Philosophical Studies',
    }
    result = journals.do(create_record(snippet))

    assert validate(result['journal_title'], subschema) is None
    assert expected == result['journal_title']


def test_related_records_from_530__a_w_0():
    schema = load_schema('journals')
    subschema = schema['properties']['related_records']

    snippet = (
        '<datafield tag="530" ind1=" " ind2=" ">'
        '  <subfield code="0">1212820</subfield>'
        '  <subfield code="a">Phys.Rev.ST Accel.Beams</subfield>'
        '  <subfield code="w">a</subfield>'
        '</datafield>'
    )  # record/1415879

    expected = [
        {
            'curated_relation': True,
            'record': {
                '$ref': 'http://localhost:5000/api/journals/1212820',
            },
            'relation': 'predecessor',
        },
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['related_records'], subschema) is None
    assert expected == result['related_records']


def test_related_records_from_530__a_i_w_0():
    schema = load_schema('journals')
    subschema = schema['properties']['related_records']

    snippet = (
        '<datafield tag="530" ind1=" " ind2=" ">'
        '  <subfield code="0">1214339</subfield>'
        '  <subfield code="a">Zh.Eksp.Teor.Fiz.</subfield>'
        '  <subfield code="i">Original version (Russian)</subfield>'
        '  <subfield code="w">r</subfield>'
        '</datafield>'
    )  # record/1214386

    expected = [
        {
            'curated_relation': True,
            'record': {
                '$ref': 'http://localhost:5000/api/journals/1214339',
            },
            'relation_freetext': 'Original version (Russian)',
        },
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['related_records'], subschema) is None
    assert expected == result['related_records']


def test_license_from_540__a():
    schema = load_schema('journals')
    subschema = schema['properties']['license']

    snippet = (
        '<datafield tag="540" ind1=" " ind2=" ">'
        '  <subfield code="a">CC-BY 4.0</subfield>'
        '</datafield>'
    )  # record/1617955

    expected = {'license': 'CC-BY 4.0'}
    result = journals.do(create_record(snippet))

    assert validate(result['license'], subschema) is None
    assert expected == result['license']


def test_harvesting_info_from_583__a_c_i_3():
    schema = load_schema('journals')
    subschema = schema['properties']['_harvesting_info']

    snippet = (
        '<datafield tag="583" ind1=" " ind2=" ">'
        '  <subfield code="c">2017-08-21</subfield>'
        '  <subfield code="3">New Phys.Sae Mulli,67</subfield>'
        '  <subfield code="a">partial</subfield>'
        '  <subfield code="i">harvest</subfield>'
        '</datafield>'
    )  # record/1616534

    expected = {
        'coverage': 'partial',
        'date_last_harvest': '2017-08-21',
        'last_seen_item': 'New Phys.Sae Mulli,67',
        'method': 'harvest',
    }
    result = journals.do(create_record(snippet))

    assert validate(result['_harvesting_info'], subschema) is None
    assert expected == result['_harvesting_info']


def test_public_notes_from_640__a():
    schema = load_schema('journals')
    subschema = schema['properties']['public_notes']

    snippet = (
        '<datafield tag="640" ind1=" " ind2=" ">'
        '  <subfield code="a">v.1 starts 2013</subfield>'
        '</datafield>'
    )  # record/1466026

    expected = [
        {'value': 'v.1 starts 2013'},
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['public_notes'], subschema) is None
    assert expected == result['public_notes']


def test_publisher_from_643__b():
    schema = load_schema('journals')
    subschema = schema['properties']['publisher']

    snippet = (
        '<datafield tag="643" ind1=" " ind2=" ">'
        '  <subfield code="b">ANITA PUBLICATIONS, INDIA</subfield>'
        '</datafield>'
    )  # record/1211888

    expected = ['ANITA PUBLICATIONS, INDIA']
    result = journals.do(create_record(snippet))

    assert validate(result['publisher'], subschema) is None
    assert expected == result['publisher']


def test_publisher_from_double_643__b():
    schema = load_schema('journals')
    subschema = schema['properties']['publisher']

    snippet = (
        '<record>'
        '  <datafield tag="643" ind1=" " ind2=" ">'
        '    <subfield code="b">Elsevier</subfield>'
        '  </datafield>'
        '  <datafield tag="643" ind1=" " ind2=" ">'
        '    <subfield code="b">Science Press</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1212635

    expected = [
        'Elsevier',
        'Science Press',
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['publisher'], subschema) is None
    assert expected == result['publisher']


def test_private_notes_from_667__x():
    schema = load_schema('journals')
    subschema = schema['properties']['_private_notes']

    snippet = (
        '<datafield tag="667" ind1=" " ind2=" ">'
        '  <subfield code="x">Open Access</subfield>'
        '</datafield>'
    )  # record/1485643

    expected = [
        {'value': 'Open Access'},
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['_private_notes'], subschema) is None
    assert expected == result['_private_notes']


def test_doi_prefixes_from_677__d():
    schema = load_schema('journals')
    subschema = schema['properties']['doi_prefixes']

    snippet = (
        '<datafield tag="677" ind1=" " ind2=" ">'
        '  <subfield code="d">10.17406/GJSFR</subfield>'
        '</datafield>'
    )  # record/1617963

    expected = ['10.17406/GJSFR']
    result = journals.do(create_record(snippet))

    assert validate(result['doi_prefixes'], subschema) is None
    assert expected == result['doi_prefixes']


def test_public_notes_from_680__i():
    schema = load_schema('journals')
    subschema = schema['properties']['public_notes']

    snippet = (
        u'<datafield tag="680" ind1=" " ind2=" ">'
        u'  <subfield code="i">Russian Title: Высокомолекулярные соединения. Серия В. Химия полимеров (Vysokomolekulyarnye Soedineniya, Seriya B)</subfield>'
        u'</datafield>'
    )  # record/1615699

    expected = [
        {'value': u'Russian Title: Высокомолекулярные соединения. Серия В. Химия полимеров (Vysokomolekulyarnye Soedineniya, Seriya B)'},
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['public_notes'], subschema) is None
    assert expected == result['public_notes']


def test_proceedings_from_double_690__a():
    schema = load_schema('journals')
    subschema = schema['properties']['proceedings']

    snippet = (
        '<record>'
        '  <datafield tag="690" ind1=" " ind2=" ">'
        '    <subfield code="a">NON-PUBLISHED</subfield>'
        '  </datafield>'
        '  <datafield tag="690" ind1=" " ind2=" ">'
        '    <subfield code="a">Proceedings</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1213080

    expected = True
    result = journals.do(create_record(snippet))

    assert validate(result['proceedings'], subschema) is None
    assert expected == result['proceedings']


def test_refereed_from_690__a_peer_review():
    schema = load_schema('journals')
    subschema = schema['properties']['refereed']

    snippet = (
        '<datafield tag="690" ind1=" " ind2=" ">'
        '  <subfield code="a">Peer Review</subfield>'
        '</datafield>'
    )  # record/1617955

    expected = True
    result = journals.do(create_record(snippet))

    assert validate(result['refereed'], subschema) is None
    assert expected == result['refereed']


def test_refereed_from_690__a_non_published():
    schema = load_schema('journals')
    subschema = schema['properties']['refereed']

    snippet = (
        '<datafield tag="690" ind1=" " ind2=" ">'
        '  <subfield code="a">NON-PUBLISHED</subfield>'
        '</datafield>'
    )  # record/1357923

    expected = False
    result = journals.do(create_record(snippet))

    assert validate(result['refereed'], subschema) is None
    assert expected == result['refereed']


def test_short_title_from_711__a():
    schema = load_schema('journals')
    subschema = schema['properties']['short_title']

    snippet = (
        '<datafield tag="711" ind1=" " ind2=" ">'
        '  <subfield code="a">Phys.Rev.ST Accel.Beams</subfield>'
        '</datafield>'
    )  # record/1212820

    expected = 'Phys.Rev.ST Accel.Beams'
    result = journals.do(create_record(snippet))

    assert validate(result['short_title'], subschema) is None
    assert expected == result['short_title']


def test_short_title_from_711__a_u():
    schema = load_schema('journals')
    short_title_schema = schema['properties']['short_title']
    title_variants_schema = schema['properties']['title_variants']

    snippet = (
        '<datafield tag="711" ind1=" " ind2=" ">'
        '  <subfield code="a">Univ.Politech.Bucharest Sci.Bull.</subfield>'
        '  <subfield code="u">Univ.Politech.Bucharest Sci.Bull.A</subfield>'
        '</datafield>'
    )  # record/1485822

    expected_short_title = 'Univ.Politech.Bucharest Sci.Bull.A'
    expected_title_variants = ['Univ.Politech.Bucharest Sci.Bull.']
    result = journals.do(create_record(snippet))

    assert validate(result['short_title'], short_title_schema) is None
    assert expected_short_title == result['short_title']

    assert validate(result['title_variants'], title_variants_schema) is None
    assert expected_title_variants == result['title_variants']


def test_short_title_from_711__a_u_and_double_730__a():
    schema = load_schema('journals')
    short_title_schema = schema['properties']['short_title']
    title_variants_schema = schema['properties']['title_variants']

    snippet = (
        '<record>'
        '  <datafield tag="711" ind1=" " ind2=" ">'
        '    <subfield code="a">Diss.Abstr.Int.</subfield>'
        '    <subfield code="u">Diss.Abstr.Int.B</subfield>'
        '  </datafield>'
        '  <datafield tag="730" ind1=" " ind2=" ">'
        '    <subfield code="a">DISS ABSTR INT</subfield>'
        '  </datafield>'
        '  <datafield tag="730" ind1=" " ind2=" ">'
        '    <subfield code="a">DABBB</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1212928

    expected_short_title = 'Diss.Abstr.Int.B'
    expected_title_variants = [
        'Diss.Abstr.Int.',
        'DISS ABSTR INT',
        'DABBB',
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['short_title'], short_title_schema) is None
    assert expected_short_title == result['short_title']

    assert validate(result['title_variants'], title_variants_schema) is None
    assert sorted(expected_title_variants) == sorted(result['title_variants'])


def test_title_variants_from_730__a():
    schema = load_schema('journals')
    subschema = schema['properties']['title_variants']

    snippet = (
        '<datafield tag="730" ind1=" " ind2=" ">'
        '  <subfield code="a">PHYSICAL REVIEW SPECIAL TOPICS ACCELERATORS AND BEAMS</subfield>'
        '</datafield>'
    )  # record/1212820

    expected = ['PHYSICAL REVIEW SPECIAL TOPICS ACCELERATORS AND BEAMS']
    result = journals.do(create_record(snippet))

    assert validate(result['title_variants'], subschema) is None
    assert expected == result['title_variants']


def test_title_variants_from_double_730__a():
    schema = load_schema('journals')
    subschema = schema['properties']['title_variants']

    snippet = (
        '<record>'
        '  <datafield tag="730" ind1=" " ind2=" ">'
        '    <subfield code="a">PHYS REV SPECIAL TOPICS ACCELERATORS BEAMS</subfield>'
        '  </datafield>'
        '  <datafield tag="730" ind1=" " ind2=" ">'
        '    <subfield code="a">PHYSICS REVIEW ST ACCEL BEAMS</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1212820

    expected = [
        'PHYS REV SPECIAL TOPICS ACCELERATORS BEAMS',
        'PHYSICS REVIEW ST ACCEL BEAMS',
    ]
    result = journals.do(create_record(snippet))

    assert validate(result['title_variants'], subschema) is None
    assert expected == result['title_variants']


def test_title_variants_skips_730_when_it_contains_a_b():
    snippet = (
        '<datafield tag="730" ind1=" " ind2=" ">'
        '  <subfield code="a">AIHPD</subfield>'
        '  <subfield code="b">D</subfield>'
        '</datafield>'
    )  # record/1511950

    result = journals.do(create_record(snippet))

    assert 'title_variants' not in result


def test_book_series_from_double_980__a():
    schema = load_schema('journals')
    subschema = schema['properties']['book_series']

    snippet = (
        '<record>'
        '  <datafield tag="980" ind1=" " ind2=" ">'
        '    <subfield code="a">JOURNALS</subfield>'
        '  </datafield>'
        '  <datafield tag="980" ind1=" " ind2=" ">'
        '    <subfield code="a">BookSeries</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1311535

    expected = True
    result = journals.do(create_record(snippet))

    assert validate(result['book_series'], subschema) is None
    assert expected == result['book_series']


def test_deleted_from_980__a():
    schema = load_schema('journals')
    subschema = schema['properties']['deleted']

    snippet = (
        '<datafield tag="980" ind1=" " ind2=" ">'
        '  <subfield code="a">DELETED</subfield>'
        '</datafield>'
    )  # synthetic data

    expected = True
    result = journals.do(create_record(snippet))

    assert validate(result['deleted'], subschema) is None
    assert expected == result['deleted']
