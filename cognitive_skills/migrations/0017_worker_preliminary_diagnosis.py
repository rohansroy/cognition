# Generated by Django 3.2.5 on 2022-12-23 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognitive_skills', '0016_auto_20221223_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='preliminary_diagnosis',
            field=models.CharField(blank=True, help_text='Leave blank if unknown', max_length=255, null=True),
        ),
    ]