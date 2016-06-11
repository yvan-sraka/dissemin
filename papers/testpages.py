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

import unittest
import django.test
import html5lib
from papers.utils import overescaped_re
from django.core.urlresolvers import reverse
from backend.tests import PrefilledTest
from backend.crossref import CrossRefPaperSource
from backend.oai import OaiPaperSource
from papers.models import OaiRecord

# TODO TO BE TESTED

#        # Paper views
#        url(r'^mail_paper/(?P<pk>\d+)/$', views.mailPaperView, name='mail_paper'),
#        url(r'^journal/(?P<journal>\d+)/$', views.searchView, name='journal'),
#        # Tasks, AJAX
#        url(r'^researcher/(?P<pk>\d+)/update/$', views.refetchResearcher, name='refetch-researcher'),
#        url(r'^researcher/(?P<pk>\d+)/recluster/$', views.reclusterResearcher, name='recluster-researcher'),
#        # Annotations (to be deleted)
#        url(r'^annotations/$', views.AnnotationsView.as_view(), name='annotations'),

class RenderingTest(PrefilledTest):
    def setUp(self):
        super(RenderingTest, self).setUp()
        self.client = django.test.Client()
        self.parser = html5lib.HTMLParser(strict=True)

    def checkHtml(self, resp):
        self.assertEqual(resp.status_code, 200)
        # Check that there are no overescaped HTML strings…
        self.assertEqual(overescaped_re.findall(resp.content), [])
        try:
            parsed = self.parser.parse(resp.content)
        except html5lib.html5parser.ParseError as e:
            print resp.content
            print "HTML validation error: "+unicode(e)
            raise e

    def getPage(self, *args, **kwargs):
        urlargs = kwargs.copy()
        if 'getargs' in kwargs:
            del urlargs['getargs']
            return self.client.get(reverse(*args, **urlargs), kwargs['getargs'])
        return self.client.get(reverse(*args, **kwargs))

    def checkPage(self, *args, **kwargs):
        self.checkHtml(self.getPage(*args, **kwargs))

    def checkPermanentRedirect(self, *args, **kwargs):
        self.assertEqual(self.getPage(*args, **kwargs).status_code, 301)

    def checkUrl(self, url):
        self.checkHtml(self.client.get(url))

class InstitutionPagesTest(RenderingTest):
    def test_dept(self):
        self.checkUrl(self.d.url)
        self.checkUrl(self.di.url)

    def test_univ(self):
        self.checkUrl(self.i.url)

class PaperPagesTest(RenderingTest):
    def test_index(self):
        self.checkHtml(self.getPage('index'))
        
    def test_researcher(self):
        for r in [self.r1, self.r2, self.r3, self.r4]:
            self.checkPage('researcher', kwargs={'researcher':r.pk, 'slug':r.slug})
            self.checkUrl(self.r4.url)

    def test_researcher_orcid(self):
        self.checkPermanentRedirect('researcher-by-orcid', kwargs={'orcid':self.r4.orcid})

    def test_search_no_parameters(self):
        self.checkPage('search')

    def test_search_researcher_pk(self):
        self.checkPermanentRedirect('search', getargs={'researcher':self.r3.pk})
        self.checkPage('search', getargs={'researcher':self.r3.pk, 'slug':self.r3.slug})

    def test_search_name(self):
        self.checkPage('search', getargs={'name':self.r3.name_id})

    def test_search_department(self):
        self.checkPage('search', getargs={'department':self.di.pk})

    # ampersands not escaped in django bootstrap pagination, https://github.com/jmcclell/django-bootstrap-pagination/issues/41

    def test_paper(self):
        for p in self.r3.papers:
            self.checkPage('paper', kwargs={'pk':p.id, 'slug':p.slug})
            if p.is_orphan() and p.visible:
                print p
            self.assertTrue(not p.is_orphan())

    def test_paper_by_doi(self):
        publi = OaiRecord.objects.filter(doi__isnull=False)[0]
        self.checkPermanentRedirect('paper-doi', kwargs={'doi':publi.doi})

