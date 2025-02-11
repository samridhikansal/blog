# Generated by Django 5.1.4 on 2025-02-11 01:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0010_alter_post_time_comments_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments_reply',
            name='author',
            field=models.CharField(blank=True, default='Guest', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateField(blank=True, default=datetime.datetime(2025, 2, 11, 1, 25, 56, 56275), null=True),
        ),
    ]
