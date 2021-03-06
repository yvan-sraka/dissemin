# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 13:44
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
from papers.utils import iunaccent

def populate_identifiers(apps, se):
    Institution = apps.get_model('papers', 'Institution')
    for i in Institution.objects.all():
        if i.country and i.name:
            i.identifiers = [i.identifier, i.country+':'+iunaccent(i.name)]
        else:
            i.identifiers = [i.identifier]
        i.save(update_fields=['identifiers'])

def backwards(apps, se):
    Institution = apps.get_model('papers', 'Institution')
    for i in Institution.objects.all():
        i.identifier = None
        for id in i.identifiers:
            if '-' in id:
                i.identifier = id
                i.save(update_fields=['identifier'])
                break

class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0042_increase_homepage_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='identifiers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), blank=True, null=True, size=None),
        ),
        migrations.RunSQL(
            ["CREATE INDEX papers_institution_identifiers_idx ON papers_institution USING gin(identifiers);"],
            ["DROP INDEX papers_institution_identifiers_idx;"],
             ),
        migrations.RunPython(populate_identifiers, backwards),
        migrations.RemoveField(
            model_name='institution',
            name='identifier',
        ),
    ]
