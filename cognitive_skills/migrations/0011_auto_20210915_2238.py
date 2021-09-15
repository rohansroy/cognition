# Generated by Django 3.2.5 on 2021-09-15 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognitive_skills', '0010_auto_20210915_2123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='worker',
            options={'ordering': ('created_at',)},
        ),
        migrations.AddField(
            model_name='result',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
