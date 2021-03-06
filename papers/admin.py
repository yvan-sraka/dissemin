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

from django.contrib import admin
from papers.models import Department
from papers.models import Institution
from papers.models import Name
from papers.models import OaiRecord
from papers.models import OaiSource
from papers.models import Paper
from papers.models import PaperWorld
from papers.models import Researcher
from solo.admin import SingletonModelAdmin


class NameInline(admin.TabularInline):
    model = Name
    extra = 0


class OaiInline(admin.TabularInline):
    model = OaiRecord
    extra = 0


class PaperAdmin(admin.ModelAdmin):
    fields = ['title', 'pubdate', 'visible', 'doctype', 'oa_status']
    list_display = ('title', 'pubdate', 'visible', 'doctype', 'oa_status')


class OaiRecordAdmin(admin.ModelAdmin):
    raw_id_fields = ('about',)


class ResearcherAdmin(admin.ModelAdmin):
    raw_id_fields = ('name', 'stats',)

admin.site.register(Institution)
admin.site.register(Department)
admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(Name)
admin.site.register(Paper, PaperAdmin)
admin.site.register(OaiSource)
admin.site.register(OaiRecord, OaiRecordAdmin)
admin.site.register(PaperWorld, SingletonModelAdmin)
