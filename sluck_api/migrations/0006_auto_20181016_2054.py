# Generated by Django 2.1.2 on 2018-10-16 23:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sluck_api', '0005_auto_20181016_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token_updated_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 16, 23, 54, 48, 510581, tzinfo=utc)),
        ),
    ]
