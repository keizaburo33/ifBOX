# Generated by Django 3.0.6 on 2020-09-30 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IfBoxHp', '0024_runninginfo_zangyotime'),
    ]

    operations = [
        migrations.AddField(
            model_name='runninginfo',
            name='zangyostr',
            field=models.CharField(default='0:00', max_length=10),
        ),
        migrations.AlterField(
            model_name='runninginfo',
            name='zangyotime',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
