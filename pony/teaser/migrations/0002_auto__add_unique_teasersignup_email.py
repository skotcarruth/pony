# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'TeaserSignup', fields ['email']
        db.create_unique('teaser_teasersignup', ['email'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TeaserSignup', fields ['email']
        db.delete_unique('teaser_teasersignup', ['email'])


    models = {
        'teaser.teasersignup': {
            'Meta': {'ordering': "('-created_ts',)", 'object_name': 'TeaserSignup'},
            'birthday_day': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'birthday_month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['teaser']
