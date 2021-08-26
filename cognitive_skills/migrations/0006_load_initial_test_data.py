# Generated by Django 3.2.5 on 2021-08-03 07:28

from django.db import migrations
from django.core.management import call_command
 
fixture = 'initial_tests.json'
 
def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='cognitive_skills')

class Migration(migrations.Migration):

    dependencies = [
        ('cognitive_skills', '0005_auto_20210802_0624'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]