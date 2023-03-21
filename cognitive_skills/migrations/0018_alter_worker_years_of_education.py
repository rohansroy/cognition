# Generated by Django 3.2.5 on 2023-03-21 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognitive_skills', '0017_worker_preliminary_diagnosis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='years_of_education',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], help_text='How many years of education have you received?', max_length=255),
        ),
    ]
