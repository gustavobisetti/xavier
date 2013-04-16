# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subject.slug'
        db.add_column(u'subjects_subject', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=30, null=True),
                      keep_default=False)

        # Adding unique constraint on 'Subject', fields ['name']
        db.create_unique(u'subjects_subject', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Subject', fields ['name']
        db.delete_unique(u'subjects_subject', ['name'])

        # Deleting field 'Subject.slug'
        db.delete_column(u'subjects_subject', 'slug')


    models = {
        u'subjects.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '30', 'null': 'True'})
        }
    }

    complete_apps = ['subjects']