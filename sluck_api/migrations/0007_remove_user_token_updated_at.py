# Generated by Django 2.1.2 on 2018-10-17 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sluck_api', '0006_auto_20181016_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token_updated_at',
        ),
    ]