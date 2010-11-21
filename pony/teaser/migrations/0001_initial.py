# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TeaserSignup'
        db.create_table('teaser_teasersignup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('birthday_month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('birthday_day', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created_ts', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('teaser', ['TeaserSignup'])


    def backwards(self, orm):
        
        # Deleting model 'TeaserSignup'
        db.delete_table('teaser_teasersignup')


    models = {
        'teaser.teasersignup': {
            'Meta': {'ordering': "('-created_ts',)", 'object_name': 'TeaserSignup'},
            'birthday_day': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'birthday_month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['teaser']
