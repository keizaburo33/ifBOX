# Generated by Django 3.0.6 on 2020-09-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IfBoxHp', '0016_admininformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='admininformation',
            name='aduminname',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
