# Generated by Django 3.0.6 on 2020-08-30 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IfBoxHp', '0008_auto_20200830_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='logindate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]