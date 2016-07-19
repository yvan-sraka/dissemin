# -*- encoding: utf-8 -*-

# Dissemin: open access policy enforcement tool
# Copyright (C) 2014 Antonin Delpeuch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
import django.test

from backend.crossref import CrossRefAPI
from backend.oai import OaiPaperSource
from backend.tests import PrefilledTest
from papers.models import Paper
from papers.testajax import JsonRenderingTest


class PaperApiTest(JsonRenderingTest):

    def test_valid_paper(self):
        p = self.r3.papers[0]
        parsed = self.checkJson(self.getPage('papers-detail', args=[p.pk]))

    def test_invalid_paper(self):
        self.checkJson(self.getPage('papers-detail', args=[123456]), 404)

    def test_valid_doi(self):
        self.checkJson(self.getPage('api-paper-doi',
                                    args=['10.1016/0379-6779(91)91572-r']))

    def test_invalid_doi(self):
        self.checkJson(self.getPage('api-paper-doi',
                                    args=['10.10.10.10.10']), 404)

    def test_query(self):
        invalid_payloads = [
            'test', '{}',
            '{"doi":"anurisecbld"}',
            '{"title":""}',
            '{"title":"this is a test"}',
            '{"title":"this is a test","date":"aunriset"}',
            '{"title":"this is a test","date":"2008"}',
            '{"title":"this is a test","date":"2008","authors":"test"}',
            '{"title":"this is a test","date":"2008-03","authors":[]}',
            '{"title":"this is a test","date":"2008-03","authors":["lsc"]}',
            '{"title":"test","date":"2008-03","authors":[{"error":"test"}]}',
            ]

        for payload in invalid_payloads:
            self.checkJson(self.postPage('api-paper-query', postargs=payload,
                                         postkwargs={'content_type': 'application/json'}), 400)

        valid_payloads = [
            '{"title":"Strange resonances measured in Al+Al collisions at sqrt {S_ NN }= 2.65 GeV with the FOPI detector","date":"2015","authors":[{"plain":"Lopez, X."}]}',
            '{"doi":"10.1016/j.paid.2009.02.013"}',
                ]
        for payload in valid_payloads:
            self.checkJson(self.postPage('api-paper-query', postargs=payload,
                                         postkwargs={'content_type': 'application/json'}), 200)
